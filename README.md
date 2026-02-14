# Teams CDR Template

> A template application for viewing and analyzing Microsoft Teams Call Detail Records (CDR) using Microsoft Graph API, Node.js, TypeScript, and React.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/nkleven/teams-cdr-template.git
cd teams-cdr-template

# Install dependencies
npm install

# Configure environment
cp .env.teams.example .env
# Edit .env with your Azure AD credentials

# Start development server
npm run dev
```

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Azure AD Setup](#azure-ad-setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Architecture](#architecture)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

This is a comprehensive template application that demonstrates how to build a Microsoft Teams Call Detail Records (CDR) viewer using modern web technologies. It integrates with Microsoft Graph API to fetch and display call records from Teams, providing insights into call history, duration, participants, and more.

### Problem Statement

Organizations using Microsoft Teams need visibility into their calling patterns and call history for:
- Compliance and auditing requirements
- Usage analytics and reporting
- Troubleshooting call quality issues
- Understanding communication patterns

### Solution

This template provides a ready-to-use application that:
- Authenticates with Azure AD using client credentials
- Fetches call records via Microsoft Graph API
- Displays call data in an intuitive, responsive UI
- Can be extended and customized for specific needs

## ✨ Features

- 🔐 **Azure AD Authentication**: Secure authentication using MSAL and client credentials flow
- 📊 **Call Records Dashboard**: View Teams call history with detailed information
- 🎯 **TypeScript**: Full type safety across frontend and backend (ESM enabled)
- ⚛️ **React Frontend**: Modern React application with hooks
- 🚀 **Node.js Backend**: Express server with MS Graph SDK integration
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🔄 **Real-time Data**: Fetch latest call records from Microsoft Graph
- 🎨 **Clean UI**: Beautiful gradient design with intuitive table layout
- 📁 **Stale Artifacts**: Note that the `src/` directory contains legacy/unrelated Python code; the active codebase is in `client/` and `server/`.

## Prerequisites

- **Node.js** (v18 or higher)
- **npm** or **yarn**
- **Azure AD App Registration** with:
  - Client ID
  - Client Secret
  - Tenant ID
  - API Permission: `CallRecords.Read.All`

## Installation

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

Copy the example environment file:

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

## Azure AD Setup

### Step 1: Create App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Configure:
   - **Name**: Teams CDR Template (or your preferred name)
   - **Supported account types**: Accounts in this organizational directory only
   - **Redirect URI**: Leave blank (not needed for client credentials flow)
5. Click **Register**

### Step 2: Get Credentials

1. On the app overview page, copy:
   - **Application (client) ID** → Use as `CLIENT_ID`
   - **Directory (tenant) ID** → Use as `TENANT_ID`

### Step 3: Create Client Secret

1. Go to **Certificates & secrets**
2. Click **New client secret**
3. Add a description and set expiration
4. Click **Add**
5. **Important**: Copy the secret **Value** immediately → Use as `CLIENT_SECRET`
   (You won't be able to see it again!)

### Step 4: Add API Permissions

1. Go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Select **Application permissions**
5. Search for and add: `CallRecords.Read.All`
6. Click **Add permissions**
7. Click **Grant admin consent for [Your Organization]**
8. Confirm the consent

### Step 5: Verify Setup

Your API permissions should show:
- **CallRecords.Read.All** (Application, Admin consented ✓)

## Usage

### Development Mode

Start both backend and frontend development servers:

```bash
# Note: Ensure you have run 'npm install'
npm run dev
```

> **Note for Windows users**: If you encounter issues with ESM modules (ERR_MODULE_NOT_FOUND), the `package.json` has been configured to use the `ts-node/esm` loader for development.

This will start:
- **Backend server** on `http://localhost:3001`
- **Frontend development server** on `http://localhost:3000`

The app will automatically open in your browser.

### Production Build

Build the application for production:

```bash
npm run build
```

This creates optimized builds in `dist/`:
- `dist/client/` - Frontend build
- `dist/server/` - Backend build

Start the production server:

```bash
npm start
```

### Using the Application

1. **Launch** the application at `http://localhost:3000`
2. **Click** "Login with Azure AD" to authenticate
3. **Click** "Fetch Call Records" to retrieve Teams call data
4. **View** call records in the table with:
   - Start and end times
   - Call duration
   - Call type
   - Modalities (audio, video, etc.)
   - Call ID

## API Endpoints

### Authentication

#### `POST /api/auth/token`

Get an access token using client credentials flow.

**Response:**
```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJub...",
  "expiresOn": "2024-02-14T23:00:00.000Z"
}
```

### Call Records

#### `GET /api/graph/callrecords`

Fetch a list of call records from Microsoft Graph.

**Headers:**
```
Authorization: Bearer {accessToken}
```

**Response:**
```json
{
  "callRecords": [
    {
      "id": "00000000-0000-0000-0000-000000000000",
      "version": 1,
      "type": "groupCall",
      "modalities": ["audio", "video"],
      "startDateTime": "2024-02-14T10:00:00Z",
      "endDateTime": "2024-02-14T10:30:00Z",
      ...
    }
  ],
  "nextLink": "https://graph.microsoft.com/beta/..."
}
```

#### `GET /api/graph/callrecords/:id`

Get details of a specific call record.

#### `GET /api/graph/callrecords/:id/sessions`

Get sessions for a specific call record.

## Architecture

```
teams-cdr-template/
├── client/                    # React frontend
│   ├── components/            # React components
│   │   ├── AuthStatus.tsx     # Authentication status UI
│   │   └── CallRecordsList.tsx # Call records table
│   ├── services/              # API service layer
│   │   └── apiService.ts      # API client
│   ├── types/                 # TypeScript type definitions
│   │   └── callRecord.ts      # Call record types
│   ├── App.tsx                # Main App component
│   ├── index.tsx              # React entry point
│   ├── index.html             # HTML template
│   └── styles.css             # Global styles
│
├── server/                    # Node.js/Express backend
│   ├── routes/                # API routes
│   │   ├── auth.ts            # Authentication endpoints
│   │   └── graph.ts           # MS Graph API endpoints
│   └── index.ts               # Server entry point
│
├── dist/                      # Compiled output
│   ├── client/                # Built frontend
│   └── server/                # Built backend
│
├── tsconfig.json              # TypeScript config (client)
├── tsconfig.server.json       # TypeScript config (server)
├── webpack.config.js          # Webpack configuration
├── package.json               # Dependencies and scripts
└── .env                       # Environment variables (not committed)
```

### Technology Stack

- **Frontend**: React 18, TypeScript 5
- **Backend**: Node.js, Express 4
- **Authentication**: MSAL Node
- **API**: Microsoft Graph Client
- **Build**: Webpack 5, TypeScript Compiler
- **Styling**: CSS3 with modern gradients

## Development

### Available Scripts

```bash
npm run dev              # Start development servers (client + server)
npm run client:dev       # Start frontend dev server only
npm run server:dev       # Start backend dev server only
npm run build            # Build for production
npm run build:client     # Build frontend only
npm run build:server     # Build backend only
npm start                # Start production server
npm run type-check       # Run TypeScript type checking
npm run lint             # Run ESLint
npm test                 # Run tests
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TENANT_ID` | Azure AD tenant ID | Yes |
| `CLIENT_ID` | Azure AD application (client) ID | Yes |
| `CLIENT_SECRET` | Azure AD client secret | Yes |
| `GRAPH_SCOPES` | Microsoft Graph scopes | Yes |
| `PORT` | Backend server port | No (default: 3001) |
| `CLIENT_PORT` | Frontend dev server port | No (default: 3000) |
| `NODE_ENV` | Environment (development/production) | No |

## 🔒 Security

- ⚠️ Never commit your `.env` file with real credentials
- 🔐 Store secrets securely in Azure Key Vault for production
- 🔑 Use least-privilege principle for API permissions
- 🔄 Regularly rotate client secrets
- 🛡️ Implement proper error handling and logging

## 📚 Resources

- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/)
- [Call Records API Reference](https://docs.microsoft.com/en-us/graph/api/resources/callrecords-api-overview)
- [MSAL Node Documentation](https://github.com/AzureAD/microsoft-authentication-library-for-js/tree/dev/lib/msal-node)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Microsoft Graph API team for excellent documentation
- Microsoft Teams platform for providing the API
- React and TypeScript communities

## 📞 Contact

- **Author**: nkleven
- **Repository**: [https://github.com/nkleven/teams-cdr-template](https://github.com/nkleven/teams-cdr-template)

---

<div align="center">
  Built with ❤️ using Microsoft Graph, Node.js, TypeScript, and React
</div>
