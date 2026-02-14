# Quick Start Guide

Get started with the Teams CDR Template in 5 minutes!

## Step 1: Prerequisites Check

Make sure you have:
- ✅ Node.js v18+ installed (`node --version`)
- ✅ npm installed (`npm --version`)
- ✅ Access to Azure Portal with admin permissions

## Step 2: Azure AD Setup (5 minutes)

### Create App Registration

1. Go to https://portal.azure.com
2. Navigate to **Azure Active Directory** → **App registrations** → **New registration**
3. Fill in:
   - **Name**: `Teams CDR Template`
   - **Supported account types**: `Accounts in this organizational directory only`
4. Click **Register**

### Get Your Credentials

Copy these values:
- **Application (client) ID** ← This is your `CLIENT_ID`
- **Directory (tenant) ID** ← This is your `TENANT_ID`

### Create Client Secret

1. Go to **Certificates & secrets** → **New client secret**
2. Add description: `Teams CDR Secret`
3. Set expiration: `6 months` (or per your policy)
4. Click **Add**
5. **IMPORTANT**: Copy the **Value** immediately ← This is your `CLIENT_SECRET`

### Add Permissions

1. Go to **API permissions** → **Add a permission**
2. Select **Microsoft Graph** → **Application permissions**
3. Search and add: `CallRecords.Read.All`
4. Click **Grant admin consent for [Your Org]** ✅

## Step 3: Install & Configure (2 minutes)

```bash
# Clone the repository
git clone https://github.com/nkleven/teams-cdr-template.git
cd teams-cdr-template

# Install dependencies
npm install

# Create environment file
cp .env.teams.example .env

# Edit .env with your credentials
nano .env  # or use your favorite editor
```

Add your values to `.env`:
```env
TENANT_ID=your-tenant-id-from-step-2
CLIENT_ID=your-client-id-from-step-2
CLIENT_SECRET=your-client-secret-from-step-2
GRAPH_SCOPES=https://graph.microsoft.com/.default
PORT=3001
NODE_ENV=development
```

## Step 4: Start the Application (1 minute)

```bash
# Start both frontend and backend
npm run dev
```

You should see:
```
Server is running on http://localhost:3001
webpack compiled successfully
```

## Step 5: Use the Application

1. Open browser to `http://localhost:3000`
2. Click **"Login with Azure AD"** button
3. Click **"Fetch Call Records"** button
4. View your Teams call records! 🎉

## Expected Result

You should see a table with:
- Start Time
- End Time
- Duration (calculated)
- Call Type
- Modalities (audio, video, etc.)
- Call ID

## Troubleshooting

### "Authentication failed"
- ✅ Verify your CLIENT_ID, CLIENT_SECRET, and TENANT_ID are correct
- ✅ Check that admin consent was granted for CallRecords.Read.All
- ✅ Make sure the client secret hasn't expired

### "Failed to fetch call records"
- ✅ Verify you have Teams call records in your tenant
- ✅ Check that the API permission was granted correctly
- ✅ Look at browser console (F12) for detailed error messages

### "Module not found" errors
- ✅ Run `npm install` again
- ✅ Delete `node_modules` and run `npm install` from scratch

### Port already in use
- ✅ Change PORT in .env to a different value (e.g., 3002)
- ✅ Or kill the process using that port

## Next Steps

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🔧 Customize the UI in `client/components/`
- 🚀 Deploy to Azure (see deployment guides)
- 🔐 Set up production secrets in Azure Key Vault

## Support

If you run into issues:
1. Check the [README.md](README.md) troubleshooting section
2. Review the [Microsoft Graph documentation](https://docs.microsoft.com/en-us/graph/)
3. Open an issue on GitHub

---

**Time to complete**: ~10 minutes
**Difficulty**: Beginner-friendly
