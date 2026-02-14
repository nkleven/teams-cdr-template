# Alpha Deployment - Mark Ramey Access

**Version**: v0.1.0-alpha  
**Date**: [Current Date]  
**Deployed To**: Mark Ramey  
**Purpose**: Initial testing and feedback

## 🚀 Quick Start for Mark

### 1. Access Repository

```bash
# Clone the repository
git clone https://github.com/nkleven/eden-source-c2.git
cd eden-source-c2

# Checkout alpha branch (if applicable)
git checkout alpha

# Or stay on main if alpha is merged
git checkout main
```

### 2. Environment Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### 3. Configure API Access

Create `.env` file with your credentials:

```env
# API Keys - Mark, use the shared test key for now
ANTHROPIC_API_KEY=sk-ant-test-xxxxx

# Rate Limiting - Conservative for alpha
RATE_LIMIT_ENABLED=true
RATE_LIMIT_MAX_CALLS=30
RATE_LIMIT_TIME_WINDOW=60.0

# Retry Logic
RETRY_ENABLED=true
RETRY_MAX_ATTEMPTS=3
RETRY_BASE_DELAY=1.0
RETRY_MAX_DELAY=60.0

# Logging - Verbose for alpha testing
LOG_LEVEL=DEBUG
```

### 4. Verify Installation

```bash
# Run the example script
python examples/advanced_features.py

# Expected output: Should demonstrate all 6 features
# 1. Basic chat
# 2. Custom tool registration
# 3. Tool management
# 4. Rate limiting demo
# 5. Retry logic demo
# 6. Configuration overview
```

## 🧪 Alpha Testing Focus Areas

### Priority 1: Core Functionality

- [ ] Agent initialization and basic chat
- [ ] Built-in tools working correctly
- [ ] Custom tool registration and execution
- [ ] Error handling and recovery

### Priority 2: Performance & Reliability

- [ ] Rate limiting prevents API throttling
- [ ] Retry logic handles transient failures
- [ ] Response times are acceptable
- [ ] Memory usage is reasonable

### Priority 3: Developer Experience

- [ ] API is intuitive and easy to use
- [ ] Error messages are clear and actionable
- [ ] Documentation is accurate and helpful
- [ ] Examples work as described

## 📝 Testing Checklist

### Basic Agent Tests

```python
# Test 1: Simple chat
from src.agent import Agent

agent = Agent()
response = await agent.chat("Hello, can you help me?")
print(response)
# Expected: Friendly response from Claude

# Test 2: Tool usage
response = await agent.chat("What tools do you have available?")
print(response)
# Expected: List of available tools

# Test 3: Custom tool
from src.tools.base import BaseTool, ToolDefinition

class TestTool(BaseTool):
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="test_tool",
            description="A test tool for alpha",
            input_schema={
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                },
                "required": ["message"]
            }
        )
    
    async def execute(self, message: str) -> str:
        return f"Test received: {message}"

agent.register_tool(TestTool())
response = await agent.chat("Use the test tool with message 'hello'")
# Expected: Tool should be called and return formatted message
```

### Edge Cases to Test

```python
# Test 4: Rate limiting
# Make rapid requests to trigger rate limiter
for i in range(60):
    response = await agent.chat(f"Quick message {i}")
# Expected: Should handle gracefully without API errors

# Test 5: Error recovery
# Force an error and verify retry logic
# (Implementation specific to your setup)

# Test 6: Tool errors
class BrokenTool(BaseTool):
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(name="broken", description="Broken tool", input_schema={})
    
    async def execute(self) -> str:
        raise ValueError("Intentional error")

agent.register_tool(BrokenTool())
# Expected: Agent should handle tool errors gracefully
```

## 🐛 Known Issues (Alpha)

Document any issues you encounter:

1. **Issue**: [Description]
   - **Severity**: Low | Medium | High | Critical
   - **Steps to Reproduce**:
   - **Expected Behavior**:
   - **Actual Behavior**:

## 📊 Feedback Template

### What's Working Well

-

### Pain Points

-

### Suggestions for Improvement

-

### Questions/Unclear Areas

-

### Performance Observations

- Response time:
- Memory usage:
- API call efficiency:

## 🔄 Alpha Testing Workflow

### Daily

1. Pull latest changes: `git pull origin main`
2. Test core functionality
3. Document any issues in GitHub Issues
4. Update feedback template

### When Issues Found

1. Check if issue is already documented
2. Create detailed bug report with:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Logs (if applicable)
3. Tag with `alpha-testing` label

### Communication

- **Slack/Email**: Quick questions and updates
- **GitHub Issues**: Bug reports and feature requests
- **Weekly Sync**: Detailed feedback session

## 📞 Support Contacts

- **Technical Issues**: [Your contact]
- **API Access**: [API admin contact]
- **General Questions**: [Team lead contact]

## 🎯 Next Steps After Alpha

Based on your feedback, we'll:

1. Address critical bugs
2. Improve documentation
3. Optimize performance
4. Plan beta release features

---

**Mark**: Start with the testing checklist above and document everything you find. Your feedback is crucial for improving the system before beta release! 🚀
