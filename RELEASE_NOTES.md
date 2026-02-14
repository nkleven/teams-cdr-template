# Release Notes - v2.1.1

**Eden Agent - Production Ready**

We're excited to release version 2.1.1 of Eden Agent! This release marks the culmination of our final sprint, bringing unified versioning and production stability to the framework.

## 🎉 What's New

### Core Features
- **Unified Versioning** - Synchronized with Eden Genesis for better ecosystem management.
- **Production Stability** - Final polish and bug fixes from the 2.1.1 code sprint.
- **AI Agent with Claude Integration** - Powered by Claude Sonnet 4.5
- **Tool System** - Extensible framework with calculator tool
- **Safety & Content Filtering** - PII detection, jailbreak prevention, content moderation
- **Responsible AI Metrics** - Comprehensive tracking for reliability, safety, and transparency
- **OpenTelemetry Tracing** - Full distributed tracing support
- **Health Checks** - System status monitoring and validation

### Developer Experience
- **Configuration Validation** - Clear error messages for missing/invalid config
- **Enhanced Error Handling** - User-friendly errors throughout the codebase
- **Rich Logging** - Beautiful console output with configurable levels
- **Comprehensive Testing** - 15 smoke tests covering all major functionality

### Documentation
- 📘 Complete README with setup instructions
- ✅ Beta Testing Checklist with procedures
- 👋 Beta Welcome Guide for new testers
- ⚙️ Detailed .env.example with all configuration options

## 🧪 Beta Testing

This is an **open beta** release. We're looking for:
- Bug reports and edge cases
- Performance feedback
- Usability issues
- Feature requests
- Documentation improvements

See [BETA_WELCOME.md](BETA_WELCOME.md) for how to get started.

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/nkleven/eden-source-c2.git
cd eden-source-c2

# Install dependencies
pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Verify installation
pytest tests/smoke_test.py -v
```

## ⚠️ Known Limitations

- Console-only tracing exporter (Jaeger/OTLP experimental)
- Single-user sessions only

See [BETA_CHECKLIST.md](BETA_CHECKLIST.md) for complete details.

## ✨ Recent Updates (Post-Beta Release)

### New Features Implemented
- ✅ **API Rate Limiting** - Prevents hitting API limits with configurable token bucket algorithm
- ✅ **Retry Logic with Exponential Backoff** - Automatic retry for transient failures
- ✅ **Custom Tool Registration** - Dynamic tool registration/unregistration API
- ✅ **Enhanced Health Checks** - Already had comprehensive health monitoring
- ✅ **Configuration Management** - Extended settings for rate limiting and retries

These features move several items from "Known Limitations" to "Implemented". See `examples/advanced_features.py` for usage demonstrations.

## 🐛 Bug Fixes

This is the initial beta release, so no bug fixes yet!

## 🔄 Breaking Changes

N/A - Initial release

## 📊 Test Results

All 15 smoke tests passing:
- ✅ Agent core functionality (3 tests)
- ✅ Content safety (4 tests)
- ✅ Metrics & monitoring (4 tests)
- ✅ Tracing (2 tests)
- ✅ Integration (2 tests)

## 🙏 Acknowledgments

Thank you to our beta testers for helping make Eden Agent production-ready!

## 📝 What's Next (v0.2.0)

### ✅ Recently Completed

- API rate limiting and exponential backoff
- Advanced tool registration API
- Multi-user session management
- Production health monitoring

### 🚧 In Progress

- Enhanced Metrics Dashboard with real-time charts
- Real-time Monitoring UI improvements
- Additional built-in tools (DateTime, Text, Web, JSON, File utilities)

### 📋 Planned

- Advanced analytics and reporting
- Plugin architecture for custom extensions
- Multi-tenant support
- Database persistence layer

---

**Full Changelog**: https://github.com/nkleven/eden-source-c2/commits/v0.1.0-beta.1

**Join the Beta**: Read [BETA_WELCOME.md](BETA_WELCOME.md) to get started!
