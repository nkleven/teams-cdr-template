# 🚀 Azure SWA Deployment - Quick Start

## What You Need:

1. ✅ Azure account ([Get free account](https://azure.microsoft.com/free/))
2. ✅ Files ready (already done!)
3. ⏭️ Deploy token from Azure

---

## Fastest Way: 3 Steps to Deploy

### Step 1: Create Azure Static Web App (2 min)

Go to [Azure Portal](https://portal.azure.com) and run this in Cloud Shell:

```bash
# Create resource group
az group create --name rg-garden-of-eden --location eastus2

# Create Static Web App
az staticwebapp create \
  --name garden-of-eden-tax \
  --resource-group rg-garden-of-eden \
  --source https://github.com/nkleven/eden-source-c2 \
  --location eastus2 \
  --branch main \
  --app-location "/" \
  --output-location "" \
  --login-with-github
```

### Step 2: Get Deployment Token (30 sec)

```bash
# Get your deployment token
az staticwebapp secrets list \
  --name garden-of-eden-tax \
  --resource-group rg-garden-of-eden \
  --query "properties.apiKey" -o tsv
```

**Copy this token!** You'll need it in the next step.

### Step 3: Add Token to GitHub (1 min)

1. Go to: https://github.com/nkleven/eden-source-c2/settings/secrets/actions
2. Click **"New repository secret"**
3. Name: `AZURE_STATIC_WEB_APPS_API_TOKEN`
4. Value: Paste the token from Step 2
5. Click **"Add secret"**

---

## Deploy!

```powershell
# Push your code
git add .
git commit -m "Deploy to Azure SWA"
git push origin main

# Watch deployment at:
# https://github.com/nkleven/eden-source-c2/actions
```

---

## Your Site Will Be Live At:

```
https://garden-of-eden-tax-<random-id>.azurestaticapps.net
```

Find exact URL in Azure Portal → Static Web Apps → Overview

---

## That's It! 🎉

**Total time: ~5 minutes**

Your professional tax advisory website is now:
- ✅ Deployed on Azure
- ✅ HTTPS enabled
- ✅ Global CDN
- ✅ Auto-deploys on every push to main
- ✅ 100% free tier

---

## Next Steps (Optional):

- **Custom Domain**: See [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md#custom-domain-setup)
- **Monitoring**: Enable Application Insights in Azure Portal
- **Staging**: Push to feature branches for preview deployments

---

**Need Help?** See [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md) for detailed instructions.
