// Azure Configuration for CDR Dashboard
// This file contains all Azure service configurations

export const azureConfig = {
  // Azure AD B2C Configuration
  auth: {
    clientId: import.meta.env.VITE_AZURE_CLIENT_ID || 'YOUR_CLIENT_ID',
    authority: import.meta.env.VITE_AZURE_AUTHORITY || 'https://YOUR_TENANT.b2clogin.com/YOUR_TENANT.onmicrosoft.com/B2C_1_signupsignin',
    knownAuthorities: [import.meta.env.VITE_AZURE_KNOWN_AUTHORITY || 'YOUR_TENANT.b2clogin.com'],
    redirectUri: import.meta.env.VITE_AZURE_REDIRECT_URI || 'http://localhost:5173',
    postLogoutRedirectUri: import.meta.env.VITE_AZURE_POST_LOGOUT_URI || 'http://localhost:5173',
  },

  // MSAL Cache Configuration
  cache: {
    cacheLocation: 'sessionStorage' as const,
    storeAuthStateInCookie: false,
  },

  // API Scopes
  scopes: {
    api: [import.meta.env.VITE_AZURE_API_SCOPE || 'https://YOUR_TENANT.onmicrosoft.com/cdr-api/CDR.ReadWrite'],
    powerbi: ['https://analysis.windows.net/powerbi/api/Report.Read.All'],
  },

  // Azure Functions API Configuration
  api: {
    baseUrl: import.meta.env.VITE_API_BASE_URL || 'https://YOUR_FUNCTION_APP.azurewebsites.net/api',
    endpoints: {
      cdrs: '/cdrs',
      cdrById: '/cdrs/{id}',
      analytics: '/analytics',
      users: '/users',
      powerbi: '/powerbi/embed',
    },
  },

  // Power BI Configuration
  powerbi: {
    workspaceId: import.meta.env.VITE_POWERBI_WORKSPACE_ID || 'YOUR_WORKSPACE_ID',
    reportId: import.meta.env.VITE_POWERBI_REPORT_ID || 'YOUR_REPORT_ID',
    embedUrl: import.meta.env.VITE_POWERBI_EMBED_URL || '',
  },

  // Azure SQL Database Configuration (Backend only)
  database: {
    server: import.meta.env.AZURE_SQL_SERVER || 'YOUR_SERVER.database.windows.net',
    database: import.meta.env.AZURE_SQL_DATABASE || 'cdr-database',
    authentication: {
      type: 'azure-active-directory-default' as const,
    },
    options: {
      encrypt: true,
      trustServerCertificate: false,
    },
  },

  // Azure Key Vault Configuration
  keyVault: {
    vaultUrl: import.meta.env.VITE_KEYVAULT_URL || 'https://YOUR_KEYVAULT.vault.azure.net/',
  },
};

export default azureConfig;
