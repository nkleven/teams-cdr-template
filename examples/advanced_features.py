"""Examples demonstrating advanced features."""

import asyncio
from src.agent.core import Agent
from src.tools.calculator import CalculatorTool
from src.tools.base import BaseTool, ToolDefinition


class WeatherTool(BaseTool):
    """Custom weather tool example."""
    
    @property
    def definition(self) -> ToolDefinition:
        """Return tool definition."""
        return ToolDefinition(
            name="get_weather",
            description="Get current weather for a location",
            input_schema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or location"
                    }
                },
                "required": ["location"]
            }
        )
    
    async def execute(self, location: str) -> str:
        """Execute the weather tool."""
        # Simulated weather data
        weather_data = {
            "san francisco": "Sunny, 72°F",
            "new york": "Cloudy, 65°F",
            "london": "Rainy, 58°F",
            "tokyo": "Clear, 75°F",
        }
        
        result = weather_data.get(
            location.lower(),
            "Weather data not available"
        )
        return f"Weather in {location}: {result}"


async def example_basic_usage():
    """Basic agent usage with built-in tools."""
    print("\n=== Example 1: Basic Agent Usage ===")
    
    agent = Agent(tools=[CalculatorTool()])
    response = await agent.chat("What is 25 times 4?")
    print(f"Response: {response}")


async def example_custom_tool():
    """Using custom tools with the agent."""
    print("\n=== Example 2: Custom Tool Registration ===")
    
    # Create agent with calculator
    agent = Agent(tools=[CalculatorTool()])
    
    # Register a custom weather tool
    weather_tool = WeatherTool()
    agent.register_tool(weather_tool)
    
    # List all registered tools
    print(f"Registered tools: {agent.list_tools()}")
    
    # Use the custom tool
    response = await agent.chat("What's the weather in San Francisco?")
    print(f"Response: {response}")


async def example_tool_management():
    """Demonstrate tool registration and unregistration."""
    print("\n=== Example 3: Tool Management ===")
    
    agent = Agent()
    
    # Register multiple tools
    agent.register_tool(CalculatorTool())
    agent.register_tool(WeatherTool())
    print(f"After registration: {agent.list_tools()}")
    
    # Unregister a tool
    agent.unregister_tool("get_weather")
    print(f"After unregistration: {agent.list_tools()}")
    
    # Try to unregister non-existent tool
    success = agent.unregister_tool("nonexistent_tool")
    print(f"Unregister nonexistent: {success}")


async def example_rate_limiting():
    """Demonstrate rate limiting in action."""
    print("\n=== Example 4: Rate Limiting ===")
    print("Rate limiting is automatically applied to all API calls.")
    print("Check settings in .env:")
    print("- RATE_LIMIT_ENABLED=true")
    print("- RATE_LIMIT_MAX_CALLS=50")
    print("- RATE_LIMIT_TIME_WINDOW=60.0")
    
    agent = Agent(tools=[CalculatorTool()])
    
    # Make multiple requests - rate limiter will control the pace
    for i in range(3):
        response = await agent.chat(f"Calculate {i} + 1")
        print(f"Request {i+1}: {response[:50]}...")


async def example_retry_logic():
    """Demonstrate retry logic for API failures."""
    print("\n=== Example 5: Retry Logic ===")
    print("Retry logic is automatically applied to API calls.")
    print("Check settings in .env:")
    print("- RETRY_ENABLED=true")
    print("- RETRY_MAX_ATTEMPTS=3")
    print("- RETRY_BASE_DELAY=1.0")
    print("- RETRY_MAX_DELAY=60.0")
    
    # The retry logic will automatically handle transient failures
    # with exponential backoff
    agent = Agent()
    response = await agent.chat("Hello, how are you?")
    print(f"Response: {response}")


async def example_configuration():
    """Show current configuration."""
    print("\n=== Example 6: Configuration Overview ===")
    
    from src.config import settings
    
    print(f"Model: {settings.model_name}")
    print(f"Max Tokens: {settings.max_tokens}")
    print(f"Temperature: {settings.temperature}")
    print("\nRate Limiting:")
    print(f"  Enabled: {settings.rate_limit_enabled}")
    if settings.rate_limit_enabled:
        print(f"  Max Calls: {settings.rate_limit_max_calls}")
        print(f"  Time Window: {settings.rate_limit_time_window}s")
    print("\nRetry Logic:")
    print(f"  Enabled: {settings.retry_enabled}")
    if settings.retry_enabled:
        print(f"  Max Attempts: {settings.retry_max_attempts}")
        print(f"  Base Delay: {settings.retry_base_delay}s")


async def main():
    """Run all examples."""
    print("=" * 60)
    print("Eden Agent - Advanced Features Examples")
    print("=" * 60)
    
    # Configuration overview
    await example_configuration()
    
    # Basic usage
    await example_basic_usage()
    
    # Custom tool
    await example_custom_tool()
    
    # Tool management
    await example_tool_management()
    
    # Rate limiting
    await example_rate_limiting()
    
    # Retry logic
    await example_retry_logic()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
