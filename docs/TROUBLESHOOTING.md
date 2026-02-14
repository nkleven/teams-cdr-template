# Troubleshooting Guide

Common issues and solutions for Eden Agent development.

## 🔒 SSL/Certificate Issues

### Problem: Certificate Verification Failed

**Error messages:**
```
SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
requests.exceptions.SSLError: HTTPSConnectionPool
urllib3.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**Root causes:**
- Outdated system certificates
- Missing CA certificates
- Corporate firewall/proxy intercepting SSL
- Python not configured with proper certificate bundle

### Solutions

#### 1. Update System Certificates (Recommended)

**macOS:**
```bash
# Run the Install Certificates command
/Applications/Python\ 3.11/Install\ Certificates.command

# Or manually with certifi
pip install --upgrade certifi
python -c "import certifi; print(certifi.where())"
```

**Windows:**
```bash
# Update certifi package
pip install --upgrade certifi pip

# Verify certificate location
python -c "import certifi; print(certifi.where())"
```

**Linux (Ubuntu/Debian):**
```bash
# Update CA certificates
sudo apt-get update
sudo apt-get install --reinstall ca-certificates

# Update certifi
pip install --upgrade certifi
```

**Linux (RHEL/CentOS):**
```bash
sudo yum reinstall ca-certificates
pip install --upgrade certifi
```

#### 2. Configure Certificate Path

Add to your `.env` file:

```env
# Point to certificate bundle
SSL_CERT_FILE=/path/to/certifi/cacert.pem
REQUESTS_CA_BUNDLE=/path/to/certifi/cacert.pem

# Find the path with:
# python -c "import certifi; print(certifi.where())"
```

Or set in your shell:

```bash
# Temporary (current session)
export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")
export REQUESTS_CA_BUNDLE=$SSL_CERT_FILE

# Permanent (add to ~/.bashrc or ~/.zshrc)
echo 'export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")' >> ~/.bashrc
```

#### 3. Configure in Code

```python
import os
import certifi
import httpx

# Set certificate bundle globally
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# Or configure client directly
client = httpx.Client(verify=certifi.where())
```

#### 4. Corporate Environment

If behind a corporate proxy with SSL inspection:

```python
# Get corporate certificate
# Usually provided by IT department as .crt or .pem file

# Option A: Add to certifi bundle
import certifi
corporate_cert = '/path/to/corporate-cert.crt'
bundle = certifi.where()

with open(bundle, 'ab') as f:
    with open(corporate_cert, 'rb') as cert:
        f.write(cert.read())

# Option B: Create custom bundle
import ssl
context = ssl.create_default_context()
context.load_verify_locations('/path/to/corporate-bundle.pem')
```

#### 5. Proxy Configuration

```bash
# Set proxy environment variables
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1,.company.com

# With authentication
export HTTPS_PROXY=http://user:password@proxy.company.com:8080
```

In `.env` file:
```env
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080
NO_PROXY=localhost,127.0.0.1
```

### ⚠️ What NOT to Do

**Never disable SSL verification in production:**

```python
# INSECURE - DO NOT USE
import httpx
client = httpx.Client(verify=False)  # ❌ Never do this!

import requests
requests.get(url, verify=False)  # ❌ Never do this!

import ssl
ssl._create_unverified_context()  # ❌ Never do this!
```

**Why?** This exposes you to man-in-the-middle attacks and data interception.

---

## 🔑 API Authentication Issues

### Problem: Invalid API Key

**Error:**
```
AuthenticationError: Invalid API key
401 Unauthorized
```

**Solutions:**

1. **Verify API key format:**
```bash
# Anthropic keys start with 'sk-ant-'
echo $ANTHROPIC_API_KEY
# Should output: sk-ant-api03-...
```

2. **Check .env file:**
```env
# Make sure there are no quotes or extra spaces
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx  # ✓ Correct
ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"  # ✗ May cause issues
```

3. **Reload environment:**
```bash
# After changing .env
source .env  # Linux/macOS
# Or restart your terminal/IDE
```

---

## 📦 Installation Issues

### Problem: Module Not Found

**Error:**
```
ImportError: No module named 'src'
ModuleNotFoundError: No module named 'src.agent'
```

**Solutions:**

```bash
# Reinstall in editable mode
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"

# Verify installation
pip list | grep eden
python -c "import src; print(src.__file__)"
```

### Problem: Dependency Conflicts

**Error:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```

**Solutions:**

```bash
# Create fresh virtual environment
deactivate
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install with explicit versions
pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
```

---

## 🚦 Rate Limiting Issues

### Problem: Too Many Requests

**Error:**
```
RateLimitError: Rate limit exceeded
429 Too Many Requests
```

**Solutions:**

1. **Adjust rate limits in .env:**
```env
RATE_LIMIT_ENABLED=true
RATE_LIMIT_MAX_CALLS=30  # Reduce from 50
RATE_LIMIT_TIME_WINDOW=60.0  # Increase window
```

2. **Add delays in code:**
```python
import asyncio

for i in range(10):
    response = await agent.chat(f"Message {i}")
    await asyncio.sleep(2)  # Add 2 second delay
```

---

## 🔄 Retry Logic Issues

### Problem: Constant Retries

**Error:**
```
Max retries exceeded
Connection timeout after multiple attempts
```

**Solutions:**

```env
# Adjust retry settings
RETRY_ENABLED=true
RETRY_MAX_ATTEMPTS=5  # Increase attempts
RETRY_BASE_DELAY=2.0  # Longer initial delay
RETRY_MAX_DELAY=120.0  # Longer max delay
```

---

## 🪵 Debugging Tips

### Enable Debug Logging

```env
LOG_LEVEL=DEBUG
```

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check API Connectivity

```python
import httpx

# Test basic connectivity
response = httpx.get('https://api.anthropic.com')
print(response.status_code)

# Test with certificates
import certifi
client = httpx.Client(verify=certifi.where())
response = client.get('https://api.anthropic.com')
```

### Inspect Environment

```python
import os
print("Python:", sys.version)
print("SSL_CERT_FILE:", os.environ.get('SSL_CERT_FILE'))
print("Certifi:", certifi.where())
print("Working dir:", os.getcwd())
```

---

## 📞 Getting Help

If issues persist:

1. **Check logs:** Look for detailed error messages
2. **Search issues:** Check GitHub issues for similar problems
3. **Create issue:** Include:
   - Error message (full traceback)
   - Python version: `python --version`
   - OS and version
   - Steps to reproduce
   - Relevant configuration

---

## 🔍 Quick Diagnostic Script

Run this to diagnose common issues:

```python
# diagnostic.py
import sys
import os
import certifi
import platform

print("=== System Information ===")
print(f"Python: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Working Directory: {os.getcwd()}")

print("\n=== SSL Configuration ===")
print(f"Certifi: {certifi.where()}")
print(f"SSL_CERT_FILE: {os.environ.get('SSL_CERT_FILE', 'Not set')}")
print(f"REQUESTS_CA_BUNDLE: {os.environ.get('REQUESTS_CA_BUNDLE', 'Not set')}")

print("\n=== Environment Variables ===")
print(f"ANTHROPIC_API_KEY: {'Set' if os.environ.get('ANTHROPIC_API_KEY') else 'Not set'}")
print(f"HTTP_PROXY: {os.environ.get('HTTP_PROXY', 'Not set')}")
print(f"HTTPS_PROXY: {os.environ.get('HTTPS_PROXY', 'Not set')}")

print("\n=== Package Versions ===")
try:
    import anthropic
    print(f"anthropic: {anthropic.__version__}")
except ImportError:
    print("anthropic: Not installed")

try:
    import httpx
    print(f"httpx: {httpx.__version__}")
except ImportError:
    print("httpx: Not installed")

print("\n=== Connectivity Test ===")
try:
    import httpx
    response = httpx.get('https://api.anthropic.com', timeout=5)
    print(f"API connectivity: OK ({response.status_code})")
except Exception as e:
    print(f"API connectivity: FAILED - {e}")
```

Run with: `python diagnostic.py`
