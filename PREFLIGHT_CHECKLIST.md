# Pre-Flight Checklist ✈️

## Before First Run

### Dependencies Installed
- [x] SWA CLI installed (`npm install` completed)
- [x] Python packages installed (`pip install -r api/requirements.txt` completed)
- [ ] **REQUIRED**: Add your Anthropic API key to `api/local.settings.json`

### Files Ready
- [x] API structure created ([api/](api))
- [x] Agent endpoint ([api/agent/](api/agent))
- [x] Health check endpoint ([api/health/](api/health))
- [x] Configuration files updated
- [x] Frontend integration script ([agent-client.js](agent-client.js))

### Configuration Check
- [x] [staticwebapp.config.json](staticwebapp.config.json) - Auth & routing configured
- [x] [swa-cli.config.json](swa-cli.config.json) - API location set
- [x] [package.json](package.json) - NPM scripts ready
- [ ] `api/local.settings.json` - **Add your API key here!**

---

## First Flight 🛫

### 1. Configure API Key (Required)
Edit `api/local.settings.json`:
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "ANTHROPIC_API_KEY": "sk-ant-YOUR-KEY-HERE"  ← Add your key
  }
}
```

### 2. Start Local Server
```powershell
npm start
```

Expected output:
```
Azure Static Web Apps emulator started at http://localhost:4280
Functions host started at http://localhost:7071
```

### 3. Test Endpoints
Open these in your browser or use curl:

**Health Check (Public):**
```powershell
curl http://localhost:4280/api/health
```
Expected: `{"status":"healthy",...}`

**Auth Status:**
```powershell
curl http://localhost:4280/.auth/me
```
Expected: User info or empty (local mode)

**Agent Chat (Authenticated):**
```powershell
curl -X POST http://localhost:4280/api/agent `
  -H "Content-Type: application/json" `
  -d '{"message":"What is 2+2?"}'
```

---

## Deployment Checklist 🚀

### Pre-Deployment
- [ ] Tested locally successfully
- [ ] All endpoints responding correctly
- [ ] Authentication flow tested
- [ ] Static pages load properly

### Deploy to Azure
```powershell
# Step 1: Login
npx swa login

# Step 2: Deploy
npm run deploy
```

### Post-Deployment
- [ ] Add production API key in Azure Portal
  - Go to: Static Web App → Configuration
  - Add: `ANTHROPIC_API_KEY = sk-ant-...`
- [ ] Test production health endpoint
- [ ] Test authentication in production
- [ ] Test agent chat functionality

---

## Troubleshooting Guide

### "npm start" fails
**Check:**
- SWA CLI installed: `swa --version`
- Python available: `python --version`
- API dependencies: `cd api && pip list`

**Fix:**
```powershell
npm install -g @azure/static-web-apps-cli
pip install -r api/requirements.txt
```

### API returns 500 error
**Check:**
- API key configured in `api/local.settings.json`
- Python modules installed
- Function logs in terminal for errors

### "Module not found" errors
**Fix:**
```powershell
# Install project as editable package
pip install -e .
```

### Authentication doesn't work locally
**Note:** Local dev uses simulated auth. Real auth only works in production.

**To test auth flow:**
- Deploy to Azure first
- Test auth in production environment

---

## Quick Reference

### NPM Scripts
| Command | Purpose |
|---------|---------|
| `npm start` | Start local dev (frontend + API) |
| `npm run deploy` | Deploy to Azure |
| `npm run api:install` | Install API dependencies |
| `npm run api:local` | Start API only |

### Endpoints
| Path | Method | Auth | Purpose |
|------|--------|------|---------|
| `/api/agent` | POST | ✅ | AI agent chat |
| `/api/health` | GET | ❌ | Health check |
| `/.auth/me` | GET | ❌ | Auth status |
| `/login` | GET | ❌ | Login redirect |
| `/logout` | GET | ❌ | Logout |

### File Locations
- **Frontend**: `index.html`, `accountant/index.html`
- **API**: `api/agent/`, `api/health/`
- **Config**: `staticwebapp.config.json`, `swa-cli.config.json`
- **Docs**: `QUICKSTART_SWA.md`, `SWA_DEPLOYMENT.md`

---

## Status: Ready for Takeoff! ✈️

All systems are configured. Just add your API key and you're cleared for departure!

**Next Command:**
```powershell
npm start
```

Then open: http://localhost:4280

---

*For detailed documentation, see [QUICKSTART_SWA.md](QUICKSTART_SWA.md)*
