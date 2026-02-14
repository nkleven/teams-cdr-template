"""Calculator tool for mathematical operations."""

import ast
import operator
from typing import Any
from .base import BaseTool, ToolDefinition
from ..tracing.tracer import tracer


class CalculatorTool(BaseTool):
    """Tool for performing calculations."""
    
    # Safe operators for math evaluation
    SAFE_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="calculator",
            description="Perform mathematical calculations. Supports basic arithmetic operations (+, -, *, /, **, %, //).",
            input_schema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5', '2 ** 3')"
                    }
                },
                "required": ["expression"]
            }
        )
    
    def _safe_eval(self, node: ast.AST) -> float:
        """Safely evaluate an AST node with only allowed operations."""
        if isinstance(node, ast.Constant):  # Python 3.8+
            return float(node.value)
        elif isinstance(node, ast.Num):  # Python 3.7 compatibility
            return float(node.n)
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self.SAFE_OPERATORS:
                raise ValueError(f"Unsupported operation: {op_type.__name__}")
            left = self._safe_eval(node.left)
            right = self._safe_eval(node.right)
            return self.SAFE_OPERATORS[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self.SAFE_OPERATORS:
                raise ValueError(f"Unsupported operation: {op_type.__name__}")
            operand = self._safe_eval(node.operand)
            return self.SAFE_OPERATORS[op_type](operand)
        elif isinstance(node, ast.Expression):
            return self._safe_eval(node.body)
        else:
            raise ValueError(f"Unsupported expression type: {type(node).__name__}")
    
    async def execute(self, expression: str) -> Any:
        """Execute the calculation safely using AST parsing."""
        with tracer.trace_operation(
            "calculator_execute",
            attributes={"expression": expression}
        ):
            try:
                # Parse expression into AST
                tree = ast.parse(expression, mode='eval')
                # Safely evaluate the AST
                result = self._safe_eval(tree)
                return {"result": result, "expression": expression}
            except (SyntaxError, ValueError, ZeroDivisionError, TypeError) as e:
                return {"error": str(e), "expression": expression}
            except Exception as e:
                return {"error": f"Calculation error: {str(e)}", "expression": expression}
