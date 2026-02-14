"""Rate limiting and retry utilities for API calls."""

import time
import logging
from typing import Optional, Callable, TypeVar, Any
from functools import wraps
import asyncio

logger = logging.getLogger("eden_agent.rate_limit")

T = TypeVar('T')


class RateLimiter:
    """Simple rate limiter using token bucket algorithm."""
    
    def __init__(self, max_calls: int, time_window: float):
        """
        Initialize rate limiter.
        
        Args:
            max_calls: Maximum number of calls allowed in time window
            time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls: list[float] = []
        
    async def acquire(self) -> None:
        """Wait if necessary to respect rate limit."""
        now = time.time()
        
        # Remove old calls outside the time window
        self.calls = [
            call_time for call_time in self.calls
            if now - call_time < self.time_window
        ]
        
        # If at limit, wait until oldest call expires
        if len(self.calls) >= self.max_calls:
            oldest_call = min(self.calls)
            wait_time = self.time_window - (now - oldest_call)
            if wait_time > 0:
                logger.debug(
                    "Rate limit reached, waiting %.2f seconds",
                    wait_time
                )
                await asyncio.sleep(wait_time)
                # Recursively check again after waiting
                await self.acquire()
                return
        
        # Record this call
        self.calls.append(time.time())


class RetryConfig:
    """Configuration for retry behavior."""
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
    ):
        """
        Initialize retry configuration.
        
        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Initial delay between retries in seconds
            max_delay: Maximum delay between retries in seconds
            exponential_base: Base for exponential backoff
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
    
    def get_delay(self, attempt: int) -> float:
        """Calculate delay for given attempt number."""
        delay = self.base_delay * (self.exponential_base ** attempt)
        return min(delay, self.max_delay)


async def retry_with_backoff(
    func: Callable[..., T],
    *args: Any,
    retry_config: Optional[RetryConfig] = None,
    retry_on: Optional[tuple[type[Exception], ...]] = None,
    **kwargs: Any,
) -> T:
    """
    Execute function with exponential backoff retry.
    
    Args:
        func: Async function to execute
        args: Positional arguments for func
        retry_config: Retry configuration
        retry_on: Tuple of exception types to retry on
        kwargs: Keyword arguments for func
        
    Returns:
        Result of successful function call
        
    Raises:
        Last exception if all retries exhausted
    """
    if retry_config is None:
        retry_config = RetryConfig()
    
    if retry_on is None:
        retry_on = (Exception,)
    
    last_exception: Optional[Exception] = None
    
    for attempt in range(retry_config.max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except retry_on as e:
            last_exception = e
            
            if attempt == retry_config.max_retries:
                logger.error(
                    "Max retries (%d) exhausted for %s: %s",
                    retry_config.max_retries,
                    func.__name__,
                    e
                )
                raise
            
            delay = retry_config.get_delay(attempt)
            logger.warning(
                "Attempt %d/%d failed for %s: %s. Retrying in %.2fs",
                attempt + 1,
                retry_config.max_retries + 1,
                func.__name__,
                e,
                delay
            )
            await asyncio.sleep(delay)
    
    # Should never reach here, but for type safety
    if last_exception:
        raise last_exception
    raise RuntimeError("Unexpected retry loop exit")


def with_rate_limit(rate_limiter: RateLimiter):
    """Decorator to apply rate limiting to async functions."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            await rate_limiter.acquire()
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def with_retry(
    retry_config: Optional[RetryConfig] = None,
    retry_on: Optional[tuple[type[Exception], ...]] = None,
):
    """Decorator to apply retry logic to async functions."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            return await retry_with_backoff(
                func,
                *args,
                retry_config=retry_config,
                retry_on=retry_on,
                **kwargs
            )
        return wrapper
    return decorator
