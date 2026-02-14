"""Comprehensive test suite for Eden Agent."""

import pytest
import asyncio
from typing import List
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent.core import Agent, AgentError, ToolExecutionError
from src.agent.enhanced_core import EnhancedAgent, AgentConfig, AgentMetrics
from src.tools.calculator import CalculatorTool
from src.tools.data_validation import DataValidationTool
from src.tools.text_analysis import TextAnalysisTool
from src.tools.base import BaseTool, ToolDefinition


class MockTool(BaseTool):
    """Mock tool for testing."""
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="mock_tool",
            description="A mock tool for testing",
            input_schema={
                "type": "object",
                "properties": {
                    "action": {"type": "string"}
                },
                "required": ["action"]
            }
        )
    
    async def execute(self, action: str) -> str:
        if action == "error":
            raise Exception("Mock error")
        return f"Mock result: {action}"


@pytest.fixture
def agent():
    """Create a basic agent for testing."""
    return Agent(tools=[CalculatorTool()])


@pytest.fixture
def enhanced_agent():
    """Create an enhanced agent for testing."""
    config = AgentConfig(max_iterations=5)
    return EnhancedAgent(tools=[CalculatorTool(), MockTool()], config=config)


class TestAgentBasics:
    """Test basic agent functionality."""
    
    def test_agent_initialization(self, agent):
        """Test agent initializes correctly."""
        assert agent is not None
        assert len(agent._tools) == 1
        assert "calculator" in agent._tools
    
    def test_tool_registration(self, agent):
        """Test tool registration."""
        mock_tool = MockTool()
        agent.register_tool(mock_tool)
        
        assert "mock_tool" in agent._tools
        assert len(agent.list_tools()) == 2
    
    def test_tool_unregistration(self, agent):
        """Test tool unregistration."""
        result = agent.unregister_tool("calculator")
        assert result is True
        assert len(agent._tools) == 0
        
        result = agent.unregister_tool("nonexistent")
        assert result is False
    
    def test_list_tools(self, agent):
        """Test listing tools."""
        tools = agent.list_tools()
        assert isinstance(tools, list)
        assert "calculator" in tools
    
    def test_clear_history(self, agent):
        """Test clearing conversation history."""
        agent.conversation_history.append({"role": "user", "content": "test"})
        assert len(agent.conversation_history) > 0
        
        agent.clear_history()
        assert len(agent.conversation_history) == 0


class TestEnhancedAgent:
    """Test enhanced agent features."""
    
    def test_enhanced_initialization(self, enhanced_agent):
        """Test enhanced agent initializes correctly."""
        assert enhanced_agent is not None
        assert isinstance(enhanced_agent.config, AgentConfig)
        assert isinstance(enhanced_agent.metrics, AgentMetrics)
    
    def test_metrics_tracking(self, enhanced_agent):
        """Test metrics are tracked correctly."""
        metrics = enhanced_agent.metrics
        
        metrics.record_request(True, 100, 1.5)
        assert metrics.total_requests == 1
        assert metrics.successful_requests == 1
        assert metrics.total_tokens_used == 100
        
        metrics.record_request(False, 50, 0.5, "test_error")
        assert metrics.total_requests == 2
        assert metrics.failed_requests == 1
        assert "test_error" in metrics.error_count_by_type
    
    def test_tool_usage_tracking(self, enhanced_agent):
        """Test tool usage is tracked."""
        metrics = enhanced_agent.metrics
        
        metrics.record_tool_usage("calculator")
        metrics.record_tool_usage("calculator")
        metrics.record_tool_usage("mock_tool")
        
        assert metrics.total_tool_calls == 3
        assert metrics.tool_usage_stats["calculator"] == 2
        assert metrics.tool_usage_stats["mock_tool"] == 1
    
    def test_get_metrics_summary(self, enhanced_agent):
        """Test metrics summary generation."""
        metrics = enhanced_agent.metrics
        metrics.record_request(True, 100, 1.0)
        
        summary = metrics.get_summary()
        assert "total_requests" in summary
        assert "success_rate" in summary
        assert "total_tokens_used" in summary
        assert summary["total_requests"] == 1
    
    def test_tool_validation(self, enhanced_agent):
        """Test tool validation."""
        # Valid tool should register without error
        valid_tool = MockTool()
        enhanced_agent.register_tool(valid_tool)
        assert "mock_tool" in enhanced_agent._tools
    
    def test_get_tool_definitions(self, enhanced_agent):
        """Test getting tool definitions for display."""
        definitions = enhanced_agent.get_tool_definitions_for_display()
        assert isinstance(definitions, list)
        assert len(definitions) > 0
        assert "name" in definitions[0]
        assert "description" in definitions[0]


class TestTools:
    """Test tool implementations."""
    
    @pytest.mark.asyncio
    async def test_calculator_tool(self):
        """Test calculator tool."""
        calc = CalculatorTool()
        result = await calc.execute(expression="2 + 2")
        assert result == 4
    
    @pytest.mark.asyncio
    async def test_data_validation_tool_email(self):
        """Test data validation tool with email."""
        validator = DataValidationTool()
        
        # Valid email
        result = await validator.execute(
            validation_type="email",
            data="test@example.com"
        )
        assert result["valid"] is True
        
        # Invalid email
        result = await validator.execute(
            validation_type="email",
            data="invalid-email"
        )
        assert result["valid"] is False
    
    @pytest.mark.asyncio
    async def test_data_validation_tool_url(self):
        """Test data validation tool with URL."""
        validator = DataValidationTool()
        
        # Valid URL
        result = await validator.execute(
            validation_type="url",
            data="https://example.com"
        )
        assert result["valid"] is True
        
        # Invalid URL
        result = await validator.execute(
            validation_type="url",
            data="not-a-url"
        )
        assert result["valid"] is False
    
    @pytest.mark.asyncio
    async def test_text_analysis_tool_statistics(self):
        """Test text analysis tool statistics."""
        analyzer = TextAnalysisTool()
        
        text = "This is a test. This is only a test."
        result = await analyzer.execute(text=text, analysis_type="statistics")
        
        assert "statistics" in result
        stats = result["statistics"]
        assert stats["words"] > 0
        assert stats["sentences"] == 2
        assert "avg_word_length" in stats
    
    @pytest.mark.asyncio
    async def test_text_analysis_tool_sentiment(self):
        """Test text analysis tool sentiment."""
        analyzer = TextAnalysisTool()
        
        # Positive text
        result = await analyzer.execute(
            text="This is great and wonderful!",
            analysis_type="sentiment"
        )
        assert "sentiment" in result
        assert result["sentiment"]["sentiment"] in ["positive", "neutral"]
        
        # Negative text
        result = await analyzer.execute(
            text="This is terrible and awful.",
            analysis_type="sentiment"
        )
        assert result["sentiment"]["sentiment"] in ["negative", "neutral"]


class TestInputValidation:
    """Test input validation."""
    
    def test_empty_message_validation(self, agent):
        """Test empty message is rejected."""
        with pytest.raises(ValueError):
            asyncio.run(agent.chat(""))
    
    def test_whitespace_message_validation(self, agent):
        """Test whitespace-only message is rejected."""
        with pytest.raises(ValueError):
            asyncio.run(agent.chat("   "))
    
    def test_invalid_max_iterations(self, agent):
        """Test invalid max_iterations is rejected."""
        with pytest.raises(ValueError):
            asyncio.run(agent.chat("test", max_iterations=0))
        
        with pytest.raises(ValueError):
            asyncio.run(agent.chat("test", max_iterations=100))


class TestErrorHandling:
    """Test error handling."""
    
    @pytest.mark.asyncio
    async def test_tool_execution_error(self, enhanced_agent):
        """Test tool execution error handling."""
        # The mock tool raises an error when action="error"
        # In a real scenario, this would test actual tool execution errors
        pass  # This would need actual API calls to test properly


class TestContextManagement:
    """Test context window management."""
    
    def test_context_truncation(self, enhanced_agent):
        """Test conversation history is truncated."""
        # Add many messages
        for i in range(100):
            enhanced_agent.conversation_history.append({
                "role": "user",
                "content": f"Message {i}"
            })
        
        # Manage context
        managed = enhanced_agent._manage_context_window(
            enhanced_agent.conversation_history
        )
        
        # Should be truncated to max_history_messages
        assert len(managed) <= enhanced_agent.config.max_history_messages


def run_tests():
    """Run all tests."""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_tests()
