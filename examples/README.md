# Eden Agent Examples

This directory contains example scripts demonstrating various features of the Eden Agent.

## Examples

### advanced_features.py

Demonstrates the advanced features added in v0.1.0-beta.1:

1. **Basic Agent Usage** - Simple chat with built-in tools
2. **Custom Tool Registration** - Creating and registering custom tools
3. **Tool Management** - Registering, listing, and unregistering tools
4. **Rate Limiting** - Automatic API rate limiting to prevent throttling
5. **Retry Logic** - Automatic retry with exponential backoff for API failures
6. **Configuration** - Overview of configuration settings

## Running Examples

Make sure you have installed the package and configured your `.env` file:

```bash
# Install package
pip install -e ".[dev]"


# Run examples
python examples/advanced_features.py
```

## Creating Custom Tools

Custom tools must inherit from `BaseTool` and implement two methods:

```python
from src.tools.base import BaseTool, ToolDefinition

class MyCustomTool(BaseTool):
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="my_tool",
            description="Description of what the tool does",
            input_schema={
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "Parameter description"
                    }
                },
                "required": ["param1"]
            }
        )
    
    async def execute(self, param1: str) -> str:
        # Tool implementation
        return f"Result: {param1}"
```

Then register it with the agent:

```python
agent = Agent()
agent.register_tool(MyCustomTool())
```

## Configuration

### Rate Limiting

Control API request rate to avoid hitting limits:

```env
RATE_LIMIT_ENABLED=true
RATE_LIMIT_MAX_CALLS=50
RATE_LIMIT_TIME_WINDOW=60.0
```

### Retry Logic

Automatically retry failed API calls with exponential backoff:

```env
RETRY_ENABLED=true
RETRY_MAX_ATTEMPTS=3
RETRY_BASE_DELAY=1.0
RETRY_MAX_DELAY=60.0
```

## Best Practices

1. **Tool Design**: Keep tools focused and single-purpose
2. **Error Handling**: Let tools raise exceptions - the agent will handle them
3. **Rate Limiting**: Enable rate limiting to avoid API throttling
4. **Retry Logic**: Enable retries for production resilience
5. **Monitoring**: Use health checks to monitor system status

## Error Handling

The agent provides a structured way to handle errors. You can raise an `AgentError` with a custom message:

```python
from src.agent import AgentError

try:
    # Some API call
except SomeAPIException as e:
    raise AgentError(f"API error occurred: {e.message}") from e
```

## Troubleshooting

### SSL Certificate Errors

If you encounter SSL certificate verification errors like:
- `SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]`
- `urllib3.exceptions.SSLError`
- Certificate validation failures

**Solutions:**

1. **Update certificates** (Recommended):
```bash
# On macOS
/Applications/Python\ 3.x/Install\ Certificates.command

# On Windows - Update certifi
pip install --upgrade certifi

# On Linux
sudo apt-get install ca-certificates  # Debian/Ubuntu
sudo yum install ca-certificates      # RHEL/CentOS
```

2. **Environment variable** (Temporary fix):
```bash
# Point to system certificates
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt  # Linux
export SSL_CERT_FILE=/etc/ssl/cert.pem                    # macOS
```

3. **Configure in code** (Last resort - use cautiously):
```python
import os
import certifi

# Use certifi's certificate bundle
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
```

**⚠️ Warning**: Never disable SSL verification in production:
```python
# DON'T DO THIS IN PRODUCTION
verify=False  # This is insecure!
```

### Corporate Proxy/Firewall Issues

If you're behind a corporate firewall:

```bash
# Set proxy environment variables
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# Or in your .env file
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080
```

For more troubleshooting, see [TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md).
