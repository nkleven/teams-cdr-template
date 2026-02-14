# Eden Agent - Beta Tester Welcome! 🎉

Thank you for joining the Eden Agent beta testing program!

## What You Should Know

### Current Version

**v0.1.0-beta.1** - Initial public beta release

### Beta Testing Timeline

- **Start Date:** December 24, 2025
- **Expected Duration:** 4-6 weeks
- **Target Release:** v1.0.0 (Q1 2026)

## Getting Started

### 1. Set Up Your Environment

```bash
# Clone the repository
git clone https://github.com/nkleven/eden-source-c2.git
cd eden-source-c2

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Configure your environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 2. Verify Installation

```bash
# Run smoke tests
pytest tests/smoke_test.py -v

# Check health
python -c "from src.health import health_checker; print(health_checker.perform_health_check().to_dict())"
```

### 3. Review Documentation

- Read [README.md](README.md) for features and usage
- Review [BETA_CHECKLIST.md](BETA_CHECKLIST.md) for testing procedures
- Check configuration options in [.env.example](.env.example)

## What We Need From You

### Priority Areas for Testing

1. **Core Functionality (High Priority)**
   - Agent chat and conversation flow
   - Tool execution (especially calculator)
   - Error handling with invalid inputs
   - Multi-turn conversations

2. **Safety & Content Filtering (High Priority)**
   - PII detection accuracy
   - Jailbreak attempt detection
   - False positive rates
   - Edge cases in content filtering

3. **Performance (Medium Priority)**
   - Response times under various loads
   - Memory usage during extended sessions
   - Token consumption tracking
   - Concurrent request handling

4. **Usability (Medium Priority)**
   - Setup and configuration experience
   - Error message clarity
   - Documentation completeness
   - API ergonomics

5. **Integration (Low Priority)**
   - OpenTelemetry tracing output
   - Custom tool development
   - Metrics export
   - Logging configuration

### Reporting Issues

**Create a GitHub Issue with:**

- Clear title describing the issue
- Steps to reproduce
- Expected vs actual behavior
- Your environment details (OS, Python version)
- Relevant logs (set `LOG_LEVEL=DEBUG`)
- Label: `beta-feedback`

**Example Issue Title:**

- "Safety filter false positive on email addresses"
- "Agent crashes with tool execution error"
- "Documentation unclear on custom tool registration"

## Communication Channels

- **GitHub Issues:** Bug reports and feature requests
- **Discussions:** General questions and community support
- **Direct:** For sensitive security issues, email <nkleven@github.com>

## Beta Tester Benefits

### Recognition

- Beta testers credited in release notes
- Contributors list in README
- Special "Beta Tester" badge (coming soon)

### Early Access

- First to receive v0.2.0 beta
- Input on feature prioritization
- Direct access to development team

### Rewards (for top contributors)

- Free API credits (if applicable)
- Lifetime pro features (future)
- Exclusive swag (possibly)

## Known Limitations

Please review [BETA_CHECKLIST.md](BETA_CHECKLIST.md) for the complete list of known limitations.

**Key limitations:**

- No built-in rate limiting (you may hit API limits)
- Limited retry logic for transient failures
- Console-only tracing exporter
- Single-user sessions only
- Calculator is the only built-in tool

## FAQs

**Q: Do I need to pay for API access?**
A: You need your own Anthropic API key. Standard API rates apply.

**Q: Can I use this in production?**
A: Not yet! This is beta software for testing only.

**Q: How do I add custom tools?**
A: See the "Adding New Tools" section in README.md. API may change in v0.2.0.

**Q: The tests are failing, what do I do?**
A: Check that your .env file is configured properly, especially ANTHROPIC_API_KEY. If issues persist, create a GitHub issue.

**Q: Can I deploy this to the cloud?**
A: Yes, but it's not officially supported yet. Cloud deployment templates planned for v0.2.0.

## Feedback Survey

After testing, please complete our feedback survey (link coming soon) to help us improve Eden Agent!

## Thank You! 🙏

Your participation is invaluable to making Eden Agent production-ready. We're excited to build this with you!

---

**Happy Testing!**
*The Eden Agent Team*
