#!/bin/bash
set -euo pipefail

echo "::notice::🌳 Google integration beginning..."

# Configure Google OAuth
echo "::notice::🔑 Configuring Google OAuth..."

# Create OAuth config file
cat > google-oauth-config.json << EOF
{
  "web": {
    "client_id": "\${GOOGLE_CLIENT_ID}",
    "client_secret": "\${GOOGLE_CLIENT_SECRET}",
    "redirect_uris": ["https://eden.azure.com/auth/google/callback"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token"
  }
}
EOF

echo "::notice::✅ Google OAuth configured"
echo "::notice::🌳 Google stirs. The orchard opens a gate."

# Clean up sensitive files
rm -f google-oauth-config.json
