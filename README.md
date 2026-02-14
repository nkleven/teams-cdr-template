# CDR Dashboard Template for Microsoft Teams

A ready-to-customize call reporting dashboard that can be hosted as a web app and added to Microsoft Teams as a tab.

This project is a web app (Vite + TypeScript). It does not include a Teams app manifest or Teams SDK code, but it is built to be embedded in Teams once you host it over HTTPS.

## Who this is for
- Teams admins and developers who want a dashboard tab inside Teams.
- Businesses that want a simple, modern UI for call detail records (CDR).

## What you get
- Setup wizard and first-run experience
- Call activity dashboard with success/failure indicators
- Admin area for users and settings
- Dark mode
- SIP ladder visualization

## Prerequisites
- Node.js 18+ and npm
- An HTTPS hosting location for production (required by Teams)
- Azure resources if you plan to use the built-in integrations:
  - Azure AD B2C
  - Azure Functions API
  - Power BI (optional)
  - Azure Key Vault (optional)

## Quick start (local)
1. Install dependencies:
   ```bash
   npm install
   ```
2. Create a local environment file:
   - Copy `.env.example` to `.env`.
   - Fill in any values you plan to use now.
3. Run the app:
   ```bash
   npm run dev
   ```
4. Open the local URL shown in your terminal (usually `http://localhost:5173`).

## Configure the app
All configuration is done with environment variables. Use `.env.example` as a guide.

Key settings:
- `VITE_AZURE_CLIENT_ID`
- `VITE_AZURE_AUTHORITY`
- `VITE_AZURE_KNOWN_AUTHORITY`
- `VITE_AZURE_API_SCOPE`
- `VITE_API_BASE_URL`
- `VITE_POWERBI_*` (optional)
- `VITE_KEYVAULT_URL` (optional)

## Build for production
1. Build the app:
   ```bash
   npm run build
   ```
2. Host the contents of `dist/` on your web server or static host.
3. Make sure the site is reachable via HTTPS.

## Add to Microsoft Teams as a tab
This template is a standard web app. To use it in Teams:
1. Host the app over HTTPS and copy the full URL (for example, `https://dashboard.yourcompany.com`).
2. Open the Teams Developer Portal.
3. Create a new app.
4. Add a **Tab**:
   - **Content URL**: your hosted app URL
   - **Website URL**: your hosted app URL
5. Add your domain to **Valid domains**.
6. Save and install the app to a team or chat.

If you want a more integrated experience (authentication, deep links, or context from Teams),
add the Microsoft Teams JavaScript SDK and update the app to read Teams context.

## Reset the first-run setup wizard
If you want to see the setup wizard again:
1. Open your browser dev tools.
2. Go to Application > Local Storage.
3. Clear the app's local storage.
4. Refresh the page.

## Tech stack
- Vite
- TypeScript
- Fluent UI styles

## Troubleshooting
Common issues:
- Blank screen in Teams: confirm the app is hosted over HTTPS and the domain is in the Teams app's valid domains list.
- Login issues: confirm Azure AD B2C values in `.env` match your tenant settings.
- API errors: check `VITE_API_BASE_URL` and confirm your Azure Functions endpoints are live.

## License
Use this template within your organization. Add a license file if you plan to distribute it publicly.
