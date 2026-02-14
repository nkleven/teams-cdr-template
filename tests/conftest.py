"""Pytest configuration for Eden Agent tests."""
import pytest
import os
from dotenv import load_dotenv

# Load test environment variables
load_dotenv()


@pytest.fixture(scope="session")
def mock_anthropic_key():
    """Provide a mock API key for testing."""
    original_key = os.environ.get("ANTHROPIC_API_KEY")
    if not original_key:
        os.environ["ANTHROPIC_API_KEY"] = "test-key-for-unit-tests"
    yield os.environ["ANTHROPIC_API_KEY"]
    if not original_key:
        del os.environ["ANTHROPIC_API_KEY"]


@pytest.fixture(autouse=True)
def reset_metrics():
    """Reset metrics before each test."""
    from src.monitoring.responsible_ai_metrics import metrics_tracker
    metrics_tracker.reset()
    yield
    metrics_tracker.reset()
