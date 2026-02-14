# Teams CDR Template

A template application for viewing and analyzing Microsoft Teams Call Detail Records (CDR) using Microsoft Graph API, Node.js, TypeScript, and React.

## 🚀 Features

- **MS Graph Integration**: Access Teams call records via Microsoft Graph API
- **TypeScript**: Full TypeScript support for type safety
- **React Frontend**: Modern React application with hooks
- **Node.js Backend**: Express server with MS Graph SDK
- **Azure AD Authentication**: Secure authentication using MSAL
- **Call Records Dashboard**: View call history with details like duration, participants, and modalities

## 📋 Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Azure AD App Registration with the following:
  - Client ID
  - Client Secret
  - Tenant ID
  - API Permissions: `CallRecords.Read.All`

## 🔧 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/nkleven/teams-cdr-template.git
cd teams-cdr-template
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Copy the example environment file and fill in your Azure AD credentials:

```bash
cp .env.teams.example .env
```

Edit `.env` and add your Azure AD configuration:

```env
TENANT_ID=your_tenant_id_here
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
GRAPH_SCOPES=https://graph.microsoft.com/.default
PORT=3001
CLIENT_PORT=3000
NODE_ENV=development
```

### 4. Azure AD App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations** > **New registration**
3. Configure your app:
   - Name: Teams CDR Template
   - Supported account types: Accounts in this organizational directory only
   - Redirect URI: Not required for client credentials flow
4. After registration:
   - Copy the **Application (client) ID** to `CLIENT_ID`
   - Copy the **Directory (tenant) ID** to `TENANT_ID`
5. Create a client secret:
   - Go to **Certificates & secrets** > **New client secret**
   - Copy the secret value to `CLIENT_SECRET`
6. Add API permissions:
   - Go to **API permissions** > **Add a permission**
   - Select **Microsoft Graph** > **Application permissions**
   - Add `CallRecords.Read.All`
   - Click **Grant admin consent**

## 🚀 Running the Application

### Development Mode

Start both the backend server and frontend development server:

```bash
npm run dev
```

This will start:
- Backend server on `http://localhost:3001`
- Frontend development server on `http://localhost:3000`

### Production Build

Build the application:

```bash
npm run build
```

Start the production server:

```bash
npm start
```

## 📖 API Endpoints

### Authentication

- `POST /api/auth/token` - Get access token using client credentials

### Call Records

- `GET /api/graph/callrecords` - Get list of call records
- `GET /api/graph/callrecords/:id` - Get specific call record by ID
- `GET /api/graph/callrecords/:id/sessions` - Get sessions for a call record

## 🏗️ Project Structure

```
teams-cdr-template/
├── client/                 # React frontend
│   ├── components/         # React components
│   │   ├── AuthStatus.tsx
│   │   └── CallRecordsList.tsx
│   ├── services/           # API service layer
│   │   └── apiService.ts
│   ├── types/              # TypeScript type definitions
│   │   └── callRecord.ts
│   ├── App.tsx             # Main App component
│   ├── index.tsx           # React entry point
│   ├── index.html          # HTML template
│   └── styles.css          # Global styles
├── server/                 # Node.js backend
│   ├── routes/             # API routes
│   │   ├── auth.ts         # Authentication routes
│   │   └── graph.ts        # MS Graph API routes
│   └── index.ts            # Server entry point
├── dist/                   # Compiled output
├── tsconfig.json           # TypeScript configuration
├── tsconfig.server.json    # Server TypeScript config
├── webpack.config.js       # Webpack configuration
└── package.json            # Dependencies and scripts
```

## 🔒 Security

- Never commit your `.env` file with real credentials
- Store secrets securely in Azure Key Vault for production
- Use least-privilege principle for API permissions
- Implement proper error handling and logging
- Regularly rotate client secrets

## 📚 Resources

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/)
- [Call Records API Reference](https://docs.microsoft.com/en-us/graph/api/resources/callrecords-api-overview)
- [MSAL Node Documentation](https://github.com/AzureAD/microsoft-authentication-library-for-js/tree/dev/lib/msal-node)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Microsoft Graph API team
- Microsoft Teams platform
- React and TypeScript communities

---

Built with ❤️ using Microsoft Graph, Node.js, TypeScript, and React
