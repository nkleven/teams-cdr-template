# Azure Static Web Apps Deployment Guide

## 🎯 Quick Start - Deploy to Azure SWA

Your website is ready to deploy! Follow these steps:

---

## Prerequisites

- Azure account ([free account available](https://azure.microsoft.com/free/))
- GitHub repository with your code
- Azure CLI (optional but recommended)

---

## Method 1: Azure Portal (Easiest - 5 minutes)

### Step 1: Create Azure Static Web App

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **"Create a resource"**
3. Search for **"Static Web App"**
4. Click **"Create"**

### Step 2: Configure Basic Settings

| Setting | Value |
|---------|-------|
| **Subscription** | Select your subscription |
| **Resource Group** | Create new: `rg-garden-of-eden` |
| **Name** | `garden-of-eden-tax` |
| **Plan type** | Free (for hobby or personal projects) |
| **Region** | East US 2 (or closest to you) |

### Step 3: Configure Deployment

| Setting | Value |
|---------|-------|
| **Source** | GitHub |
| **Organization** | `nkleven` |
| **Repository** | `eden-source-c2` |
| **Branch** | `main` (or `copilot/implement-ui-functionality`) |

### Step 4: Build Settings

| Setting | Value |
|---------|-------|
| **Build Presets** | Custom |
| **App location** | `/` |
| **Api location** | (leave empty) |
| **Output location** | (leave empty) |

### Step 5: Review and Create

1. Click **"Review + create"**
2. Click **"Create"**
3. Wait 2-3 minutes for deployment

### Step 6: Get Your URL

After creation, you'll see:
```
Your site URL: https://garden-of-eden-tax-<random>.azurestaticapps.net
```

---

## Method 2: Using SWA CLI (Fastest)

```powershell
# Install SWA CLI
npm install -g @azure/static-web-apps-cli

# Login to Azure
az login

# Initialize SWA (creates config)
swa init

# Follow the prompts:
# - Select: "Create a new Static Web App"
# - Name: garden-of-eden-tax
# - Region: East US 2
# - App location: /
# - Output location: (leave empty)

# Deploy!
swa deploy
```

---

## Method 3: Azure CLI (Advanced)

```powershell
# Login
az login

# Create resource group
az group create `
  --name rg-garden-of-eden `
  --location eastus2

# Create Static Web App
az staticwebapp create `
  --name garden-of-eden-tax `
  --resource-group rg-garden-of-eden `
  --source https://github.com/nkleven/eden-source-c2 `
  --location eastus2 `
  --branch main `
  --app-location "/" `
  --output-location "" `
  --login-with-github

# Get deployment token
$token = az staticwebapp secrets list `
  --name garden-of-eden-tax `
  --resource-group rg-garden-of-eden `
  --query "properties.apiKey" -o tsv

Write-Host "Add this token to GitHub Secrets as AZURE_STATIC_WEB_APPS_API_TOKEN:"
Write-Host $token
```

---

## Adding the GitHub Secret

After creating the Azure SWA resource, you need to add the deployment token to GitHub:

### Step 1: Get the Deployment Token

From Azure Portal:
1. Go to your Static Web App resource
2. Click **"Manage deployment token"**
3. Copy the token

Or using Azure CLI:
```powershell
az staticwebapp secrets list `
  --name garden-of-eden-tax `
  --resource-group rg-garden-of-eden `
  --query "properties.apiKey" -o tsv
```

### Step 2: Add to GitHub

1. Go to your GitHub repo: `https://github.com/nkleven/eden-source-c2`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Name: `AZURE_STATIC_WEB_APPS_API_TOKEN`
5. Value: Paste the token from Step 1
6. Click **"Add secret"**

---

## Verify Deployment

### Check GitHub Actions

1. Go to: `https://github.com/nkleven/eden-source-c2/actions`
2. You should see **"Azure Static Web Apps CI/CD"** workflow
3. Wait for green checkmark ✅

### Test Your Site

Visit your Azure SWA URL:
```
https://garden-of-eden-tax-<random>.azurestaticapps.net
```

**Test checklist:**
- [ ] Homepage loads
- [ ] Navigation works
- [ ] Forms are functional
- [ ] Responsive design works
- [ ] No console errors

---

## Custom Domain Setup

### Step 1: Add Custom Domain in Azure

1. Go to Azure Portal → Your Static Web App
2. Click **"Custom domains"**
3. Click **"+ Add"** → **"Custom domain on other DNS"**
4. Enter: `www.gardenofedentax.com`
5. Azure will provide validation records

### Step 2: Update DNS Records

Add these records to your DNS provider:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| CNAME | www | `<your-swa-url>.azurestaticapps.net` | 3600 |
| TXT | _dnsauth.www | `<validation-token>` | 3600 |

### Step 3: Verify

- Wait 10-15 minutes for DNS propagation
- Azure will automatically verify and enable HTTPS

---

## Environment Configuration

Your current `staticwebapp.config.json` is already configured with:

✅ Security headers (CSP, X-Frame-Options)  
✅ MIME types  
✅ 404 fallback to index.html  
✅ Route handling  

**No additional configuration needed!**

---

## Updating Your Site

Every time you push to the `main` branch, GitHub Actions will automatically:
1. Build your site
2. Deploy to Azure
3. Update the live site

```powershell
# Make changes to your files
git add .
git commit -m "Update website"
git push origin main

# Deployment happens automatically!
# Check progress: https://github.com/nkleven/eden-source-c2/actions
```

---

## Monitoring & Logs

### View Application Insights

1. Azure Portal → Your Static Web App
2. Click **"Application Insights"**
3. View:
   - Page views
   - Performance metrics
   - Errors and exceptions

### Check Deployment Logs

1. Azure Portal → Your Static Web App
2. Click **"GitHub Action runs"**
3. View deployment history

---

## Cost Breakdown

| Tier | Cost | Bandwidth | Custom Domain | Features |
|------|------|-----------|---------------|----------|
| **Free** | $0/month | 100GB/month | ✅ | Perfect for this site |
| **Standard** | $9/month | Unlimited | ✅ | Premium features |

**Recommendation**: Start with **Free tier** - more than enough for a professional website

---

## Troubleshooting

### Issue: GitHub Action Fails

**Solution**: Verify the `AZURE_STATIC_WEB_APPS_API_TOKEN` secret is set correctly

```powershell
# Regenerate token if needed
az staticwebapp secrets list `
  --name garden-of-eden-tax `
  --resource-group rg-garden-of-eden
```

### Issue: 404 Errors for Assets

**Solution**: Check your `staticwebapp.config.json` excludes:
```json
"exclude": ["/assets/*", "/styles.css", "/fluent.css", "/app.js"]
```

### Issue: Custom Domain Not Working

**Solution**: 
1. Verify DNS records are correct
2. Wait 24 hours for DNS propagation
3. Check validation status in Azure Portal

---

## Production Checklist

Before going live:

- [ ] GitHub Actions workflow runs successfully
- [ ] Site deploys to Azure SWA
- [ ] All pages load correctly
- [ ] Forms work properly
- [ ] Mobile responsive
- [ ] HTTPS enabled (automatic)
- [ ] Custom domain configured (optional)
- [ ] Analytics added (optional)
- [ ] Contact information verified

---

## Next Steps

1. **Deploy Now**: Follow Method 1 (Azure Portal) above
2. **Add Secret**: Add deployment token to GitHub
3. **Push Code**: Merge your branch to `main`
4. **Verify**: Check your site at the Azure URL
5. **Custom Domain**: Set up your domain (optional)

---

## Support

- **Azure Docs**: https://docs.microsoft.com/azure/static-web-apps/
- **SWA CLI**: https://azure.github.io/static-web-apps-cli/
- **GitHub Issues**: https://github.com/nkleven/eden-source-c2/issues

---

**You're ready to deploy!** 🚀

Choose a method above and your site will be live in minutes.
