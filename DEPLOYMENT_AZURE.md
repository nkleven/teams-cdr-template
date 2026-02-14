# Deployment Guide

This guide covers deploying the Teams CDR Template application to production environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Azure App Service Deployment](#azure-app-service-deployment)
- [Docker Deployment](#docker-deployment)
- [Environment Variables](#environment-variables)
- [Security Best Practices](#security-best-practices)

## Prerequisites

Before deploying, ensure you have:
- ✅ Azure subscription with appropriate permissions
- ✅ Azure CLI installed (`az --version`)
- ✅ Application built (`npm run build`)
- ✅ Azure AD App Registration configured
- ✅ Production secrets ready (Client ID, Secret, Tenant ID)

## Azure App Service Deployment

### Deploy Using Azure CLI

#### Step 1: Create Resource Group

```bash
az group create \
  --name teams-cdr-rg \
  --location eastus
```

#### Step 2: Create App Service Plan

```bash
az appservice plan create \
  --name teams-cdr-plan \
  --resource-group teams-cdr-rg \
  --sku B1 \
  --is-linux
```

#### Step 3: Create Web App

```bash
az webapp create \
  --name teams-cdr-app \
  --resource-group teams-cdr-rg \
  --plan teams-cdr-plan \
  --runtime "NODE|18-lts"
```

#### Step 4: Configure Environment Variables

```bash
az webapp config appsettings set \
  --name teams-cdr-app \
  --resource-group teams-cdr-rg \
  --settings \
    TENANT_ID="your-tenant-id" \
    CLIENT_ID="your-client-id" \
    CLIENT_SECRET="your-client-secret" \
    GRAPH_SCOPES="https://graph.microsoft.com/.default" \
    NODE_ENV="production" \
    PORT="8080"
```

#### Step 5: Deploy Application

```bash
# Build the application
npm run build

# Deploy
az webapp up \
  --name teams-cdr-app \
  --resource-group teams-cdr-rg \
  --runtime "NODE|18-lts"
```

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY dist ./dist

ENV NODE_ENV=production
ENV PORT=8080

EXPOSE 8080

CMD ["node", "dist/server/index.js"]
```

### Build and Deploy

```bash
# Build
docker build -t teams-cdr-template .

# Run locally
docker run -p 8080:8080 \
  -e TENANT_ID="your-tenant-id" \
  -e CLIENT_ID="your-client-id" \
  -e CLIENT_SECRET="your-client-secret" \
  teams-cdr-template
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TENANT_ID` | Azure AD Tenant ID | Yes |
| `CLIENT_ID` | Application Client ID | Yes |
| `CLIENT_SECRET` | Client Secret Value | Yes |
| `GRAPH_SCOPES` | Graph API Scopes | Yes |
| `NODE_ENV` | Environment | No |
| `PORT` | Server Port | No |

## Security Best Practices

1. **Use HTTPS only**
2. **Store secrets in Azure Key Vault**
3. **Enable managed identity**
4. **Set up CORS properly**
5. **Enable Application Insights**
6. **Regular security updates**

## Monitoring

Enable Application Insights:

```bash
az monitor app-insights component create \
  --app teams-cdr-insights \
  --resource-group teams-cdr-rg \
  --location eastus
```

## Support

For deployment issues, review:
- Azure App Service documentation
- Deployment logs
- Environment variables
- Local production build test
