# Azure Static Web App - Certificate Troubleshooting Guide

## Current Status ✅

**Date:** December 24, 2025

All custom domains on Azure Static Web Apps are currently **OPERATIONAL**:

| Domain | Status | HTTPS | Certificate |
|--------|--------|-------|-------------|
| staging.kellzkreations.com | ✅ Ready | ✅ Working | ✅ Valid |
| genesis.kellzkreations.com | ✅ Ready | ✅ Working | ✅ Valid |
| www.kellzkreations.com | ✅ Ready | ✅ Working | ✅ Valid |
| mark.kellzkreations.com | ✅ Ready | ✅ Working | ✅ Valid |

---

## Common Certificate Errors & Solutions

### 1. Certificate Not Yet Provisioned

**Symptoms:**
- Browser shows "Your connection is not private"
- Certificate error: NET::ERR_CERT_AUTHORITY_INVALID
- Domain shows "Validating" status in Azure Portal

**Solutions:**

```bash
# Check domain validation status
az staticwebapp hostname show \
  --name eden-staging \
  --resource-group eden \
  --hostname "your-domain.com" \
  --output json

# If status is "Validating", wait 24-48 hours for certificate provisioning
```

**Typical Timeline:**
- DNS propagation: 1-24 hours
- Certificate validation: 1-48 hours
- Total: Up to 72 hours

### 2. DNS Configuration Issues

**Symptoms:**
- Domain not resolving
- Certificate validation stuck
- "DNS resolution failed" errors

**Solutions:**

```bash
# Verify DNS records
nslookup your-domain.com

# Check TXT record for validation (if required)
nslookup -type=TXT _dnsauth.your-domain.com

# Verify CNAME points to Azure SWA
nslookup -type=CNAME www.your-domain.com
```

**Required DNS Records:**

For **Apex Domain** (e.g., kellzkreations.com):
```
Type: TXT
Name: _dnsauth
Value: [validation-token-from-azure]
TTL: 3600

Type: TXT
Name: asuid
Value: [azure-static-web-app-id]
TTL: 3600
```

For **Subdomain** (e.g., www.kellzkreations.com):
```
Type: CNAME
Name: www
Value: zealous-sky-0b4dd2c0f.3.azurestaticapps.net
TTL: 3600
```

### 3. Certificate Renewal Issues

**Symptoms:**
- Previously working domain shows certificate error
- Certificate expired warning
- "NET::ERR_CERT_DATE_INVALID"

**Solutions:**

```bash
# Force certificate refresh
az staticwebapp hostname delete \
  --name eden-staging \
  --resource-group eden \
  --hostname "your-domain.com"

# Wait 5 minutes, then re-add the domain
az staticwebapp hostname set \
  --name eden-staging \
  --resource-group eden \
  --hostname "your-domain.com"
```

### 4. Mixed Content Warnings

**Symptoms:**
- Page loads but shows "Not Secure" padlock
- Console errors: "Mixed Content"
- Resources blocked by browser

**Solution - Update staticwebapp.config.json:**

```json
{
  "globalHeaders": {
    "content-security-policy": "default-src 'self' https:; style-src 'self' 'unsafe-inline' https:; script-src 'self' https:; img-src 'self' data: https:; font-src 'self' data: https:",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY"
  }
}
```

### 5. Custom Domain Not Showing in Portal

**Symptoms:**
- Domain added but not visible
- CLI shows domain but Portal doesn't
- "Resource not found" errors

**Solutions:**

```bash
# List all custom domains
az staticwebapp hostname list \
  --name eden-staging \
  --resource-group eden \
  --output table

# If domain missing, add it
az staticwebapp hostname set \
  --name eden-staging \
  --resource-group eden \
  --hostname "new-domain.com"
```

---

## Diagnostic Commands

### Check All Static Web Apps
```bash
az staticwebapp list --output table
```

### Check Custom Domains for a Site
```bash
az staticwebapp hostname list \
  --name eden-staging \
  --resource-group eden \
  --output table
```

### Check Specific Domain Details
```bash
az staticwebapp hostname show \
  --name eden-staging \
  --resource-group eden \
  --hostname "staging.kellzkreations.com" \
  --output json
```

### Test HTTPS Connection
```powershell
# PowerShell
Invoke-WebRequest -Uri "https://staging.kellzkreations.com" -UseBasicParsing

# Or use curl
curl -I https://staging.kellzkreations.com
```

### Check Certificate Details
```powershell
# PowerShell - View certificate details
$url = "https://staging.kellzkreations.com"
$request = [System.Net.WebRequest]::Create($url)
$request.GetResponse() | Out-Null
$cert = $request.ServicePoint.Certificate
$cert | Select-Object Subject, Issuer, GetExpirationDateString
```

### Verify DNS Propagation
```bash
# Check DNS from different locations
nslookup staging.kellzkreations.com
nslookup staging.kellzkreations.com 8.8.8.8
nslookup staging.kellzkreations.com 1.1.1.1

# Check DNS propagation globally
# Visit: https://www.whatsmydns.net/
```

---

## Adding a New Custom Domain

### Step 1: Verify Domain Ownership
```bash
# Get the validation token
az staticwebapp hostname set \
  --name eden-staging \
  --resource-group eden \
  --hostname "newdomain.com"

# Azure will provide a TXT record to add to your DNS
```

### Step 2: Add DNS Records

**For Apex Domain (newdomain.com):**
```
TXT  _dnsauth  [validation-token]
TXT  asuid     [your-swa-id]
```

**For Subdomain (www.newdomain.com):**
```
CNAME  www  zealous-sky-0b4dd2c0f.3.azurestaticapps.net
```

### Step 3: Wait for Validation
```bash
# Check status every 30 minutes
az staticwebapp hostname show \
  --name eden-staging \
  --resource-group eden \
  --hostname "newdomain.com" \
  --query "status" \
  --output tsv
```

### Step 4: Verify Certificate
```bash
# Once status is "Ready", test HTTPS
curl -I https://newdomain.com

# Should return: HTTP/1.1 200 OK
```

---

## Certificate Best Practices

### 1. Use HTTPS Everywhere
- Always redirect HTTP to HTTPS
- Add HSTS header for security
- Enable "Require HTTPS" in Azure Portal

### 2. Monitor Certificate Expiration
- Azure auto-renews Let's Encrypt certificates
- Certificates typically valid for 90 days
- Auto-renewal happens at 60 days

### 3. Test Before Going Live
```bash
# Test staging domain first
https://staging.kellzkreations.com

# Then promote to production
https://www.kellzkreations.com
```

### 4. Enable Enterprise CDN (Optional)
```bash
# For better performance and global certificate management
az staticwebapp enterprise-edge enable \
  --name eden-staging \
  --resource-group eden
```

---

## Troubleshooting Checklist

When experiencing certificate errors:

- [ ] Verify DNS records are correct
- [ ] Wait 24-48 hours for DNS propagation
- [ ] Check Azure Portal for domain status
- [ ] Confirm validation token is in DNS
- [ ] Test from different networks/browsers
- [ ] Clear browser cache and SSL state
- [ ] Check for mixed content warnings
- [ ] Verify no firewalls blocking port 443
- [ ] Test with curl/PowerShell commands
- [ ] Review Azure activity logs for errors

---

## Emergency Contacts & Resources

### Azure Support
- Portal: https://portal.azure.com
- Support tickets: portal.azure.com → Support → New support request
- Community: https://docs.microsoft.com/answers/

### DNS Provider Support
- Check your domain registrar's documentation
- Verify DNS management panel access
- Contact DNS provider support if needed

### Documentation
- Azure SWA Custom Domains: https://learn.microsoft.com/azure/static-web-apps/custom-domain
- SSL/TLS Configuration: https://learn.microsoft.com/azure/static-web-apps/custom-domain-ssl

---

## Current Configuration Summary

**Static Web App:** eden-staging  
**Resource Group:** eden  
**Region:** East US 2  
**Default Hostname:** zealous-sky-0b4dd2c0f.3.azurestaticapps.net  

**Custom Domains (All Active):**
1. ✅ staging.kellzkreations.com (Primary staging environment)
2. ✅ genesis.kellzkreations.com (Project genesis)
3. ✅ www.kellzkreations.com (Production)
4. ✅ mark.kellzkreations.com (Mark's domain)

**Certificate Status:** All domains have valid SSL/TLS certificates  
**Certificate Provider:** Let's Encrypt (Auto-managed by Azure)  
**Certificate Type:** Domain Validated (DV)  
**Auto-Renewal:** Enabled ✅

---

## Quick Reference Commands

```bash
# View all sites
az staticwebapp list --output table

# View all custom domains
az staticwebapp hostname list --name eden-staging --resource-group eden --output table

# Add custom domain
az staticwebapp hostname set --name eden-staging --resource-group eden --hostname "new.domain.com"

# Remove custom domain
az staticwebapp hostname delete --name eden-staging --resource-group eden --hostname "old.domain.com"

# View domain details
az staticwebapp hostname show --name eden-staging --resource-group eden --hostname "domain.com" --output json

# Test HTTPS
curl -I https://your-domain.com

# Check DNS
nslookup your-domain.com
```

---

**Last Updated:** December 24, 2025  
**Status:** All systems operational ✅  
**Next Review:** January 24, 2026
