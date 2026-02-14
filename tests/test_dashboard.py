"""Unit tests for the dashboard server."""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from datetime import datetime, timezone

from src.dashboard.server import (
    create_dashboard_app,
    DashboardConfig,
    ConnectionManager
)


@pytest.fixture
def dashboard_config():
    """Create a test dashboard configuration."""
    return DashboardConfig(
        host="127.0.0.1",
        port=8001,
        reload=False,
        enable_cors=True,
        cors_origins=["http://localhost:3000"]
    )


@pytest.fixture
def mock_session_manager():
    """Mock the session manager."""
    with patch('src.dashboard.server.session_manager') as mock:
        # Create mock sessions with proper attributes
        session1 = Mock(status="active", created_at=datetime.now(timezone.utc))
        session1.metrics = None  # Explicitly set metrics to None to avoid recursion
        session1.to_dict = lambda: {"id": "session1", "status": "active", "data": "test"}
        
        session2 = Mock(status="active", created_at=datetime.now(timezone.utc))
        session2.metrics = None
        session2.to_dict = lambda: {"id": "session2", "status": "active", "data": "test"}
        
        mock.get_all_sessions.return_value = {
            "session1": session1,
            "session2": session2
        }
        
        # Create a mock for get_session that returns proper serializable data
        session_detail = Mock(status="active")
        session_detail.metrics = None  # No metrics to avoid recursion
        session_detail.get_info = lambda: {"id": "session1", "status": "active"}
        session_detail.to_dict = lambda: {"id": "session1", "status": "active", "data": "test"}
        mock.get_session.return_value = session_detail
        
        mock.get_stats.return_value = {
            "total_sessions": 2,
            "active_sessions": 2,
            "expired_sessions": 0,
            "avg_age_seconds": 120,
            "avg_idle_seconds": 30
        }
        yield mock


@pytest.fixture
def mock_metrics_tracker():
    """Mock the metrics tracker."""
    with patch('src.dashboard.server.metrics_tracker') as mock:
        mock.generate_report.return_value = {
            "reliability": {
                "success_rate": 0.95,
                "total_requests": 100,
                "failed_requests": 5,
                "avg_response_time_ms": 250
            },
            "safety": {
                "block_rate": 0.02,
                "total_blocks": 2,
                "sensitive_data_detections": {"email": 1, "phone": 0}
            },
            "performance": {
                "avg_input_length": 150,
                "avg_output_length": 300,
                "avg_tokens_used": 450
            },
            "transparency": {
                "total_tool_calls": 50,
                "tool_usage": {"search": 30, "calculator": 20}
            }
        }
        yield mock


@pytest.fixture
def mock_health_checker():
    """Mock the health checker."""
    with patch('src.dashboard.server.health_checker') as mock:
        health_result = Mock()
        health_result.to_dict.return_value = {
            "status": "healthy",
            "version": "1.0.0",
            "python_version": "3.11.0",
            "checks": {
                "system": {"uptime_seconds": 3600}
            }
        }
        mock.perform_health_check.return_value = health_result
        yield mock


@pytest.fixture
def app(dashboard_config, mock_session_manager, mock_metrics_tracker, mock_health_checker):
    """Create a test FastAPI application."""
    return create_dashboard_app(dashboard_config)


@pytest.fixture
def client(app):
    """Create a test client."""
    return TestClient(app)


class TestDashboardEndpoints:
    """Test dashboard API endpoints."""

    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "sessions" in data
        assert data["version"] == "1.0.0"

    def test_get_sessions(self, client, mock_session_manager):
        """Test getting all sessions."""
        response = client.get("/api/sessions")
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data
        assert len(data["sessions"]) == 2

    def test_get_session_detail(self, client, mock_session_manager):
        """Test getting session details."""
        response = client.get("/api/sessions/session1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "session1"
        assert data["status"] == "active"

    def test_get_session_not_found(self, client, mock_session_manager):
        """Test getting non-existent session."""
        mock_session_manager.get_session.return_value = None
        response = client.get("/api/sessions/nonexistent")
        assert response.status_code == 404

    def test_cleanup_session(self, client, mock_session_manager):
        """Test manual session cleanup."""
        mock_session_manager.delete_session.return_value = True
        response = client.post("/api/sessions/session1/cleanup")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_cleanup_expired_sessions(self, client, mock_session_manager):
        """Test cleanup of expired sessions."""
        mock_session_manager.cleanup_expired_sessions.return_value = 3
        response = client.post("/api/sessions/cleanup-expired")
        assert response.status_code == 200
        data = response.json()
        assert data["cleaned_count"] == 3

    def test_get_all_stats(self, client, mock_metrics_tracker, mock_session_manager, mock_health_checker):
        """Test getting comprehensive stats."""
        response = client.get("/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert "metrics" in data
        assert "sessions" in data
        assert "health" in data
        assert "timestamp" in data

    def test_get_metrics(self, client, mock_metrics_tracker):
        """Test getting metrics report."""
        response = client.get("/api/metrics")
        assert response.status_code == 200
        # Note: This test may need adjustment based on actual JSONResponse import

    def test_dashboard_html(self, client):
        """Test dashboard HTML page."""
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert b"Eden Agent Dashboard" in response.content

    def test_monitoring_html(self, client):
        """Test monitoring HTML page."""
        response = client.get("/monitoring")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert b"Real-time Monitoring" in response.content

    def test_favicon(self, client):
        """Test favicon endpoint."""
        response = client.get("/favicon.ico")
        assert response.status_code == 204


class TestConnectionManager:
    """Test WebSocket connection manager."""

    @pytest.fixture
    def connection_manager(self):
        """Create a connection manager instance."""
        return ConnectionManager()

    @pytest.mark.asyncio
    async def test_connect(self, connection_manager):
        """Test connecting a WebSocket."""
        mock_websocket = MagicMock()
        mock_websocket.accept = AsyncMock(return_value=None)
        
        await connection_manager.connect(mock_websocket)
        
        assert len(connection_manager.active_connections) == 1
        assert mock_websocket in connection_manager.active_connections
        mock_websocket.accept.assert_called_once()

    def test_disconnect(self, connection_manager):
        """Test disconnecting a WebSocket."""
        mock_websocket = MagicMock()
        connection_manager.active_connections.append(mock_websocket)
        
        connection_manager.disconnect(mock_websocket)
        
        assert len(connection_manager.active_connections) == 0

    @pytest.mark.asyncio
    async def test_broadcast(self, connection_manager):
        """Test broadcasting to all connections."""
        mock_ws1 = MagicMock()
        mock_ws1.send_json = AsyncMock(return_value=None)
        mock_ws2 = MagicMock()
        mock_ws2.send_json = AsyncMock(return_value=None)
        
        connection_manager.active_connections = [mock_ws1, mock_ws2]
        
        message = {"type": "test", "data": "hello"}
        await connection_manager.broadcast(message)
        
        mock_ws1.send_json.assert_called_once_with(message)
        mock_ws2.send_json.assert_called_once_with(message)


class TestDashboardConfig:
    """Test dashboard configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = DashboardConfig()
        assert config.host == "0.0.0.0"
        assert config.port == 8000
        assert config.reload is False
        assert config.enable_cors is True
        assert config.cors_origins == ["*"]

    def test_custom_config(self):
        """Test custom configuration."""
        config = DashboardConfig(
            host="127.0.0.1",
            port=3000,
            reload=True,
            enable_cors=False,
            cors_origins=["http://localhost:3000"]
        )
        assert config.host == "127.0.0.1"
        assert config.port == 3000
        assert config.reload is True
        assert config.enable_cors is False
        assert config.cors_origins == ["http://localhost:3000"]


class TestWebSocketEndpoint:
    """Test WebSocket functionality."""

    def test_websocket_connect(self, client):
        """Test WebSocket connection."""
        with client.websocket_connect("/ws") as websocket:
            data = websocket.receive_json()
            assert data["type"] == "init"
            assert "sessions" in data

    def test_websocket_get_sessions(self, client):
        """Test WebSocket get sessions message."""
        with client.websocket_connect("/ws") as websocket:
            # Skip init message
            websocket.receive_json()
            
            # Send get_sessions request
            websocket.send_json({"type": "get_sessions"})
            data = websocket.receive_json()
            
            assert data["type"] == "sessions"
            assert "data" in data

    def test_websocket_get_session(self, client):
        """Test WebSocket get specific session message."""
        with client.websocket_connect("/ws") as websocket:
            # Skip init message
            websocket.receive_json()
            
            # Send get_session request
            websocket.send_json({"type": "get_session", "session_id": "session1"})
            data = websocket.receive_json()
            
            assert data["type"] == "session_data"
            assert data["session_id"] == "session1"

    def test_websocket_invalid_json(self, client):
        """Test WebSocket with invalid JSON."""
        with client.websocket_connect("/ws") as websocket:
            # Skip init message
            websocket.receive_json()
            
            # Send invalid JSON
            websocket.send_text("invalid json")
            data = websocket.receive_json()
            
            assert data["type"] == "error"
            assert "Invalid JSON" in data["message"]

    def test_websocket_unknown_message_type(self, client):
        """Test WebSocket with unknown message type."""
        with client.websocket_connect("/ws") as websocket:
            # Skip init message
            websocket.receive_json()
            
            # Send unknown message type
            websocket.send_json({"type": "unknown"})
            data = websocket.receive_json()
            
            assert data["type"] == "error"
            assert "Unknown message type" in data["message"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
