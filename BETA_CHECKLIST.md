# Beta Testing Checklist 🚀

## Eden Agent v0.1.0-beta.1

This document outlines the testing procedures and known limitations for beta testers.

## Pre-Testing Setup

### ✅ Environment Setup
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- [ ] Python 3.10 or higher installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed: `pip install -e ".[dev]"`
- [ ] `.env` file created from `.env.example`
- [ ] Valid `ANTHROPIC_API_KEY` configured

### ✅ Configuration Validation
<<<<<<<<< Temporary merge branch 1

Run the following to verify your setup:

=========
Run the following to verify your setup:
>>>>>>>>> Temporary merge branch 2
```bash
python -c "from src.config import settings; print('✓ Configuration valid')"
```

## Core Testing Areas

### 1. Agent Functionality ⚙️

#### Basic Chat
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- [ ] Agent initializes without errors
- [ ] Simple questions receive appropriate responses
- [ ] Multi-turn conversations work correctly
- [ ] Conversation history is maintained

**Test Commands:**
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
```python
from src.agent.core import Agent
import asyncio

agent = Agent()
response = await agent.chat("Hello, introduce yourself")
print(response)
```

#### Tool Execution
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- [ ] Calculator tool executes correctly
- [ ] Tool errors are handled gracefully
- [ ] Multiple tool calls in one conversation work
- [ ] Invalid tool inputs produce helpful error messages

**Test Commands:**
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
```bash
pytest tests/smoke_test.py::TestSmokeAgent -v
```

### 2. Safety & Content Filtering 🛡️

#### Input Safety
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- [ ] Safe inputs pass without issues
- [ ] Jailbreak attempts are detected and blocked
- [ ] Prompt injection attempts are flagged
- [ ] PII (emails, phone numbers) is detected

#### Output Safety
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- [ ] Short responses are flagged appropriately
- [ ] Normal responses pass safety checks
- [ ] URLs and code blocks are tracked in metadata

**Test Commands:**
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
```bash
pytest tests/smoke_test.py::TestSmokeSafety -v
```

**Manual Tests:**
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- Test with various user inputs including:
  - Normal questions
  - Inputs with email addresses
  - Inputs with phone numbers
  - Jailbreak attempts (e.g., "ignore previous instructions")

### 3. Monitoring & Metrics 📊

#### Metrics Collection
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- [ ] Interactions are recorded correctly
- [ ] Success/failure rates calculate accurately
- [ ] Tool usage is tracked
- [ ] Response times are captured

#### Report Generation
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- [ ] Reports generate without errors
- [ ] All metric categories are present
- [ ] JSON export works correctly

**Test Commands:**
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
```bash
pytest tests/smoke_test.py::TestSmokeMonitoring -v
```

### 4. Tracing & Observability 🔍

#### OpenTelemetry
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- [ ] Tracing initializes correctly
- [ ] Spans are created for operations
- [ ] Attributes are set properly
- [ ] No tracing errors in logs

**Test Commands:**
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
```bash
pytest tests/smoke_test.py::TestSmokeTracing -v
```

### 5. Integration Tests 🔗

#### End-to-End Workflows
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- [ ] Safe workflow completes successfully
- [ ] Blocked content workflow behaves correctly
- [ ] Multiple agent instances work independently
- [ ] Memory usage stays reasonable during long sessions

**Test Commands:**
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
```bash
pytest tests/smoke_test.py::TestSmokeIntegration -v
```

### 6. Error Handling 🚨

#### Configuration Errors
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- [ ] Missing API key produces clear error message
- [ ] Invalid model name produces warning
- [ ] Out-of-range parameters are validated

#### Runtime Errors
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- [ ] API timeouts are handled gracefully
- [ ] API errors produce user-friendly messages
- [ ] Tool execution failures don't crash the agent
- [ ] Max iterations reached produces clear message

**Manual Tests:**
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
```bash
# Test with invalid API key
ANTHROPIC_API_KEY=invalid pytest tests/smoke_test.py::TestSmokeAgent::test_imports -v

# Test with missing .env file
mv .env .env.backup
python -c "from src.config import settings"
mv .env.backup .env
```

## Performance Testing

### Response Times ⏱️
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- [ ] First response < 5 seconds (simple query)
- [ ] Tool execution < 3 seconds (calculator)
- [ ] Multi-turn conversation < 10 seconds (3 turns)

### Resource Usage 💻
<<<<<<<<< Temporary merge branch 1

=========
>>>>>>>>> Temporary merge branch 2
- [ ] Memory usage < 500MB for typical session
- [ ] No memory leaks during extended use
- [ ] CPU usage reasonable during idle time

## Known Limitations ⚠️

### Current Beta Limitations
<<<<<<<<< Temporary merge branch 1

1. ~~**Rate Limiting**: No built-in rate limiting yet~~ ✅ RESOLVED
2. ~~**Retry Logic**: Limited retry logic for transient API failures~~ ✅ RESOLVED
3. **Async Only**: Agent chat requires async/await
4. ~~**Single User**: No multi-user session management~~ ✅ RESOLVED
5. **Tool System**: Expanding built-in tools (calculator, datetime, text, web, json, file)
6. **Tracing**: Console exporter only (Jaeger/OTLP experimental)

### Known Issues

=========
1. **Rate Limiting**: No built-in rate limiting yet - may hit API limits
2. **Retry Logic**: Limited retry logic for transient API failures
3. **Async Only**: Agent chat requires async/await
4. **Single User**: No multi-user session management
5. **Tool System**: Limited to built-in tools (calculator only)
6. **Tracing**: Console exporter only (Jaeger/OTLP experimental)

### Known Issues
>>>>>>>>> Temporary merge branch 2
- **OpenTelemetry Warning**: Console exporter may show "closed file" warning during shutdown (non-critical)
- **Long Responses**: Responses >4096 tokens may be truncated
- **Tool Loops**: Max 10 iterations to prevent infinite loops

<<<<<<<<< Temporary merge branch 1
### Recently Implemented ✅

- [x] API rate limiting and backoff
- [x] Advanced retry strategies (exponential backoff)
- [x] Custom tool registration API
- [x] Multi-user session management
- [x] Production-grade health checks

### Not Yet Implemented

- [ ] Enhanced metrics dashboard with advanced charts
- [ ] Real-time monitoring UI improvements
- [ ] Additional built-in tools (beyond calculator)
=========
### Not Yet Implemented
- [ ] API rate limiting and backoff
- [ ] Advanced retry strategies
- [ ] Custom tool registration API
- [ ] Multi-user session management
- [ ] Production-grade health checks
- [ ] Metrics dashboard
- [ ] Real-time monitoring UI
>>>>>>>>> Temporary merge branch 2

## Reporting Issues 🐛

When reporting issues, please include:

1. **Environment Information:**
   - Python version
   - Operating system
   - Installed package versions: `pip freeze`

2. **Configuration:**
   - Sanitized `.env` contents (remove API keys!)
   - Model and parameters used

3. **Error Details:**
   - Full error message and stack trace
   - Steps to reproduce
   - Expected vs actual behavior

4. **Logs:**
   - Run with `LOG_LEVEL=DEBUG`
   - Include relevant log output

## Success Criteria ✨

For beta to be considered successful:

- [ ] All smoke tests pass: `pytest tests/smoke_test.py -v`
- [ ] No critical errors in typical usage
- [ ] Error messages are clear and actionable
- [ ] Documentation is clear and complete
- [ ] Performance meets stated targets

## Feedback 💬

Please provide feedback on:

1. **Ease of Setup**: Was it easy to get started?
2. **Documentation**: Was anything unclear or missing?
3. **Error Messages**: Were errors helpful?
4. **Performance**: Did it meet your expectations?
5. **Features**: What features would you like to see?
6. **Use Cases**: What are you using Eden Agent for?

---

**Version**: 0.1.0-beta.1  
**Last Updated**: 2025-12-24  
**Status**: Active Beta Testing

Thank you for participating in the beta! 🎉
