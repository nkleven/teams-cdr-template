# Quick Start Guide - Enhanced Eden Agent

## 🚀 Getting Started in 5 Minutes

### 1. Install Dependencies

```bash
pip install anthropic python-dotenv opentelemetry-api opentelemetry-sdk aiohttp fastapi uvicorn websockets pytest pytest-asyncio
```

### 2. Set Up Environment

Create `.env` file:
```env
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Run Your First Enhanced Agent

```python
import asyncio
from src.agent.enhanced_core import EnhancedAgent
from src.tools.calculator import CalculatorTool

async def main():
    agent = EnhancedAgent(tools=[CalculatorTool()])
    
    async with agent:
        response = await agent.chat("What is 123 * 456?")
        print(response)
        
        # Get metrics
        print(agent.get_metrics())

asyncio.run(main())
```

### 4. Run the Demo

```bash
python examples/demo_enhanced_features.py
```

### 5. Start the Dashboard

```bash
python src/dashboard/enhanced_server.py
```

Then open: http://localhost:8000

### 6. Run Tests

```bash
pytest tests/test_comprehensive.py -v
```

## 📋 What's New?

### Enhanced Agent Features
- ✅ Advanced context management
- ✅ Real-time metrics tracking
- ✅ Tool execution timeout
- ✅ Parallel tool execution
- ✅ Middleware system
- ✅ Better error handling

### New Tools
- ✅ Data Validation (email, URL, phone, JSON, credit card)
- ✅ Text Analysis (statistics, sentiment, readability, keywords)
- ✅ API Client (HTTP requests to external services)

### Evaluation Framework
- ✅ Tool accuracy evaluation
- ✅ Output quality metrics
- ✅ Response time tracking
- ✅ Safety checks
- ✅ Detailed JSON reports

### Dashboard
- ✅ Real-time WebSocket updates
- ✅ Beautiful modern UI
- ✅ Metrics visualization
- ✅ Tool usage tracking
- ✅ Performance monitoring

### Testing
- ✅ Comprehensive test suite
- ✅ Agent functionality tests
- ✅ Tool validation tests
- ✅ Error handling tests
- ✅ Context management tests

## 🎯 Common Use Cases

### Use Case 1: Agent with Multiple Tools

```python
from src.agent.enhanced_core import EnhancedAgent, AgentConfig
from src.tools.calculator import CalculatorTool
from src.tools.data_validation import DataValidationTool
from src.tools.text_analysis import TextAnalysisTool

config = AgentConfig(max_iterations=20)
agent = EnhancedAgent(
    tools=[
        CalculatorTool(),
        DataValidationTool(),
        TextAnalysisTool()
    ],
    config=config
)

# Agent can now handle math, validation, and text analysis!
```

### Use Case 2: Production Monitoring

```python
import aiohttp

async def report_metrics(metrics):
    async with aiohttp.ClientSession() as session:
        await session.post(
            "http://localhost:8000/api/metrics",
            json=metrics
        )

# After each agent call
metrics = agent.get_metrics()
await report_metrics(metrics)
```

### Use Case 3: Automated Testing

```python
from evaluation.enhanced_evaluation import EnhancedEvaluationFramework

framework = EnhancedEvaluationFramework(agent)
report = await framework.run_evaluation(
    test_file=Path("tests/test_cases.json"),
    output_dir=Path("results/")
)
print(f"Pass rate: {report.summary['pass_rate']}%")
```

## 📚 File Organization

```
New Files Created:
├── src/agent/enhanced_core.py          # Enhanced agent implementation
├── src/tools/data_validation.py        # Data validation tool
├── src/tools/text_analysis.py          # Text analysis tool
├── src/tools/api_client.py             # API client tool
├── src/dashboard/enhanced_server.py    # Real-time dashboard
├── evaluation/enhanced_evaluation.py   # Evaluation framework
├── tests/test_comprehensive.py         # Complete test suite
├── examples/demo_enhanced_features.py  # Feature demonstrations
├── README_ENHANCEMENTS.md              # Full documentation
└── QUICK_START.md                      # This file
```

## 💡 Tips

1. **Use context manager** for automatic metrics reporting:
   ```python
   async with agent:
       response = await agent.chat(message)
   # Metrics automatically printed on exit
   ```

2. **Configure for your needs**:
   ```python
   config = AgentConfig(
       max_iterations=15,           # Increase for complex tasks
       tool_timeout_seconds=30.0,   # Adjust for slow APIs
       max_history_messages=100     # More context = more tokens
   )
   ```

3. **Monitor in real-time**: Keep dashboard open while testing

4. **Run tests frequently**: `pytest tests/test_comprehensive.py -v`

5. **Check metrics**: `agent.get_metrics()` after operations

## 🐛 Troubleshooting

### Agent not responding?
- Check API key in `.env`
- Verify internet connection
- Check rate limits

### Dashboard not loading?
- Ensure port 8000 is free
- Run: `python src/dashboard/enhanced_server.py`
- Visit: http://localhost:8000

### Tests failing?
- Install pytest: `pip install pytest pytest-asyncio`
- Check dependencies: `pip install -r requirements.txt`

### Import errors?
- Ensure you're in project root
- Check Python path

## 🎓 Next Steps

1. ✅ Read [README_ENHANCEMENTS.md](README_ENHANCEMENTS.md) for full details
2. ✅ Explore [examples/demo_enhanced_features.py](examples/demo_enhanced_features.py)
3. ✅ Create your own custom tools
4. ✅ Set up continuous evaluation
5. ✅ Deploy to production with monitoring

## 📞 Support

- Check existing documentation files
- Review example code
- Run demo script
- Check test cases for usage patterns

---

**🎉 You're ready to build production-grade AI agents!**
