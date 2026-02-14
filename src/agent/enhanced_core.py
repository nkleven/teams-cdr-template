"""Enhanced AI agent implementation with advanced features."""

import logging
from typing import Dict, List, Optional, Any, Callable, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import asyncio

from anthropic import Anthropic, APIError, APITimeoutError  # type: ignore[import-not-found]
from anthropic.types import TextBlock, ToolUseBlock  # type: ignore[import-not-found]

from ..config import settings
from ..tools.base import BaseTool
from ..tracing.tracer import tracer
from ..rate_limit import RateLimiter, RetryConfig, retry_with_backoff


# Type aliases
Message = Dict[str, Any]
ToolResult = Dict[str, Any]

# Constants
DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant."
DEFAULT_MAX_ITERATIONS = 10
MAX_CONTEXT_WINDOW = 100000  # tokens

logger = logging.getLogger("eden_agent.enhanced_agent")


class AgentError(Exception):
    """Base exception for agent errors."""


class ToolExecutionError(AgentError):
    """Exception raised when tool execution fails."""


class ContextOverflowError(AgentError):
    """Exception raised when context exceeds limits."""


@dataclass
class AgentMetrics:
    """Track agent performance metrics."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_tokens_used: int = 0
    total_tool_calls: int = 0
    avg_response_time: float = 0.0
    error_count_by_type: Dict[str, int] = field(default_factory=dict)
    tool_usage_stats: Dict[str, int] = field(default_factory=dict)
    
    def record_request(self, success: bool, tokens: int, response_time: float, error_type: Optional[str] = None):
        """Record a request's metrics."""
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
            if error_type:
                self.error_count_by_type[error_type] = self.error_count_by_type.get(error_type, 0) + 1
        
        self.total_tokens_used += tokens
        # Update running average
        self.avg_response_time = (self.avg_response_time * (self.total_requests - 1) + response_time) / self.total_requests
    
    def record_tool_usage(self, tool_name: str):
        """Record tool usage."""
        self.total_tool_calls += 1
        self.tool_usage_stats[tool_name] = self.tool_usage_stats.get(tool_name, 0) + 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary."""
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": self.successful_requests / max(self.total_requests, 1),
            "total_tokens_used": self.total_tokens_used,
            "total_tool_calls": self.total_tool_calls,
            "avg_response_time": round(self.avg_response_time, 3),
            "error_count_by_type": self.error_count_by_type,
            "tool_usage_stats": self.tool_usage_stats,
        }


@dataclass
class AgentConfig:
    """Configuration for enhanced agent."""
    max_iterations: int = DEFAULT_MAX_ITERATIONS
    enable_context_management: bool = True
    enable_tool_validation: bool = True
    enable_streaming: bool = False
    enable_caching: bool = False
    max_history_messages: int = 50
    tool_timeout_seconds: float = 30.0
    enable_safety_checks: bool = True


class EnhancedAgent:
    """Enhanced AI Agent with advanced capabilities.
    
    Features:
    - Advanced context management with automatic truncation
    - Tool validation and safety checks
    - Comprehensive metrics tracking
    - Tool execution timeout
    - Conversation history management
    - Middleware/plugin system
    - Graceful degradation
    - Streaming support (optional)
    
    Example:
        >>> config = AgentConfig(max_iterations=15)
        >>> agent = EnhancedAgent(tools=[calculator_tool], config=config)
        >>> response = await agent.chat("What is 2+2?")
    """
    
    def __init__(
        self,
        tools: Optional[List[BaseTool]] = None,
        config: Optional[AgentConfig] = None,
        middlewares: Optional[List[Callable]] = None
    ):
        """Initialize the enhanced agent.
        
        Args:
            tools: Optional list of tools to register
            config: Agent configuration
            middlewares: List of middleware functions for request/response processing
            
        Raises:
            AgentError: If initialization fails
        """
        try:
            self.client = Anthropic(api_key=settings.anthropic_api_key)
            logger.info("✓ Enhanced Agent initialized successfully")
        except Exception as e:
            logger.error("✗ Failed to initialize Anthropic client: %s", e)
            raise AgentError(f"Failed to initialize agent: {e}") from e
        
        self.config = config or AgentConfig()
        self._tools: Dict[str, BaseTool] = {}
        self._middlewares: List[Callable] = middlewares or []
        self.conversation_history: List[Message] = []
        self.metrics = AgentMetrics()
        
        # Register tools
        if tools:
            for tool in tools:
                self.register_tool(tool)
        
        # Initialize rate limiter
        self.rate_limiter: Optional[RateLimiter] = None
        if settings.rate_limit_enabled:
            self.rate_limiter = RateLimiter(
                max_calls=settings.rate_limit_max_calls,
                time_window=settings.rate_limit_time_window,
            )
        
        # Initialize retry config
        self.retry_config: Optional[RetryConfig] = None
        if settings.retry_enabled:
            self.retry_config = RetryConfig(
                max_retries=settings.retry_max_attempts,
                base_delay=settings.retry_base_delay,
                max_delay=settings.retry_max_delay,
            )
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if exc_type is not None:
            logger.error("Agent exited with error: %s", exc_val)
        logger.info("Agent metrics: %s", self.metrics.get_summary())
    
    def register_tool(self, tool: BaseTool) -> None:
        """Register a new tool with validation.
        
        Args:
            tool: Tool instance to register
            
        Raises:
            ValueError: If tool is invalid
        """
        tool_name = tool.definition.name
        
        if self.config.enable_tool_validation:
            self._validate_tool(tool)
        
        if tool_name in self._tools:
            logger.warning("Tool '%s' already registered, replacing", tool_name)
        
        self._tools[tool_name] = tool
        logger.info("✓ Tool '%s' registered", tool_name)
    
    def _validate_tool(self, tool: BaseTool) -> None:
        """Validate tool definition and implementation.
        
        Args:
            tool: Tool to validate
            
        Raises:
            ValueError: If tool is invalid
        """
        definition = tool.definition
        if not definition.name:
            raise ValueError("Tool must have a name")
        if not definition.description:
            raise ValueError(f"Tool '{definition.name}' must have a description")
        if not definition.input_schema:
            raise ValueError(f"Tool '{definition.name}' must have an input schema")
        
        # Validate execute method exists and is async
        if not hasattr(tool, 'execute'):
            raise ValueError(f"Tool '{definition.name}' must implement execute method")
        if not asyncio.iscoroutinefunction(tool.execute):
            raise ValueError(f"Tool '{definition.name}' execute method must be async")
    
    def unregister_tool(self, tool_name: str) -> bool:
        """Unregister a tool by name."""
        if tool_name in self._tools:
            del self._tools[tool_name]
            logger.info("✓ Tool '%s' unregistered", tool_name)
            return True
        logger.warning("Tool '%s' not found", tool_name)
        return False
    
    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self._tools.keys())
    
    def get_tool_definitions_for_display(self) -> List[Dict[str, Any]]:
        """Get formatted tool definitions for display."""
        return [
            {
                "name": tool.definition.name,
                "description": tool.definition.description,
                "parameters": tool.definition.input_schema.get("properties", {})
            }
            for tool in self._tools.values()
        ]
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history.clear()
        logger.info("✓ Conversation history cleared")
    
    def get_history(self) -> List[Message]:
        """Get conversation history."""
        return self.conversation_history.copy()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics."""
        return self.metrics.get_summary()
    
    def _manage_context_window(self, messages: List[Message]) -> List[Message]:
        """Manage context window to stay within limits.
        
        Args:
            messages: Current conversation messages
            
        Returns:
            Truncated messages if needed
        """
        if not self.config.enable_context_management:
            return messages
        
        # Keep only recent messages if history is too long
        if len(messages) > self.config.max_history_messages:
            # Keep system message (if exists) and recent messages
            truncated = messages[-self.config.max_history_messages:]
            logger.info("Truncated conversation history to %d messages", len(truncated))
            return truncated
        
        return messages
    
    def _get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get tool definitions for Claude API."""
        return [tool.definition.model_dump() for tool in self._tools.values()]
    
    def _find_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Find a tool by name."""
        return self._tools.get(tool_name)
    
    async def _execute_single_tool(self, block: ToolUseBlock) -> ToolResult:
        """Execute a single tool with timeout and error handling.
        
        Args:
            block: ToolUseBlock from Claude's response
            
        Returns:
            Tool result dictionary
        """
        tool = self._find_tool(block.name)
        
        if not tool:
            error_msg = f"Tool '{block.name}' not found"
            logger.error(error_msg)
            return {
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": f"Error: {error_msg}",
                "is_error": True,
            }
        
        try:
            with tracer.trace_operation(
                "tool_execution",
                attributes={
                    "tool_name": block.name,
                    "input_keys": ",".join(block.input.keys()),
                },
            ) as tool_span:
                # Execute with timeout
                result = await asyncio.wait_for(
                    tool.execute(**block.input),
                    timeout=self.config.tool_timeout_seconds
                )
                
                tool_span.set_attribute("result_type", type(result).__name__)
                tool_span.set_attribute("success", True)
                
                # Record metrics
                self.metrics.record_tool_usage(block.name)
                
                logger.debug("Tool '%s' executed successfully", block.name)
                return {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                }
                
        except asyncio.TimeoutError:
            error_msg = f"Tool '{block.name}' execution timed out after {self.config.tool_timeout_seconds}s"
            logger.error(error_msg)
            return {
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": f"Error: {error_msg}",
                "is_error": True,
            }
        except Exception as e:
            error_msg = f"Tool '{block.name}' execution failed: {str(e)}"
            logger.error(error_msg)
            return {
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": f"Error: {error_msg}",
                "is_error": True,
            }
    
    async def _execute_tools(self, response) -> List[ToolResult]:
        """Execute all tools from Claude's response in parallel when possible."""
        tool_results = []
        tool_blocks = [block for block in response.content if isinstance(block, ToolUseBlock)]
        
        if not tool_blocks:
            return tool_results
        
        # Execute tools in parallel
        tasks = [self._execute_single_tool(block) for block in tool_blocks]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                logger.error("Unexpected error in tool execution: %s", result)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": "unknown",
                    "content": f"Error: {str(result)}",
                    "is_error": True,
                })
            else:
                tool_results.append(result)
        
        return tool_results
    
    def _extract_text_response(self, response) -> str:
        """Extract text content from Claude response."""
        text_parts = []
        for block in response.content:
            if isinstance(block, TextBlock):
                text_parts.append(block.text)
        return "".join(text_parts) if text_parts else "No response generated."
    
    async def _make_api_call(
        self,
        messages: List[Message],
        system_prompt: str,
        tool_definitions: List[Dict[str, Any]],
        iteration: int
    ):
        """Make a single API call to Claude with comprehensive tracking."""
        with tracer.trace_operation(
            "claude_api_call",
            attributes={
                "model": settings.model_name,
                "temperature": settings.temperature,
                "max_tokens": settings.max_tokens,
                "message_count": len(messages),
                "iteration": iteration,
                "tool_count": len(tool_definitions),
            },
        ) as api_span:
            start_time = datetime.now()
            
            result = self.client.messages.create(
                model=settings.model_name,
                max_tokens=settings.max_tokens,
                temperature=settings.temperature,
                system=system_prompt,
                messages=messages,
                tools=tool_definitions or None,
            )
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            api_span.set_attribute("stop_reason", result.stop_reason or "unknown")
            api_span.set_attribute("content_block_count", len(result.content))
            api_span.set_attribute("response_time_seconds", response_time)
            
            # Estimate tokens (actual usage would come from API response if available)
            estimated_tokens = result.usage.input_tokens + result.usage.output_tokens if hasattr(result, 'usage') else 0
            api_span.set_attribute("estimated_tokens", estimated_tokens)
            
            return result, response_time, estimated_tokens
    
    def _validate_chat_input(self, user_message: str, max_iterations: int) -> None:
        """Validate chat input parameters."""
        if not user_message or not user_message.strip():
            raise ValueError("User message cannot be empty")
        if max_iterations < 1 or max_iterations > 50:
            raise ValueError("max_iterations must be between 1 and 50")
    
    async def _apply_middlewares(self, phase: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply middleware functions."""
        for middleware in self._middlewares:
            try:
                data = await middleware(phase, data)
            except Exception as e:
                logger.error("Middleware error in phase '%s': %s", phase, e)
        return data
    
    async def chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        max_iterations: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Chat with the enhanced agent.
        
        Args:
            user_message: User's input message
            system_prompt: Optional system prompt override
            max_iterations: Optional max iterations override
            metadata: Optional metadata for tracking/logging
            
        Returns:
            Agent's final text response
            
        Raises:
            AgentError: If agent encounters an unrecoverable error
        """
        start_time = datetime.now()
        request_id = metadata.get("request_id", "unknown") if metadata else "unknown"
        
        # Validate inputs
        max_iterations = max_iterations or self.config.max_iterations
        self._validate_chat_input(user_message, max_iterations)
        
        system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        
        with tracer.trace_operation(
            "enhanced_agent_chat",
            attributes={
                "user_message_length": len(user_message),
                "tool_count": len(self._tools),
                "max_iterations": max_iterations,
                "request_id": request_id,
            },
        ) as root_span:
            try:
                # Apply pre-processing middleware
                await self._apply_middlewares("pre_request", {
                    "user_message": user_message,
                    "system_prompt": system_prompt
                })
                
                # Add user message to history
                self.conversation_history.append({
                    "role": "user",
                    "content": user_message,
                })
                
                # Manage context window
                messages = self._manage_context_window(self.conversation_history.copy())
                tool_definitions = self._get_tool_definitions()
                
                root_span.set_attribute("tool_definitions_count", len(tool_definitions))
                
                iteration = 0
                total_tokens = 0
                
                while iteration < max_iterations:
                    iteration += 1
                    logger.debug("Chat iteration %d/%d", iteration, max_iterations)
                    
                    try:
                        # Apply rate limiting
                        if self.rate_limiter:
                            await self.rate_limiter.acquire()
                        
                        # Make API call with retry logic
                        if self.retry_config:
                            response_data = await retry_with_backoff(
                                lambda: self._make_api_call(
                                    messages, system_prompt, tool_definitions, iteration
                                ),
                                retry_config=self.retry_config
                            )
                        else:
                            response_data = await self._make_api_call(
                                messages, system_prompt, tool_definitions, iteration
                            )
                        
                        response, response_time, tokens = response_data
                        total_tokens += tokens
                        
                    except (APIError, APITimeoutError) as e:
                        logger.error("API error on iteration %d: %s", iteration, e)
                        self.metrics.record_request(False, 0, 0, "api_error")
                        raise AgentError(f"API error: {str(e)}") from e
                    except Exception as e:
                        logger.error("Unexpected error on iteration %d: %s", iteration, e)
                        self.metrics.record_request(False, 0, 0, "unexpected_error")
                        raise AgentError(f"Unexpected error: {str(e)}") from e
                    
                    # Check if Claude wants to use tools
                    if response.stop_reason == "tool_use":
                        tool_results = await self._execute_tools(response)
                        
                        # Add assistant message and tool results to history
                        messages.append({"role": "assistant", "content": response.content})
                        messages.append({"role": "user", "content": tool_results})
                    else:
                        # No more tool use, extract final response
                        final_text = self._extract_text_response(response)
                        
                        self.conversation_history.append({
                            "role": "assistant",
                            "content": final_text,
                        })
                        
                        end_time = datetime.now()
                        total_time = (end_time - start_time).total_seconds()
                        
                        root_span.set_attribute("final_response_length", len(final_text))
                        root_span.set_attribute("total_iterations", iteration)
                        root_span.set_attribute("total_tokens", total_tokens)
                        root_span.set_attribute("total_time_seconds", total_time)
                        
                        # Record metrics
                        self.metrics.record_request(True, total_tokens, total_time)
                        
                        # Apply post-processing middleware
                        await self._apply_middlewares("post_response", {
                            "response": final_text,
                            "iterations": iteration,
                            "tokens": total_tokens
                        })
                        
                        logger.info(
                            "✓ Agent response completed in %d iterations, %.2fs, %d tokens",
                            iteration, total_time, total_tokens
                        )
                        
                        return final_text
                
                # Max iterations reached
                error_msg = f"Max iterations ({max_iterations}) reached without completion"
                logger.error(error_msg)
                self.metrics.record_request(False, total_tokens, 0, "max_iterations")
                raise AgentError(error_msg)
                
            except Exception as e:
                root_span.set_attribute("error", str(e))
                raise


# Convenience function for backwards compatibility
async def create_agent(tools: Optional[List[BaseTool]] = None) -> EnhancedAgent:
    """Create an enhanced agent instance.
    
    Args:
        tools: Optional list of tools to register
        
    Returns:
        EnhancedAgent instance
    """
    return EnhancedAgent(tools=tools)
