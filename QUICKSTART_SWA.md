# Quick Start Guide for Eden Agent Azure SWA

## 🚀 Fast Track to Running Locally

### Step 1: Install Dependencies (2 minutes)
```powershell
# From project root S:\eden-source-c2
npm install
cd api
pip install -r requirements.txt
cd ..
```

### Step 2: Configure API Key (1 minute)
Edit `api\local.settings.json` and add your Anthropic API key:
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "ANTHROPIC_API_KEY": "sk-ant-..."
  }
}
```

### Step 3: Start the App (30 seconds)
```powershell
npm start
```

Open browser to: **http://localhost:4280**

---

## 🌐 Deploy to Azure (5 minutes)

### First Time Deployment
```powershell
# Login to Azure
npx swa login

# Deploy
npm run deploy
```

**Follow the prompts:**
1. Select your subscription
2. Create new or select existing Static Web App
3. Choose resource group: `rg-garden-of-eden`
4. Wait for deployment (2-3 minutes)

### Update Production Environment Variables
After first deployment, add your API key in Azure Portal:
1. Go to your Static Web App resource
2. Settings → Configuration
3. Add Application setting:
   - Name: `ANTHROPIC_API_KEY`
   - Value: `sk-ant-...`
4. Click Save

### GitHub Actions (Automated Deployments)
Connect your GitHub repo in Azure Portal for automatic deployments on push:
1. Static Web App → Deployment
2. Link GitHub repository
3. Azure creates `.github/workflows/azure-static-web-apps-*.yml`

---

## 🔒 Authentication Test

Test auth locally:
```powershell
# Check auth status
curl http://localhost:4280/.auth/me

# Login
# Open browser to: http://localhost:4280/login

# After login, test agent API
curl -X POST http://localhost:4280/api/agent `
  -H "Content-Type: application/json" `
  -d '{"message":"What is 42 * 137?"}'
```

---

## 📊 Project Status

✅ **Completed:**
- API backend with Azure Functions (Python)
- Agent and health endpoints
- Authentication (GitHub, Azure AD)
- SWA CLI configuration
- Local development setup
- Security headers and CSP

✅ **Ready to Deploy:**
- Static frontend with agent integration
- Managed Functions API
- Built-in authentication
- Auto-scaling and CDN

📝 **Next Steps:**
1. Test locally with `npm start`
2. Deploy with `npm run deploy`
3. Configure production API key
4. Test agent chat functionality

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `staticwebapp.config.json` | Routing, auth, security headers |
| `swa-cli.config.json` | SWA CLI local dev config |
| `api/agent/__init__.py` | Eden Agent chat endpoint |
| `api/health/__init__.py` | Health check endpoint |
| `agent-client.js` | Frontend API integration |
| `package.json` | NPM scripts for dev/deploy |

---

## 🛠 Troubleshooting

**"Command 'swa' not found"**
```powershell
npm install -g @azure/static-web-apps-cli
```

**"API returns 500 error"**
- Check `ANTHROPIC_API_KEY` is set
- Check Python dependencies are installed
- Review function logs in terminal

**"Authentication not working"**
- In local dev, auth is simulated
- In production, configure providers in Azure Portal

---

## 📚 Full Documentation

See [SWA_DEPLOYMENT.md](SWA_DEPLOYMENT.md) for comprehensive guide.
