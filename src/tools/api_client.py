"""API client tool for making HTTP requests."""

import asyncio
import aiohttp
from typing import Any, Dict, Optional
from .base import BaseTool, ToolDefinition


class APIClientTool(BaseTool):
    """Tool for making HTTP requests to external APIs."""
    
    def __init__(self, timeout: int = 10):
        """Initialize the API client tool.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="api_client",
            description="Make HTTP requests to external APIs (GET, POST, PUT, DELETE)",
            input_schema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The API endpoint URL"
                    },
                    "method": {
                        "type": "string",
                        "enum": ["GET", "POST", "PUT", "DELETE"],
                        "description": "HTTP method to use",
                        "default": "GET"
                    },
                    "headers": {
                        "type": "object",
                        "description": "Optional HTTP headers",
                        "default": {}
                    },
                    "body": {
                        "type": "object",
                        "description": "Optional request body for POST/PUT",
                        "default": {}
                    },
                    "params": {
                        "type": "object",
                        "description": "Optional query parameters",
                        "default": {}
                    }
                },
                "required": ["url"]
            }
        )
    
    async def execute(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        body: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Execute an HTTP request.
        
        Args:
            url: API endpoint URL
            method: HTTP method
            headers: Optional HTTP headers
            body: Optional request body
            params: Optional query parameters
            
        Returns:
            Response data including status, headers, and body
        """
        headers = headers or {}
        params = params or {}
        
        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=body if body else None,
                    params=params
                ) as response:
                    try:
                        response_data = await response.json()
                    except:
                        response_data = await response.text()
                    
                    return {
                        "status": response.status,
                        "success": 200 <= response.status < 300,
                        "headers": dict(response.headers),
                        "data": response_data,
                        "url": str(response.url)
                    }
        
        except asyncio.TimeoutError:
            return {
                "status": 408,
                "success": False,
                "error": f"Request timeout after {self.timeout} seconds"
            }
        except aiohttp.ClientError as e:
            return {
                "status": 0,
                "success": False,
                "error": f"Client error: {str(e)}"
            }
        except Exception as e:
            return {
                "status": 0,
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
