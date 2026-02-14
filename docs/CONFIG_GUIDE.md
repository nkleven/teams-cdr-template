# Configuration Guide

## Overview

This project has multiple configuration files for different environments and purposes. This guide clarifies which configuration to use and when.

## Configuration Files

### 1. `/src/config.py` (Primary Application Config) ✅ USE THIS

**Purpose**: Main application configuration for the Eden Agent system
**Used By**: 
- Agent core (`src/agent/core.py`)
- Azure Functions (`api/agent/__init__.py`)
- Tools and utilities throughout the application

**Key Settings**:
- Anthropic API configuration (Claude models)
- Wedding-specific context (Kelli & Nathan)
- Travel coordination settings
- Payment integration (Stripe)
- Tracing and monitoring
- Rate limiting

**Environment Variables**: See `.env.example` for required variables

```python
from src.config import settings
# Access settings like:
# settings.anthropic_api_key
# settings.bride_name, settings.groom_name
```

---

### 2. `/config.py` (Root - Deprecated/Alternate Backend) ⚠️

**Purpose**: Configuration for alternate Ollama-based backend
**Status**: Secondary backend option using local Ollama instance
**Used By**: `/core.py` (root-level alternate implementation)

**Key Settings**:
- Ollama API configuration (local models)
- Basic tracing and rate limiting

**Note**: This is for development/testing with local LLMs. The primary production system uses Anthropic Claude (see `/src/config.py`).

---

### 3. `/local.settings.json` (Azure Functions Local Dev)

**Purpose**: Azure Functions runtime configuration for local development
**Used By**: Azure Functions Core Tools / `func host start`

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python"
  }
}
```

---

### 4. `/staticwebapp.config.json` (Azure SWA)

**Purpose**: Azure Static Web Apps configuration for routing and security
**Features**:
- Route configuration
- Security headers (CSP, XSS protection)
- MIME type mappings
- Navigation fallback rules

---

### 5. `/swa-cli.config.json` (SWA CLI)

**Purpose**: Azure Static Web Apps CLI tool configuration
**Used By**: `swa` CLI commands during development

---

## Environment Setup

### Production (Azure Functions + Claude)

1. Copy `.env.example` to `.env`
2. Set `ANTHROPIC_API_KEY` with your Claude API key
3. Configure other settings as needed
4. Use `/src/config.py` settings throughout application

```bash
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY
```

### Local Development (Ollama Alternative)

1. Install and run Ollama locally
2. Use `/config.py` settings
3. Point `OLLAMA_BASE_URL` to local instance

```bash
ollama serve
# Use local model like llama3.2
```

## API Backends

The project supports multiple AI backends:

| Backend | Config File | API Client | Use Case |
|---------|-------------|------------|----------|
| **Anthropic Claude** (Primary) | `/src/config.py` | `anthropic` | Production, Azure Functions |
| **Ollama** (Secondary) | `/config.py` | `openai` (compatible) | Local development, testing |
| **Azure OpenAI** (Legacy) | `/function_app.py` | `openai.AzureOpenAI` | Old implementation |

## Best Practices

1. **Always use `/src/config.py`** for new features
2. Keep sensitive keys in `.env` (never commit!)
3. Use `.env.example` as template
4. Document new config options in this guide
5. Use `pydantic` validation for new settings

## Configuration Priority

Settings are loaded in this order (later overrides earlier):

1. Default values in config class
2. `.env` file variables
3. Environment variables (system)

## Common Issues

### Import Errors
❌ `from ..config import settings` (in root files)
✅ `from src.config import settings` (absolute import)

### Missing API Key
```
ANTHROPIC_API_KEY not configured
```
→ Check `.env` file has valid API key

### Wrong Backend
If Claude calls fail, check you're using the right config:
- Production: `/src/config.py` (Anthropic)
- Local dev: `/config.py` (Ollama)

## Migration Notes

**Consolidating configs**: Future work should consolidate `/config.py` and `/src/config.py` into a single unified configuration system with backend selection via environment variable.

---

**Last Updated**: Feb 9, 2026
**Maintainer**: Development Team
