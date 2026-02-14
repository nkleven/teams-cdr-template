"""Base tool interface for AI agent."""

from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel


class ToolDefinition(BaseModel):
    """Tool definition for Claude."""
    name: str
    description: str
    input_schema: Dict[str, Any]


class BaseTool(ABC):
    """Base class for agent tools."""
    
    @property
    @abstractmethod
    def definition(self) -> ToolDefinition:
        """Return the tool definition."""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters."""
        pass
