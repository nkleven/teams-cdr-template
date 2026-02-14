# Deployment Guide: Garden of Eden Tax & Advisory Website

## 🚀 Quick Start

Your accounting website is ready to deploy! Choose your preferred hosting platform:

---

## Option 1: GitHub Pages (Free & Easy)

### Setup Steps:

1. **Enable GitHub Pages:**
   ```bash
   # Navigate to: https://github.com/nkleven/eden-source-c2/settings/pages
   # Source: Deploy from a branch or GitHub Actions
   ```

2. **Configure GitHub Actions:**
   - Go to Settings → Pages
   - Under "Build and deployment", select **GitHub Actions**
   - The workflow is already configured in `.github/workflows/deploy-website.yml`

3. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy accounting website"
   git push origin main
   ```

4. **Access your site:**
   - URL: `https://nkleven.github.io/eden-source-c2/`
   - Takes 2-3 minutes to deploy

---

## Option 2: Azure Static Web Apps (Recommended)

### Why Azure?
- ✅ Custom domain support
- ✅ Free SSL certificate
- ✅ Global CDN
- ✅ Professional hosting
- ✅ Built-in security headers

### Deployment Steps:

#### Method A: Azure Portal (Visual)

1. **Create Static Web App:**
   ```bash
   # Open Azure Portal
   az login
   az staticwebapp create \
     --name garden-of-eden-tax \
     --resource-group your-resource-group \
     --source https://github.com/nkleven/eden-source-c2 \
     --location centralus \
     --branch main \
     --app-location "/" \
     --output-location "/"
   ```

2. **GitHub Integration:**
   - Azure will automatically add a GitHub Actions workflow
   - Every push to `main` deploys automatically

3. **Custom Domain:**
   - Go to Azure Portal → Static Web App → Custom domains
   - Add: `www.gardenofedentax.com`
   - Update DNS records as instructed

#### Method B: Azure CLI (Fast)

```bash
# Install Azure Static Web Apps CLI
npm install -g @azure/static-web-apps-cli

# Login to Azure
az login

# Create resource group (if needed)
az group create --name rg-eden-tax --location centralus

# Deploy static web app
az staticwebapp create \
  --name garden-of-eden-tax \
  --resource-group rg-eden-tax \
  --source https://github.com/nkleven/eden-source-c2 \
  --branch main \
  --app-location "/" \
  --output-location "/" \
  --login-with-github
```

#### Method C: VS Code Extension

1. Install "Azure Static Web Apps" extension
2. Click Azure icon → Static Web Apps → Create
3. Follow wizard:
   - Select subscription
   - Enter name: `garden-of-eden-tax`
   - Select region
   - Connect GitHub repo
   - Done!

---

## Option 3: Netlify (Alternative)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod
```

---

## Post-Deployment Checklist

### 1. Test the Website
- [ ] Homepage loads correctly
- [ ] All navigation links work
- [ ] CTA buttons function properly
- [ ] Feature cards are interactive
- [ ] Responsive design works on mobile
- [ ] No console errors

### 2. SEO & Analytics
- [ ] Add Google Analytics (optional)
- [ ] Submit sitemap to Google Search Console
- [ ] Verify meta tags and descriptions

### 3. Custom Domain Setup (Optional)
```
# DNS Records for custom domain:
Type  Name  Value                          TTL
A     @     Your_Azure_Static_IP           3600
CNAME www   your-app.azurestaticapps.net  3600
```

### 4. SSL Certificate
- ✅ Automatically provided by Azure/GitHub Pages
- ✅ No configuration needed

---

## Configuration Files

### `staticwebapp.config.json`
- Routing rules
- Security headers
- MIME types
- 404 handling

### `.github/workflows/deploy-website.yml`
- Automated deployment on push
- GitHub Pages integration

---

## Updating the Website

```bash
# Make changes to index.html, app.js, or fluent.css
git add .
git commit -m "Update website content"
git push origin main

# Deployment happens automatically!
```

---

## Support & Resources

### For Accountants Using the Site:
- All interactive features work offline
- No login required
- Click feature cards for detailed information
- Use CTA buttons to schedule consultations

### Technical Support:
- **GitHub Issues**: https://github.com/nkleven/eden-source-c2/issues
- **Azure Support**: https://portal.azure.com
- **Documentation**: This file

---

## Security Features

✅ Content Security Policy (CSP)  
✅ XSS Protection  
✅ Clickjacking protection  
✅ MIME type sniffing prevention  
✅ HTTPS enforced (Azure/GitHub Pages)  

---

## Cost Estimate

| Platform | Cost | Features |
|----------|------|----------|
| GitHub Pages | **FREE** | Basic hosting, HTTPS |
| Azure Static Web Apps (Free Tier) | **FREE** | 100GB bandwidth/month, custom domain |
| Azure Static Web Apps (Standard) | **$9/month** | Unlimited bandwidth, advanced features |
| Netlify | **FREE** | 100GB bandwidth/month |

**Recommendation**: Start with GitHub Pages or Azure Free Tier

---

## Quick Commands

```bash
# Test locally
python -m http.server 3000
# Visit: http://localhost:3000

# Deploy to GitHub Pages
git push origin main

# Deploy to Azure
az staticwebapp create --name garden-of-eden-tax --resource-group rg-eden-tax

# Check deployment status
gh workflow view "Deploy Website"
```

---

## Next Steps

1. ✅ Configuration files created
2. ✅ Deployment workflows ready
3. ⏭️ Choose deployment platform (GitHub Pages or Azure)
4. ⏭️ Push to main branch
5. ⏭️ Share URL with accountants!

---

**Ready to deploy!** 🎉

Choose a platform above and follow the steps. Your accounting website will be live in minutes.
