#!/usr/bin/env python3
"""Quick test script to verify calculator security fix."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.tools.calculator import CalculatorTool


async def test_calculator():
    """Test the safe calculator implementation."""
    calc = CalculatorTool()
    
    print("Testing Safe Calculator Implementation")
    print("=" * 50)
    
    test_cases = [
        # Valid math expressions
        ("2 + 2", 4),
        ("10 * 5", 50),
        ("100 / 4", 25),
        ("2 ** 3", 8),
        ("15 % 4", 3),
        ("17 // 5", 3),
        ("(2 + 3) * 4", 20),
        ("-5 + 10", 5),
        
        # Should fail - unsafe operations
        ("__import__('os').system('ls')", "error"),
        ("eval('2+2')", "error"),
        ("open('/etc/passwd')", "error"),
        ("[x for x in range(10)]", "error"),
    ]
    
    passed = 0
    failed = 0
    
    for expression, expected in test_cases:
        try:
            result = await calc.execute(expression)
            
            if "error" in result:
                if expected == "error":
                    print(f"✅ PASS (blocked): {expression}")
                    print(f"   Error: {result['error']}")
                    passed += 1
                else:
                    print(f"❌ FAIL: {expression}")
                    print(f"   Got error: {result['error']}")
                    print(f"   Expected: {expected}")
                    failed += 1
            else:
                actual = result["result"]
                if abs(actual - expected) < 0.0001:  # Float comparison
                    print(f"✅ PASS: {expression} = {actual}")
                    passed += 1
                else:
                    print(f"❌ FAIL: {expression}")
                    print(f"   Got: {actual}")
                    print(f"   Expected: {expected}")
                    failed += 1
                    
        except Exception as e:
            if expected == "error":
                print(f"✅ PASS (exception): {expression}")
                print(f"   Exception: {e}")
                passed += 1
            else:
                print(f"❌ FAIL: {expression}")
                print(f"   Unexpected exception: {e}")
                failed += 1
        
        print()
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = asyncio.run(test_calculator())
    sys.exit(0 if success else 1)
