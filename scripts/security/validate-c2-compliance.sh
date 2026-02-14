#!/bin/bash
set -euo pipefail

# 🌳 Eden C2 Compliance Validator
# Ensures Microsoft C2 confidential information standards
# The Bridge guards. Logos validates. Bud watches the gate.

echo "::notice::🔒 C2 Compliance validation begins..."

ENVIRONMENT="${1:-development}"
FAILED_CHECKS=0

# Check 1: Encryption at Rest
echo "::group::Validating encryption at rest"
if [ "$ENVIRONMENT" = "production" ] || [ "$ENVIRONMENT" = "staging" ]; then
    if [ -z "${AZURE_KEY_VAULT_URI:-}" ]; then
        echo "::error::Azure Key Vault not configured for $ENVIRONMENT"
        ((FAILED_CHECKS++))
    else
        echo "✅ Azure Key Vault configured"
    fi
fi
echo "::endgroup::"

# Check 2: Access Controls
echo "::group::Validating access controls"
if [ -z "${AZURE_TENANT_ID:-}" ]; then
    echo "::error::Azure AD tenant not configured"
    ((FAILED_CHECKS++))
else
    echo "✅ Azure AD tenant configured"
fi
echo "::endgroup::"

# Check 3: Encryption in Transit
echo "::group::Validating TLS configuration"
if [ "$ENVIRONMENT" != "development" ]; then
    if [ -z "${TLS_CERT_PATH:-}" ]; then
        echo "::warning::TLS certificate path not set - ensure HTTPS enforced"
    else
        echo "✅ TLS configuration present"
    fi
fi
echo "::endgroup::"

# Check 4: Audit Logging
echo "::group::Validating audit logging"
if [ -z "${LOG_ANALYTICS_WORKSPACE_ID:-}" ]; then
    echo "::warning::Log Analytics not configured - audit trail may be incomplete"
else
    echo "✅ Log Analytics configured"
fi
echo "::endgroup::"

# Check 5: Data Residency
echo "::group::Validating data residency"
AZURE_REGION="${AZURE_REGION:-eastus}"
if [[ ! "$AZURE_REGION" =~ ^(eastus|westus|northeurope|westeurope)$ ]]; then
    echo "::warning::Azure region '$AZURE_REGION' may not meet compliance requirements"
fi
echo "✅ Region: $AZURE_REGION"
echo "::endgroup::"

# Check 6: Secret Management
echo "::group::Validating secret management"
REQUIRED_SECRETS=(
    "AZURE_CLIENT_ID"
    "AZURE_TENANT_ID"
)

for secret in "${REQUIRED_SECRETS[@]}"; do
    if [ -z "${!secret:-}" ]; then
        echo "::error::Required secret $secret not found"
        ((FAILED_CHECKS++))
    fi
done

if [ $FAILED_CHECKS -eq 0 ]; then
    echo "✅ All required secrets configured"
fi
echo "::endgroup::"

# Summary
if [ $FAILED_CHECKS -eq 0 ]; then
    echo "::notice::🌳 C2 compliance validated. The orchard is secure."
    echo "::notice::🌳 Bud thumps once. The gate opens with confidence."
    exit 0
else
    echo "::error::🌳 C2 compliance failed: $FAILED_CHECKS checks failed"
    echo "::error::🌳 Bud whimpers. The gate remains closed."
    exit 1
fi
