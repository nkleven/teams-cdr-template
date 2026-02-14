"""Core AI agent implementation using Claude."""

import logging
from typing import Dict, List, Optional, Any

from anthropic import Anthropic, APIError, APITimeoutError  # type: ignore[import-not-found]
from anthropic.types import TextBlock, ToolUseBlock  # type: ignore[import-not-found]

from ..config import settings
from ..tools.base import BaseTool
from ..tracing.tracer import tracer
from ..rate_limit import RateLimiter, RetryConfig, retry_with_backoff


# Type aliases for clarity
Message = Dict[str, Any]
ToolResult = Dict[str, Any]

# Constants
DEFAULT_SYSTEM_PROMPT = "You are a helpful AI assistant."
DEFAULT_MAX_ITERATIONS = 10

logger = logging.getLogger("eden_agent.agent")


class AgentError(Exception):
    """Base exception for agent errors."""


class ToolExecutionError(AgentError):
    """Exception raised when tool execution fails."""


class Agent:
    """AI Agent with tool calling capabilities and error handling.
    
    Features:
    - Tool registration and execution
    - Rate limiting support
    - Automatic retry with exponential backoff
    - OpenTelemetry tracing integration
    - Conversation history management
    
    Example:
        >>> agent = Agent(tools=[calculator_tool])
        >>> response = await agent.chat("What is 2+2?")
    """
    
    def __init__(self, tools: Optional[List[BaseTool]] = None):
        """Initialize the agent.
        
        Args:
            tools: Optional list of tools to register with the agent
            
        Raises:
            AgentError: If Anthropic client initialization fails
        """
        try:
            self.client = Anthropic(api_key=settings.anthropic_api_key)
            logger.info("✓ Agent initialized successfully")
        except Exception as e:
            logger.error("✗ Failed to initialize Anthropic client: %s", e)
            raise AgentError(f"Failed to initialize agent: {e}") from e
            
        # Use dict for O(1) tool lookup
        self._tools: Dict[str, BaseTool] = {}
        if tools:
            for tool in tools:
                self._tools[tool.definition.name] = tool
                
        self.conversation_history: List[Message] = []
        
        # Initialize rate limiter if enabled
        self.rate_limiter: Optional[RateLimiter] = None
        if settings.rate_limit_enabled:
            self.rate_limiter = RateLimiter(
                max_calls=settings.rate_limit_max_calls,
                time_window=settings.rate_limit_time_window
            )
            logger.info(
                "✓ Rate limiting enabled: %d calls per %.0f seconds",
                settings.rate_limit_max_calls,
                settings.rate_limit_time_window
            )
        
        # Initialize retry config if enabled
        self.retry_config: Optional[RetryConfig] = None
        if settings.retry_enabled:
            self.retry_config = RetryConfig(
                max_retries=settings.retry_max_attempts,
                base_delay=settings.retry_base_delay,
                max_delay=settings.retry_max_delay
            )
            logger.info(
                "✓ Retry logic enabled: max %d attempts",
                settings.retry_max_attempts
            )
        
        logger.debug("Agent initialized with %d tools", len(self._tools))
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        # Cleanup if needed in future
        pass
    
    def register_tool(self, tool: BaseTool) -> None:
        """Register a new tool with the agent.
        
        Args:
            tool: Tool instance to register
        """
        tool_name = tool.definition.name
        if tool_name in self._tools:
            logger.warning("Tool '%s' already registered, replacing", tool_name)
        self._tools[tool_name] = tool
        logger.info("✓ Tool '%s' registered", tool_name)
    
    def unregister_tool(self, tool_name: str) -> bool:
        """Unregister a tool by name.
        
        Args:
            tool_name: Name of the tool to unregister
            
        Returns:
            True if tool was found and removed, False otherwise
        """
        if tool_name in self._tools:
            del self._tools[tool_name]
            logger.info("✓ Tool '%s' unregistered", tool_name)
            return True
        logger.warning("Tool '%s' not found", tool_name)
        return False
    
    def list_tools(self) -> List[str]:
        """List all registered tool names.
        
        Returns:
            List of tool names
        """
        return list(self._tools.keys())
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history.clear()
        logger.info("✓ Conversation history cleared")
    
    def _get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get tool definitions for Claude API.
        
        Returns:
            List of tool definition dictionaries
        """
        return [tool.definition.model_dump() for tool in self._tools.values()]
    
    def _find_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Find a tool by name.
        
        Args:
            tool_name: Name of the tool to find
            
        Returns:
            Tool instance or None if not found
        """
        return self._tools.get(tool_name)
    
    def _validate_chat_input(
        self,
        user_message: str,
        max_iterations: int
    ) -> None:
        """Validate chat method inputs.
        
        Args:
            user_message: User's message
            max_iterations: Maximum iterations
            
        Raises:
            AgentError: If validation fails
        """
        if not user_message or not user_message.strip():
            raise AgentError("User message cannot be empty")
        if max_iterations < 1:
            raise AgentError("max_iterations must be at least 1")
    
    async def _execute_single_tool(self, block: ToolUseBlock) -> ToolResult:
        """Execute a single tool and return result.
        
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
                result = await tool.execute(**block.input)
                tool_span.set_attribute("result_type", type(result).__name__)
                logger.debug("Tool '%s' executed successfully", block.name)
                return {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                }
        except Exception as e:
            logger.error("Tool execution failed for '%s': %s", block.name, e)
            raise ToolExecutionError(
                f"Tool '{block.name}' failed: {str(e)}"
            ) from e
    
    async def _execute_tools(self, response) -> List[ToolResult]:
        """Execute all tools from Claude's response.
        
        Args:
            response: Claude API response containing tool use blocks
            
        Returns:
            List of tool result dictionaries
        """
        tool_results = []
        for block in response.content:
            if isinstance(block, ToolUseBlock):
                try:
                    result = await self._execute_single_tool(block)
                    tool_results.append(result)
                except ToolExecutionError:
                    # Re-raise tool execution errors
                    raise
                except Exception as e:
                    # Catch unexpected errors
                    logger.error("Unexpected error executing tool: %s", e)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": f"Error executing tool: {str(e)}",
                        "is_error": True,
                    })
        return tool_results
    
    def _extract_text_response(self, response) -> str:
        """Extract text content from Claude's response.
        
        Args:
            response: Claude API response
            
        Returns:
            Concatenated text from all TextBlocks
        """
        return "".join(
            block.text for block in response.content
            if isinstance(block, TextBlock)
        )
    
    async def _make_api_call(
        self,
        messages: List[Message],
        system_prompt: str,
        tool_definitions: List[Dict[str, Any]],
        iteration: int
    ):
        """Make a single API call to Claude.
        
        Args:
            messages: Conversation messages
            system_prompt: System prompt
            tool_definitions: Tool definitions
            iteration: Current iteration number
            
        Returns:
            Claude API response
        """
        with tracer.trace_operation(
            "claude_api_call",
            attributes={
                "model": settings.model_name,
                "temperature": settings.temperature,
                "max_tokens": settings.max_tokens,
                "message_count": len(messages),
                "iteration": iteration,
            },
        ) as api_span:
            result = self.client.messages.create(
                model=settings.model_name,
                max_tokens=settings.max_tokens,
                temperature=settings.temperature,
                system=system_prompt,
                messages=messages,
                tools=tool_definitions or None,
            )
            api_span.set_attribute("stop_reason", result.stop_reason or "unknown")
            api_span.set_attribute("content_block_count", len(result.content))
            return result
    
    async def chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
    ) -> str:
        """Chat with the agent using Claude AI.
        
        The agent handles tool execution, rate limiting, retries, and tracing
        automatically. Conversation history is maintained across calls.
        
        Args:
            user_message: User's input message
            system_prompt: Optional system prompt override (defaults to helpful assistant)
            max_iterations: Maximum tool use iterations to prevent loops (default: 10)
            
        Returns:
            Agent's final text response
            
        Raises:
            AgentError: If agent encounters an unrecoverable error or max iterations reached
            ToolExecutionError: If tool execution fails critically
        """
        # Validate inputs
        self._validate_chat_input(user_message, max_iterations)
        
        system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        
        with tracer.trace_operation(
            "agent_chat",
            attributes={
                "user_message_length": len(user_message),
                "tool_count": len(self._tools),
                "max_iterations": max_iterations,
            },
        ) as root_span:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message,
            })

            messages = self.conversation_history.copy()
            tool_definitions = self._get_tool_definitions()
            root_span.set_attribute("tool_definitions_count", len(tool_definitions))
            
            iteration = 0

            while iteration < max_iterations:
                iteration += 1
                logger.debug("Chat iteration %d/%d", iteration, max_iterations)
                
                try:
                    # Apply rate limiting if enabled
                    if self.rate_limiter:
                        await self.rate_limiter.acquire()
                    
                    # Call Claude with retry logic if enabled
                    if self.retry_config:
                        response = await retry_with_backoff(
                            lambda: self._make_api_call(
                                messages, system_prompt, tool_definitions, iteration
                            ),
                            retry_config=self.retry_config,
                            retry_on=(APIError, APITimeoutError)
                        )
                    else:
                        response = await self._make_api_call(
                            messages, system_prompt, tool_definitions, iteration
                        )
                        
                except APITimeoutError as e:
                    logger.error("API timeout on iteration %d: %s", iteration, e)
                    raise AgentError("Request timed out. Please try again.") from e
                    
                except APIError as e:
                    logger.error("API error on iteration %d: %s", iteration, e)
                    raise AgentError(f"API error occurred: {e.message}") from e
                    
                except Exception as e:
                    logger.error(
                        "Unexpected error on iteration %d: %s",
                        iteration,
                        e,
                        exc_info=True
                    )
                    raise AgentError(
                        f"Unexpected error: {str(e)}"
                    ) from e
                
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
                    root_span.set_attribute("final_response_length", len(final_text))
                    root_span.set_attribute("total_iterations", iteration)
                    
                    logger.info(
                        "Chat completed in %d iterations, response length: %d",
                        iteration,
                        len(final_text)
                    )
                    
                    return final_text
            
            # Max iterations reached
            logger.warning(
                "Max iterations (%d) reached without completion",
                max_iterations
            )
            raise AgentError(
                f"Maximum iterations ({max_iterations}) reached. "
                "The agent may be stuck in a loop."
            )
