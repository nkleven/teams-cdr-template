# GitHub Setup Guide for Beta Launch

## Step 1: Create GitHub Release

1. Go to https://github.com/nkleven/eden-source-c2/releases/new
2. Fill in the form:
   - **Tag:** `v0.1.0-beta.1` (create new tag)
   - **Target:** `main` branch
   - **Title:** `v0.1.0-beta.1 - Initial Public Beta`
   - **Description:** Copy contents from [RELEASE_NOTES.md](RELEASE_NOTES.md)
   - **Pre-release:** ✅ Check this box (it's a beta)
3. Click "Publish release"

## Step 2: Enable and Configure Issues

1. Go to https://github.com/nkleven/eden-source-c2/settings
2. Scroll to "Features" section
3. Check ✅ "Issues"
4. Go to https://github.com/nkleven/eden-source-c2/labels
5. Create these labels:

### Labels to Create

| Label | Color | Description |
|-------|-------|-------------|
| `beta-feedback` | `#0E8A16` | Feedback from beta testers |
| `bug` | `#D73A4A` | Something isn't working |
| `enhancement` | `#A2EEEF` | New feature or request |
| `documentation` | `#0075CA` | Improvements or additions to documentation |
| `good first issue` | `#7057FF` | Good for newcomers |
| `help wanted` | `#008672` | Extra attention is needed |
| `priority: high` | `#B60205` | High priority issue |
| `priority: medium` | `#FFA500` | Medium priority issue |
| `priority: low` | `#FBCA04` | Low priority issue |

## Step 3: Create Issue Templates

1. Go to https://github.com/nkleven/eden-source-c2/settings
2. Scroll to "Features" → "Issues" → "Set up templates"
3. Create these templates:

### Bug Report Template

```markdown
---
name: Bug Report
about: Report a bug in Eden Agent
title: '[BUG] '
labels: bug, beta-feedback
---

**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. 
2. 
3. 

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g., Windows 11, macOS 14, Ubuntu 22.04]
- Python version: [e.g., 3.11.5]
- Eden Agent version: [e.g., v0.1.0-beta.1]

**Configuration:**
```env
# Your .env settings (REMOVE YOUR API KEY!)
MODEL_NAME=
MAX_TOKENS=
TEMPERATURE=
```

**Logs:**
```
Paste relevant logs here (run with LOG_LEVEL=DEBUG)
```

**Additional context**
Any other information about the problem.
```

### Feature Request Template

```markdown
---
name: Feature Request
about: Suggest a feature for Eden Agent
title: '[FEATURE] '
labels: enhancement, beta-feedback
---

**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Additional context**
Any other context or screenshots.

**Use case**
How would this feature benefit you and others?
```

## Step 4: Enable Discussions

1. Go to https://github.com/nkleven/eden-source-c2/settings
2. Scroll to "Features" section
3. Check ✅ "Discussions"
4. Go to https://github.com/nkleven/eden-source-c2/discussions
5. Create these categories:
   - **Announcements** - Official updates and news
   - **General** - General discussions about Eden Agent
   - **Q&A** - Questions from beta testers
   - **Ideas** - Feature ideas and brainstorming
   - **Show and tell** - Share what you built with Eden Agent

## Step 5: Share the Beta

### Reddit Posts

**r/MachineLearning:**
```
Title: [P] Eden Agent v0.1.0-beta.1 - Open Beta for AI Agent Framework with Safety & Monitoring

I've released the first public beta of Eden Agent, an AI agent framework built on Claude with comprehensive safety, monitoring, and tracing capabilities.

Key features:
• Responsible AI content filtering with PII detection
• Comprehensive metrics tracking (reliability, safety, transparency)
• OpenTelemetry distributed tracing
• Extensible tool system
• Production-ready health checks

Looking for beta testers to help identify bugs, test edge cases, and provide feedback on the API design.

GitHub: https://github.com/nkleven/eden-source-c2
Beta Welcome: https://github.com/nkleven/eden-source-c2/blob/main/BETA_WELCOME.md

All feedback welcome!
```

**r/Python:**
```
Title: [Release] Eden Agent - AI Agent Framework (Open Beta)

Just released v0.1.0-beta.1 of Eden Agent, a Python framework for building AI agents with Claude.

What makes it different:
• Built-in safety & content filtering
• Responsible AI metrics out of the box
• Full OpenTelemetry tracing support
• Comprehensive error handling
• Production-ready design

Perfect for developers building AI applications who want safety and observability baked in from day one.

Open beta - looking for testers!
GitHub: https://github.com/nkleven/eden-source-c2
```

### Discord Announcements

**Python Discord / AI/ML Channels:**
```
🚀 **Eden Agent v0.1.0-beta.1 - Open Beta!**

Just launched the first public beta of Eden Agent - an AI agent framework with comprehensive safety & monitoring.

**Features:**
✅ Claude Sonnet 4.5 integration
✅ Content safety & PII filtering
✅ Responsible AI metrics
✅ OpenTelemetry tracing
✅ Health monitoring
✅ 15 passing smoke tests

**Looking for beta testers!**
📘 Docs: https://github.com/nkleven/eden-source-c2
👋 Start here: https://github.com/nkleven/eden-source-c2/blob/main/BETA_WELCOME.md

Would love your feedback! 🙏
```

### Twitter/X Post

```
🚀 Excited to announce Eden Agent v0.1.0-beta.1 - open beta!

AI agent framework built on Claude with:
• Comprehensive safety & content filtering
• Responsible AI metrics
• OpenTelemetry tracing
• Production-ready architecture

Looking for beta testers! 🧪

https://github.com/nkleven/eden-source-c2

#AI #Python #OpenSource #MachineLearning
```

### Hacker News (Show HN)

```
Title: Show HN: Eden Agent – AI agent framework with safety and monitoring (beta)

I've been working on Eden Agent, a framework for building AI agents with Claude that emphasizes safety and observability from the start.

Key features:
- Built-in content safety with PII detection, jailbreak prevention
- Comprehensive metrics (reliability, safety, transparency)
- OpenTelemetry distributed tracing
- Extensible tool system
- Health monitoring

This is the first public beta (v0.1.0-beta.1). The goal is to make it easier to build production-ready AI agents without having to build all the safety and monitoring infrastructure yourself.

I'm looking for beta testers to help identify bugs and provide feedback on the API design. All the details are in the repo.

Would love to hear your thoughts!
```

## Step 6: Monitor and Respond

- Check GitHub Issues daily
- Respond to beta feedback within 24-48 hours
- Update documentation based on common questions
- Track bug reports in a GitHub Project board
- Celebrate wins and thank contributors

---

**Good luck with the beta launch! 🎉**
