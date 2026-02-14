# Eden Agent - Developer Onboarding

Welcome to the Eden Agent project! This guide will help you get up to speed quickly.

## 👋 Welcome, Mark Ramey!

This document will walk you through everything you need to know to start contributing to the Eden Agent codebase.

## 🎯 Project Overview

Eden Agent is an AI-powered agent system built with:
- **Claude API** for natural language processing
- **Custom Tool System** for extensible functionality
- **FastAPI** for API endpoints (if applicable)
- **Python 3.11+** as the core language

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone the repository (if not already done)
git clone https://github.com/nkleven/eden-source-c2.git
cd eden-source-c2

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### 2. Configuration

Create a `.env` file in the root directory:

```env
# API Keys
ANTHROPIC_API_KEY=your_api_key_here

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_MAX_CALLS=50
RATE_LIMIT_TIME_WINDOW=60.0

# Retry Logic
RETRY_ENABLED=true
RETRY_MAX_ATTEMPTS=3
RETRY_BASE_DELAY=1.0
RETRY_MAX_DELAY=60.0

# Logging
LOG_LEVEL=INFO
```

### 3. Verify Installation

```bash
# Run the example script
python examples/advanced_features.py

# Run tests (if available)
pytest tests/
```

## 📁 Project Structure

```
eden-source-c2/
├── src/
│   ├── agent.py           # Core agent implementation
│   ├── tools/             # Tool implementations
│   │   ├── base.py       # Base tool interface
│   │   └── ...           # Specific tools
│   ├── config.py         # Configuration management
│   └── utils/            # Utility functions
├── examples/
│   └── advanced_features.py  # Usage examples
├── tests/                # Test suite
├── docs/                 # Documentation
└── .env                  # Environment variables (not in git)
```

## 🔧 Core Concepts

### Agent Architecture

The agent uses a tool-based architecture:

1. **Agent**: Orchestrates interactions with Claude API
2. **Tools**: Modular capabilities that extend agent functionality
3. **Rate Limiter**: Prevents API throttling
4. **Retry Logic**: Handles transient failures

### Creating Custom Tools

All tools inherit from `BaseTool`:

```python
from src.tools.base import BaseTool, ToolDefinition

class MyTool(BaseTool):
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="my_tool",
            description="What the tool does",
            input_schema={
                "type": "object",
                "properties": {
                    "param": {"type": "string"}
                },
                "required": ["param"]
            }
        )
    
    async def execute(self, param: str) -> str:
        # Implementation
        return f"Processed: {param}"
```

### Agent Usage Pattern

```python
from src.agent import Agent

# Initialize
agent = Agent()

# Register custom tools
agent.register_tool(MyTool())

# Chat with agent
response = await agent.chat("Your message here")
```

## 🛠️ Development Workflow

### 1. Branch Strategy

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Description of changes"

# Push and create PR
git push origin feature/your-feature-name
```

### 2. Code Standards

- **Type Hints**: Use type annotations for all functions
- **Async/Await**: Use async for I/O operations
- **Error Handling**: Raise `AgentError` for agent-specific errors
- **Documentation**: Add docstrings to all public methods

Example:

```python
async def my_function(param: str) -> dict[str, Any]:
    """
    Brief description.
    
    Args:
        param: Description of parameter
        
    Returns:
        Dictionary containing results
        
    Raises:
        AgentError: When operation fails
    """
    try:
        # Implementation
        return {"result": param}
    except Exception as e:
        raise AgentError(f"Operation failed: {e}") from e
```

### 3. Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_agent.py
```

## 📚 Key Resources

### Internal Documentation
- [Examples README](../examples/README.md) - Usage examples and patterns
- [API Documentation](./API.md) - API reference (if exists)

### External Resources
- [Anthropic Claude API Docs](https://docs.anthropic.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## 🎓 Learning Path

### Week 1: Foundation
- [ ] Set up development environment
- [ ] Run and understand `advanced_features.py`
- [ ] Read through core agent implementation
- [ ] Create a simple custom tool

### Week 2: Deep Dive
- [ ] Understand rate limiting and retry mechanisms
- [ ] Review existing tools in `src/tools/`
- [ ] Write tests for a new feature
- [ ] Submit first PR

### Week 3: Contribution
- [ ] Pick up a feature ticket
- [ ] Implement and test thoroughly
- [ ] Document your changes
- [ ] Review other team members' PRs

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ImportError: No module named 'src'`
```bash
# Solution: Reinstall in editable mode
pip install -e .
```

**Issue**: Rate limit errors
```bash
# Solution: Adjust rate limit settings in .env
RATE_LIMIT_MAX_CALLS=30
RATE_LIMIT_TIME_WINDOW=60.0
```

**Issue**: API authentication failed
```bash
# Solution: Verify your API key in .env
echo $ANTHROPIC_API_KEY  # Check it's set correctly
```

## 💬 Getting Help

- **Code Questions**: Review `examples/` directory first
- **Architecture Questions**: Check `docs/` folder
- **Bugs**: Check existing issues or create new one
- **General Help**: Reach out to the team

## 🎯 First Tasks

Here are some good starter tasks for Mark:

1. **Familiarization**: Run `advanced_features.py` and understand each feature
2. **Custom Tool**: Create a simple custom tool (e.g., weather lookup, calculator)
3. **Documentation**: Add missing docstrings to any functions you encounter
4. **Testing**: Write a test for an existing feature
5. **Feature**: Pick a small enhancement from the backlog

## 📋 Checklist

- [ ] Development environment set up
- [ ] `.env` file configured
- [ ] Able to run examples successfully
- [ ] Read through core agent code
- [ ] Created first custom tool
- [ ] Ran test suite
- [ ] First PR submitted

---

Welcome aboard! Looking forward to your contributions to Eden Agent! 🚀
