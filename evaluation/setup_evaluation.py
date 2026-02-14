"""
Setup script for Eden Agent Evaluation Framework
Validates environment and dependencies before running evaluation
"""

import sys
import os
from pathlib import Path


def check_api_key():
    """Check if API key is configured."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    
    if not api_key or api_key == "your_anthropic_api_key_here":
        print("❌ ANTHROPIC_API_KEY not configured")
        print("\n📝 To fix:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your Anthropic API key")
        print("   3. Run: python evaluation/setup_evaluation.py")
        return False
    
    print("✅ API Key configured")
    return True


def check_dependencies():
    """Check if required packages are installed."""
    required = {
        "azure.ai.evaluation": "azure-ai-evaluation",
        "azure.identity": "azure-identity",
        "matplotlib": "matplotlib",
        "pandas": "pandas"
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module.split(".")[0])
            print(f"✅ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} not installed")
    
    if missing:
        print(f"\n📦 Install missing packages:")
        print(f"   pip install {' '.join(missing)}")
        print("\n   Or install all evaluation dependencies:")
        print("   pip install -e '.[evaluation]'")
        return False
    
    return True


def check_test_files():
    """Check if test files exist."""
    eval_dir = Path(__file__).parent
    
    files = {
        "test_queries.json": "Test queries dataset",
        "collect_responses.py": "Response collection script",
        "run_evaluation.py": "Evaluation script"
    }
    
    all_exist = True
    for filename, description in files.items():
        filepath = eval_dir / filename
        if filepath.exists():
            print(f"✅ {description} ({filename})")
        else:
            print(f"❌ {description} missing ({filename})")
            all_exist = False
    
    return all_exist


def check_responses():
    """Check if responses have been collected."""
    eval_dir = Path(__file__).parent
    responses_file = eval_dir / "test_responses.json"
    
    if not responses_file.exists():
        print("⚠️  No responses collected yet")
        print("\n📝 Run: python evaluation/collect_responses.py")
        return False
    
    # Check if responses have actual data (not just errors)
    import json
    with open(responses_file) as f:
        responses = json.load(f)
    
    successful = sum(1 for r in responses if r.get("response") is not None)
    total = len(responses)
    
    if successful == 0:
        print(f"❌ All {total} responses failed (likely API key issue)")
        print("\n📝 To fix:")
        print("   1. Set valid ANTHROPIC_API_KEY in .env")
        print("   2. Re-run: python evaluation/collect_responses.py")
        return False
    
    print(f"✅ Responses collected ({successful}/{total} successful)")
    return True


def main():
    """Run all validation checks."""
    print("🔍 Eden Agent Evaluation Setup Validation")
    print("=" * 60)
    
    checks = [
        ("Environment", check_api_key),
        ("Dependencies", check_dependencies),
        ("Test Files", check_test_files),
        ("Test Responses", check_responses),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 60)
        results.append(check_func())
    
    print("\n" + "=" * 60)
    
    if all(results):
        print("✅ All checks passed! Ready to run evaluation.")
        print("\n🚀 Next step:")
        print("   python evaluation/run_evaluation.py")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
