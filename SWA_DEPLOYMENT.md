# Azure Static Web Apps Deployment Guide

## Overview
This project is configured for Azure Static Web Apps (SWA) with Azure Functions backend for the Eden Agent.

## Project Structure
```
/
├── index.html              # Frontend (static site)
├── accountant/             # Accountant landing page
├── api/                    # Azure Functions backend
│   ├── agent/              # Agent chat endpoint
│   ├── health/             # Health check endpoint
│   ├── host.json           # Functions host config
│   ├── requirements.txt    # Python dependencies
│   └── local.settings.json # Local environment config
├── staticwebapp.config.json # SWA routing & auth config
├── swa-cli.config.json      # SWA CLI config
└── package.json             # NPM scripts
```

## Prerequisites
- Node.js (v18 or higher)
- Python 3.9+
- Azure Functions Core Tools
- Azure account with Static Web Apps resource

## Local Development Setup

### 1. Install Dependencies
```bash
# Install SWA CLI and frontend dependencies
npm install

# Install Python dependencies for API
cd api
pip install -r requirements.txt
cd ..
```

### 2. Configure Environment
Create `api/local.settings.json` with:
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "ANTHROPIC_API_KEY": "your-api-key-here"
  }
}
```

### 3. Start Local Development Server
```bash
# Start both frontend and API
npm start

# Or start separately:
# Frontend: swa start . --api-location api
# API only: cd api && func start
```

Access the app at: `http://localhost:4280`

## Authentication

### Built-in Providers (Pre-configured)
- **GitHub**: `/.auth/login/github`
- **Microsoft Entra ID**: `/.auth/login/aad`

### Authentication Flow
1. User visits `/login` → redirects to GitHub OAuth
2. After authentication, user gets `authenticated` role
3. API endpoints require authentication (except `/api/health`)
4. Check auth status: `GET /.auth/me`

### Custom Login/Logout Links
```html
<a href="/login">Login</a>
<a href="/logout">Logout</a>
```

## API Endpoints

### Agent Chat (Authenticated)
```
POST /api/agent
Body: {
  "message": "Your message here",
  "session_id": "optional-session-id"
}
```

### Health Check (Public)
```
GET /api/health
Response: {
  "status": "healthy",
  "service": "Eden Agent API",
  "version": "0.1.0-beta.1"
}
```

## Deployment to Azure

### Option 1: SWA CLI Deployment
```bash
# Login to Azure
npx swa login

# Deploy
npm run deploy

# Follow prompts to select/create SWA resource
```

### Option 2: GitHub Actions (Automated)
1. Push code to GitHub
2. Connect repository in Azure Portal:
   - Go to your Static Web App resource
   - Settings → Deployment → Link GitHub repo
   - Azure creates workflow automatically

The workflow file will be: `.github/workflows/azure-static-web-apps-*.yml`

**Configuration:**
```yaml
app_location: "."          # Frontend source
api_location: "api"        # API source
output_location: "."       # Build output (static site)
```

### Option 3: Manual Deployment via Portal
1. Azure Portal → Create Static Web App
2. Link to your GitHub repository
3. Configure build settings:
   - App location: `.`
   - API location: `api`
   - Output location: `.`

## Configuration Files

### staticwebapp.config.json
Controls routing, authentication, and headers:
- API routes require authentication
- Health endpoint is public
- GitHub login configured
- Security headers enabled

### swa-cli.config.json
Local development configuration:
- App location: current directory
- API location: `api` folder
- Resource group and app name for deployment

## Troubleshooting

### 404 Errors Locally
- Ensure `staticwebapp.config.json` is at project root
- Check `outputLocation` in `swa-cli.config.json`

### API Not Found
- Verify `api/` folder structure
- Check `function.json` files are present
- Ensure Python dependencies are installed

### Authentication Issues
- Check routes in `staticwebapp.config.json`
- Test auth endpoint: `curl http://localhost:4280/.auth/me`
- Review browser console for redirect errors

### Environment Variables
- Local: Use `api/local.settings.json`
- Azure: Configure in Portal → Configuration → Application settings

## Frontend Integration

The frontend automatically calls the API using relative paths:
```javascript
// Example from agent-client.js
const response = await fetch('/api/agent', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: userMessage })
});
```

## Security Features

- **Content Security Policy**: Restricts script/style sources
- **Authentication Required**: All API endpoints (except health)
- **Auto-redirect on 401**: Sends users to login
- **HTTPS Only**: Enforced in production
- **Built-in DDoS Protection**: Azure provides automatic protection

## Monitoring & Logs

### Local Development
- Frontend logs: Browser console
- API logs: Terminal output from `func start`

### Production
- Azure Portal → Your Static Web App → Logs
- Application Insights (if configured)
- Functions monitoring for API performance

## Next Steps

1. **Install Dependencies**: Run `npm install` and install Python packages
2. **Configure API Key**: Add your Anthropic API key to `api/local.settings.json`
3. **Test Locally**: Run `npm start` and test at http://localhost:4280
4. **Deploy**: Use `npm run deploy` or connect GitHub repository
5. **Configure Production**: Add environment variables in Azure Portal

## Resources

- [Azure Static Web Apps Docs](https://docs.microsoft.com/azure/static-web-apps/)
- [SWA CLI Documentation](https://azure.github.io/static-web-apps-cli/)
- [Azure Functions Python Guide](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)
- [Eden Agent Documentation](README.md)
