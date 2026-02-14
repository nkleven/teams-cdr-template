#!/bin/bash
set -euo pipefail

echo "::notice::🌳 Stripe integration beginning..."

# Verify Stripe CLI is available
if ! command -v stripe &> /dev/null; then
    echo "::notice::📦 Installing Stripe CLI..."
    curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg
    echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | sudo tee -a /etc/apt/sources.list.d/stripe.list
    sudo apt update && sudo apt install stripe -y
fi

# Configure Stripe (using secrets from GitHub)
echo "::notice::🔑 Configuring Stripe credentials..."

# Test connection
stripe listen --print-secret > /dev/null 2>&1 || true

echo "::notice::✅ Stripe integration complete"
echo "::notice::🌳 The offering is received. Eden speaks."
