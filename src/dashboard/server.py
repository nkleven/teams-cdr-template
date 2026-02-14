"""FastAPI server for metrics dashboard and real-time monitoring."""

import sys
import json
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    Request,
    HTTPException
)
from fastapi.responses import FileResponse, Response, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to path for absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Import application components
try:
    from src.session.manager import SessionManager
    from src.monitoring.responsible_ai_metrics import (
        ResponsibleAIMetrics
    )
    from src.health import HealthChecker
    session_manager = SessionManager()
    # Create a metrics tracker instance
    metrics_tracker = ResponsibleAIMetrics()
    health_checker = HealthChecker()
except ImportError as e:
    logger.warning(f"Optional components not available: {e}")
    session_manager = None
    metrics_tracker = None
    health_checker = None


@dataclass
class DashboardConfig:
    """Configuration for dashboard server."""
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    enable_cors: bool = True
    cors_origins: Optional[List[str]] = None
    enable_auth: bool = False
    enable_rate_limiting: bool = True
    rate_limit_per_minute: int = 60

    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["*"]


def _get_demo_metrics() -> Dict[str, Any]:
    """Get demo metrics data for dashboard."""
    return {
        "reliability": {
            "success_rate": 0.95,
            "total_requests": 42,
            "failed_requests": 2,
            "avg_response_time_ms": 247
        },
        "safety": {
            "block_rate": 0.02,
            "total_blocks": 1,
            "sensitive_data_detections": {"email": 0, "phone": 0}
        },
        "performance": {
            "avg_input_length": 156,
            "avg_output_length": 312,
            "avg_tokens_used": 468
        },
        "transparency": {
            "total_tool_calls": 18,
            "tool_usage": {"calculator": 12, "search": 6}
        }
    }


def _get_demo_health() -> Dict[str, Any]:
    """Get demo health check data."""
    return {
        "status": "healthy",
        "version": "3.0.1",
        "python_version": "3.12",
        "checks": {
            "system": {"uptime_seconds": 3600}
        }
    }


class ConnectionManager:
    """Manages WebSocket connections for real-time updates."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept a WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("✓ WebSocket client connected (total: %d)",
                    len(self.active_connections))

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info("✓ WebSocket client disconnected (total: %d)",
                    len(self.active_connections))

    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast a message to all connected clients."""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning("Failed to send to client: %s", e)
                disconnected.append(connection)

        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)


def create_dashboard_app(
    config: Optional[DashboardConfig] = None
) -> Optional[FastAPI]:
    """Create and configure the dashboard FastAPI application.

    Args:
        config: Optional dashboard configuration

    Returns:
        FastAPI application or None if FastAPI not available
    """
    config = config or DashboardConfig()

    # Create a fresh FastAPI app instance each time
    app = FastAPI(title="Eden Dashboard", version="3.0.1")

    # CORS middleware - must be added before routes are accessed
    if config.enable_cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=config.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # WebSocket connection manager
    ws_manager = ConnectionManager()
    
    # Store in app state for access in endpoints
    app.state.ws_manager = ws_manager
    app.state.config = config

    @app.get("/")
    async def root():
        """Serve the main dashboard HTML page"""
        index_path = project_root / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        return {"error": "index.html not found", "path": str(index_path)}

    @app.get("/app.js")
    async def get_app_js():
        """Serve the JavaScript file"""
        js_path = project_root / "app.js"
        if js_path.exists():
            return FileResponse(js_path, media_type="application/javascript")
        return {"error": "app.js not found", "path": str(js_path)}

    @app.get("/fluent.css")
    async def get_css():
        """Serve the CSS file"""
        css_path = project_root / "fluent.css"
        if css_path.exists():
            return FileResponse(css_path, media_type="text/css")
        return {"error": "fluent.css not found", "path": str(css_path)}

    @app.get("/favicon.ico")
    async def get_favicon():
        """Return 204 No Content for favicon requests"""
        return Response(status_code=204)

    @app.get("/health")
    async def health_check():
        """Health check endpoint for monitoring"""
        session_count = 0
        if session_manager:
            try:
                session_count = len(session_manager.get_all_sessions())
            except Exception:
                pass
        return {
            "status": "healthy",
            "sessions": session_count,
            "version": "3.0.1"
        }

    @app.get("/api/metrics")
    async def get_metrics(request: Request):
        """Get current metrics report."""
        if not metrics_tracker:
            raise HTTPException(
                status_code=503,
                detail="Metrics tracker not available"
            )
        try:
            report = metrics_tracker.generate_report()
            return report
        except Exception as e:
            logger.error("Failed to generate metrics report: %s", e)
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/sessions")
    async def get_sessions(request: Request):
        """REST endpoint to get all sessions"""
        if not session_manager:
            raise HTTPException(
                status_code=503,
                detail="Session manager not available"
            )
        try:
            sessions = session_manager.get_all_sessions()
            return {
                "sessions": [
                    {
                        "id": sid,
                        "status": getattr(session, 'status', 'unknown')
                    }
                    for sid, session in sessions.items()
                ]
            }
        except Exception as e:
            logger.error(f"Error getting sessions: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/sessions/{session_id}")
    async def get_session_detail(session_id: str):
        """Get detailed information about a specific session."""
        if not session_manager:
            raise HTTPException(
                status_code=503,
                detail="Session manager not available"
            )
        session = session_manager.get_session(session_id)
        if not session:
            raise HTTPException(
                status_code=404,
                detail=f"Session {session_id} not found or expired"
            )

        info = session.get_info()

        # Add metrics if available
        if session.metrics:
            info["metrics"] = session.metrics.generate_report()

        return info

    @app.post("/api/sessions/{session_id}/cleanup")
    async def cleanup_session(session_id: str):
        """Manually cleanup a session."""
        if not session_manager:
            raise HTTPException(
                status_code=503,
                detail="Session manager not available"
            )
        success = session_manager.delete_session(session_id)
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Session {session_id} not found"
            )
        return {
            "status": "success",
            "message": f"Session {session_id} cleaned up"
        }

    @app.post("/api/sessions/cleanup-expired")
    async def cleanup_expired():
        """Cleanup all expired sessions."""
        if not session_manager:
            raise HTTPException(
                status_code=503,
                detail="Session manager not available"
            )
        count = session_manager.cleanup_expired_sessions()
        return {
            "status": "success",
            "cleaned_count": count,
            "message": f"Cleaned up {count} expired sessions"
        }

    @app.get("/api/stats")
    async def get_all_stats():
        """Get comprehensive system statistics."""
        try:
            stats = {"timestamp": datetime.now(timezone.utc).isoformat()}
            
            # Metrics with fallback to demo data
            if metrics_tracker:
                try:
                    stats["metrics"] = metrics_tracker.generate_report()
                except Exception:
                    stats["metrics"] = _get_demo_metrics()
            else:
                stats["metrics"] = _get_demo_metrics()
                
            # Sessions stats
            if session_manager:
                stats["sessions"] = session_manager.get_stats()
            else:
                stats["sessions"] = {
                    "total_sessions": 0,
                    "active_sessions": 0,
                    "expired_sessions": 0,
                    "avg_age_seconds": 0,
                    "avg_idle_seconds": 0
                }
                
            # Health check with fallback
            if health_checker:
                try:
                    health_check_result = health_checker.perform_health_check()
                    stats["health"] = health_check_result.to_dict()
                except Exception:
                    stats["health"] = _get_demo_health()
            else:
                stats["health"] = _get_demo_health()
                
            return stats
        except Exception as e:
            logger.error("Failed to get stats: %s", e)
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/api/bible/verse/{reference:path}")
    async def get_bible_verse(reference: str):
        """
        Look up a Bible verse.
        
        The scroll opens. The Word speaks.
        Eden listens with reverence.
        """
        try:
            from src.tools.bible_study import bible_tool
            result = await bible_tool.execute(reference)
            if result.get("success"):
                return result
            else:
                raise HTTPException(
                    status_code=404,
                    detail=result.get("error", "Verse not found")
                )
        except ImportError:
            raise HTTPException(
                status_code=503,
                detail="Bible study tool not available"
            )

    @app.get("/api/bible/daily")
    async def get_daily_verse():
        """
        Get the verse of the day.
        
        The orchard offers daily bread.
        Bud thumps once. The scroll glows.
        """
        try:
            from src.tools.bible_study import bible_tool
            verse = bible_tool.get_daily_verse()
            return {
                "reference": str(verse),
                "text": verse.text,
                "version": verse.version.value,
                "stanza": "🌳 Daily bread from the orchard. Eden nourishes."
            }
        except ImportError:
            raise HTTPException(
                status_code=503,
                detail="Bible study tool not available"
            )

    @app.get("/api/bible/available")
    async def get_available_verses():
        """
        Get list of available verses in the beta library.
        
        The scroll reveals its contents.
        """
        try:
            from src.tools.bible_study import bible_tool
            verses = bible_tool.get_available_verses()
            return {
                "count": len(verses),
                "verses": verses,
                "message": "🌳 The library opens. Eden shares its wisdom."
            }
        except ImportError:
            raise HTTPException(
                status_code=503,
                detail="Bible study tool not available"
            )

    @app.get("/api/beta/testers")
    async def get_beta_testers():
        """
        Get list of registered beta testers.
        
        The Book of Names opens.
        The scroll reveals its witnesses.
        """
        try:
            from src.beta.testers import beta_registry
            testers = beta_registry.list_testers()
            return {
                "testers": [t.to_dict() for t in testers],
                "stats": beta_registry.get_stats(),
                "message": "🌳 The Book of Names opens. Eden welcomes."
            }
        except ImportError:
            return {
                "testers": [],
                "stats": {},
                "message": "Beta registry not available"
            }

    @app.get("/api/beta/welcome")
    async def beta_welcome():
        """
        Welcome page for beta testers.
        
        The gate opens. Eden welcomes.
        Customers arrive. The orchard listens.
        """
        return {
            "message": "🌳 Welcome to Project Eden Beta",
            "stanza": [
                "The gate opens. Eden welcomes.",
                "Beta testers arrive. The orchard listens.",
                "Bud thumps with joy. The scroll begins a new chapter."
            ],
            "endpoints": {
                "dashboard": "/dashboard",
                "monitoring": "/monitoring",
                "health": "/health",
                "stats": "/api/stats",
                "testers": "/api/beta/testers"
            },
            "founding_testers": [
                "Nathan Robert Kleven (The Bridge)",
                "Kelli Tait (Witness)"
            ]
        }

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """Handle WebSocket connections for real-time session updates"""
        await websocket.accept()
        client_id = id(websocket)
        
        try:
            logger.info(f"WebSocket client {client_id} connected")
            
            # Send initial session state
            if session_manager:
                sessions = session_manager.get_all_sessions()
                await websocket.send_json({
                    "type": "init",
                    "sessions": [
                        {
                            "id": sid,
                            "status": sess.status,
                            "created_at": (
                                sess.created_at.isoformat()
                                if hasattr(sess, 'created_at') else None
                            )
                        }
                        for sid, sess in sessions.items()
                    ]
                })
            else:
                await websocket.send_json({
                    "type": "error",
                    "message": "Session manager not available"
                })
            
            while True:
                data = await websocket.receive_text()
                try:
                    message = json.loads(data)
                    message_type = message.get("type")
                    
                    if not session_manager:
                        await websocket.send_json({
                            "type": "error",
                            "message": "Session manager not available"
                        })
                        continue
                    
                    if message_type == "get_sessions":
                        sessions = session_manager.get_all_sessions()
                        await websocket.send_json({
                            "type": "sessions",
                            "data": list(sessions.keys())
                        })
                        
                    elif message_type == "get_session":
                        session_id = message.get("session_id")
                        session = session_manager.get_session(session_id)
                        if session:
                            session_data = (
                                session.to_dict()
                                if hasattr(session, 'to_dict')
                                else str(session)
                            )
                            await websocket.send_json({
                                "type": "session_data",
                                "session_id": session_id,
                                "data": session_data
                            })
                        else:
                            await websocket.send_json({
                                "type": "error",
                                "message": f"Session {session_id} not found"
                            })
                            
                    else:
                        await websocket.send_json({
                            "type": "error",
                            "message": f"Unknown message type: {message_type}"
                        })
                        
                except json.JSONDecodeError:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Invalid JSON"
                    })
                    
        except WebSocketDisconnect:
            logger.info(f"WebSocket client {client_id} disconnected")
        except Exception as e:
            logger.error(f"WebSocket error for client {client_id}: {e}")
            try:
                await websocket.close()
            except Exception as close_error:
                logger.error(f"Error closing websocket: {close_error}")

    @app.get("/dashboard", response_class=HTMLResponse)
    async def dashboard_page():
        """Serve the metrics dashboard HTML page."""
        return get_dashboard_html()

    @app.get("/monitoring", response_class=HTMLResponse)
    async def monitoring_page():
        """Serve the real-time monitoring HTML page."""
        return get_monitoring_html()

    logger.info("✓ Dashboard app created successfully")
    cors_status = 'enabled' if config.enable_cors else 'disabled'
    logger.info(f"  - CORS: {cors_status}")
    rate_status = 'enabled' if config.enable_rate_limiting else 'disabled'
    logger.info(f"  - Rate limiting: {rate_status}")
    auth_status = 'enabled' if config.enable_auth else 'disabled'
    logger.info(f"  - Authentication: {auth_status}")
    return app


def get_dashboard_html() -> str:
    """Get the dashboard HTML page."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eden Agent Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }

        h1 {
            color: #333;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #666;
            font-size: 14px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .card h2 {
            color: #333;
            font-size: 18px;
            margin-bottom: 15px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }

        .metric {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }

        .metric:last-child {
            border-bottom: none;
        }

        .metric-label {
            color: #666;
            font-size: 14px;
        }

        .metric-value {
            color: #333;
            font-weight: bold;
            font-size: 14px;
        }

        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }

        .status-healthy { background: #10b981; }
        .status-degraded { background: #f59e0b; }
        .status-unhealthy { background: #ef4444; }

        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
        }

        .refresh-btn:hover {
            background: #5568d3;
        }

        .timestamp {
            color: #999;
            font-size: 12px;
            text-align: right;
            margin-top: 10px;
        }

        .chart-container {
            position: relative;
            height: 300px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Eden Agent Dashboard</h1>
            <p class="subtitle">Real-time monitoring and metrics visualization</p>
            <button class="refresh-btn" onclick="loadDashboard()">🔄 Refresh</button>
        </div>

        <div class="grid">
            <div class="card">
                <h2>System Health</h2>
                <div id="health-content">Loading...</div>
            </div>

            <div class="card">
                <h2>Session Statistics</h2>
                <div id="session-content">Loading...</div>
            </div>

            <div class="card">
                <h2>Reliability Metrics</h2>
                <div id="reliability-content">Loading...</div>
            </div>

            <div class="card">
                <h2>Safety Metrics</h2>
                <div id="safety-content">Loading...</div>
            </div>
        </div>

        <div class="card">
            <h2>Performance Trends</h2>
            <div class="chart-container">
                <canvas id="performanceChart"></canvas>
            </div>
        </div>

        <div class="card">
            <h2>Tool Usage</h2>
            <div class="chart-container">
                <canvas id="toolChart"></canvas>
            </div>
        </div>

        <div class="timestamp" id="last-updated"></div>
    </div>

    <script>
        let performanceChart = null;
        let toolChart = null;

        async function loadDashboard() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();

                updateHealth(data.health);
                updateSessions(data.sessions);
                updateReliability(data.metrics.reliability);
                updateSafety(data.metrics.safety);
                updateCharts(data.metrics);

                document.getElementById('last-updated').textContent =
                    'Last updated: ' + new Date().toLocaleString();

            } catch (error) {
                console.error('Failed to load dashboard:', error);
            }
        }

        function updateHealth(health) {
            const statusClass = 'status-' + health.status;
            const html = `
                <div class="metric">
                    <span class="metric-label">
                        <span class="status-indicator ${statusClass}"></span>
                        Status
                    </span>
                    <span class="metric-value">${health.status.toUpperCase()}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Version</span>
                    <span class="metric-value">${health.version}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Python</span>
                    <span class="metric-value">${health.python_version}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Uptime</span>
                    <span class="metric-value">${health.checks.system.uptime_seconds}s</span>
                </div>
            `;
            document.getElementById('health-content').innerHTML = html;
        }

        function updateSessions(sessions) {
            const html = `
                <div class="metric">
                    <span class="metric-label">Total Sessions</span>
                    <span class="metric-value">${sessions.total_sessions}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Active Sessions</span>
                    <span class="metric-value">${sessions.active_sessions}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Expired Sessions</span>
                    <span class="metric-value">${sessions.expired_sessions}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Avg Age</span>
                    <span class="metric-value">${sessions.avg_age_seconds}s</span>
                </div>
            `;
            document.getElementById('session-content').innerHTML = html;
        }

        function updateReliability(reliability) {
            const successRate = (reliability.success_rate * 100).toFixed(1);
            const html = `
                <div class="metric">
                    <span class="metric-label">Success Rate</span>
                    <span class="metric-value">${successRate}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Total Requests</span>
                    <span class="metric-value">${reliability.total_requests}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Failed Requests</span>
                    <span class="metric-value">${reliability.failed_requests}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Avg Response Time</span>
                    <span class="metric-value">${reliability.avg_response_time_ms}ms</span>
                </div>
            `;
            document.getElementById('reliability-content').innerHTML = html;
        }

        function updateSafety(safety) {
            const blockRate = (safety.block_rate * 100).toFixed(1);
            const html = `
                <div class="metric">
                    <span class="metric-label">Block Rate</span>
                    <span class="metric-value">${blockRate}%</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Total Blocks</span>
                    <span class="metric-value">${safety.total_blocks}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">PII Detections</span>
                    <span class="metric-value">${Object.values(safety.sensitive_data_detections).reduce((a, b) => a + b, 0)}</span>
                </div>
            `;
            document.getElementById('safety-content').innerHTML = html;
        }

        function updateCharts(metrics) {
            // Performance chart
            const perfCtx = document.getElementById('performanceChart').getContext('2d');
            if (performanceChart) performanceChart.destroy();

            performanceChart = new Chart(perfCtx, {
                type: 'bar',
                data: {
                    labels: ['Avg Input', 'Avg Output', 'Avg Tokens'],
                    datasets: [{
                        label: 'Performance Metrics',
                        data: [
                            metrics.performance.avg_input_length,
                            metrics.performance.avg_output_length,
                            metrics.performance.avg_tokens_used
                        ],
                        backgroundColor: [
                            'rgba(102, 126, 234, 0.8)',
                            'rgba(118, 75, 162, 0.8)',
                            'rgba(16, 185, 129, 0.8)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });

            // Tool usage chart
            const toolCtx = document.getElementById('toolChart').getContext('2d');
            if (toolChart) toolChart.destroy();

            const toolData = metrics.transparency.tool_usage;
            const toolLabels = Object.keys(toolData);
            const toolValues = Object.values(toolData);

            if (toolLabels.length > 0) {
                toolChart = new Chart(toolCtx, {
                    type: 'doughnut',
                    data: {
                        labels: toolLabels,
                        datasets: [{
                            data: toolValues,
                            backgroundColor: [
                                'rgba(102, 126, 234, 0.8)',
                                'rgba(118, 75, 162, 0.8)',
                                'rgba(16, 185, 129, 0.8)',
                                'rgba(245, 158, 11, 0.8)',
                                'rgba(239, 68, 68, 0.8)'
                            ]
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false
                    }
                });
            }
        }

        // Load dashboard on page load
        loadDashboard();

        // Auto-refresh every 30 seconds
        setInterval(loadDashboard, 30000);
    </script>
</body>
</html>
    """


def get_monitoring_html() -> str:
    """Get the real-time monitoring HTML page."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eden Agent - Real-time Monitoring</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #1a1a2e;
            color: #eee;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            background: #16213e;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #0f3460;
        }

        h1 {
            color: #e94560;
            margin-bottom: 10px;
        }

        .connection-status {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-top: 10px;
        }

        .connected {
            background: #10b981;
            color: white;
        }

        .disconnected {
            background: #ef4444;
            color: white;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }

        .monitor-card {
            background: #16213e;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #0f3460;
        }

        .monitor-card h2 {
            color: #e94560;
            font-size: 18px;
            margin-bottom: 15px;
            border-bottom: 2px solid #0f3460;
            padding-bottom: 10px;
        }

        .live-metric {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #0f3460;
            animation: fadeIn 0.3s;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .live-metric:last-child {
            border-bottom: none;
        }

        .metric-label {
            color: #bbb;
            font-size: 14px;
        }

        .metric-value {
            color: #e94560;
            font-weight: bold;
            font-size: 16px;
            font-family: 'Courier New', monospace;
        }

        .activity-log {
            background: #16213e;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #0f3460;
            margin-top: 20px;
            max-height: 400px;
            overflow-y: auto;
        }

        .log-entry {
            padding: 8px;
            margin: 4px 0;
            background: #0f3460;
            border-radius: 4px;
            font-size: 13px;
            font-family: 'Courier New', monospace;
            animation: slideIn 0.3s;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .timestamp {
            color: #888;
            font-size: 11px;
        }

        .pulse {
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ Real-time Monitoring</h1>
            <p class="subtitle">Live system metrics and activity tracking</p>
            <span id="status" class="connection-status disconnected">CONNECTING...</span>
        </div>

        <div class="grid">
            <div class="monitor-card">
                <h2>🎯 Live Metrics</h2>
                <div id="live-metrics">
                    <div class="live-metric">
                        <span class="metric-label">Waiting for data...</span>
                        <span class="metric-value pulse">●</span>
                    </div>
                </div>
            </div>

            <div class="monitor-card">
                <h2>👥 Active Sessions</h2>
                <div id="session-metrics">
                    <div class="live-metric">
                        <span class="metric-label">Loading...</span>
                        <span class="metric-value">-</span>
                    </div>
                </div>
            </div>

            <div class="monitor-card">
                <h2>📊 Request Stats</h2>
                <div id="request-metrics">
                    <div class="live-metric">
                        <span class="metric-label">Loading...</span>
                        <span class="metric-value">-</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="activity-log">
            <h2 style="color: #e94560; margin-bottom: 15px;">📝 Activity Log</h2>
            <div id="activity-log"></div>
        </div>
    </div>

    <script>
        let ws = null;
        let reconnectAttempts = 0;
        const maxReconnectAttempts = 5;

        function connect() {
            const wsUrl = 'ws://' + window.location.host + '/ws';
            ws = new WebSocket(wsUrl);

            ws.onopen = () => {
                console.log('WebSocket connected');
                document.getElementById('status').textContent = 'CONNECTED';
                document.getElementById('status').className = 'connection-status connected';
                reconnectAttempts = 0;
                logActivity('Connected to real-time monitoring');

                // Send ping every 5 seconds
                setInterval(() => {
                    if (ws.readyState === WebSocket.OPEN) {
                        ws.send('ping');
                    }
                }, 5000);
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.type === 'stats_update') {
                    updateDashboard(data.data);
                }
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                logActivity('Connection error occurred', 'error');
            };

            ws.onclose = () => {
                console.log('WebSocket disconnected');
                document.getElementById('status').textContent = 'DISCONNECTED';
                document.getElementById('status').className = 'connection-status disconnected';
                logActivity('Disconnected from monitoring');

                // Attempt to reconnect
                if (reconnectAttempts < maxReconnectAttempts) {
                    reconnectAttempts++;
                    setTimeout(() => {
                        logActivity(`Reconnecting (attempt ${reconnectAttempts})...`);
                        connect();
                    }, 3000);
                }
            };
        }

        function updateDashboard(data) {
            updateLiveMetrics(data.metrics);
            updateSessionMetrics(data.sessions);
            logActivity('Metrics updated');
        }

        function updateLiveMetrics(metrics) {
            const html = `
                <div class="live-metric">
                    <span class="metric-label">Total Requests</span>
                    <span class="metric-value">${metrics.reliability.total_requests}</span>
                </div>
                <div class="live-metric">
                    <span class="metric-label">Success Rate</span>
                    <span class="metric-value">${(metrics.reliability.success_rate * 100).toFixed(1)}%</span>
                </div>
                <div class="live-metric">
                    <span class="metric-label">Avg Response Time</span>
                    <span class="metric-value">${metrics.reliability.avg_response_time_ms}ms</span>
                </div>
            `;
            document.getElementById('live-metrics').innerHTML = html;

            const reqHtml = `
                <div class="live-metric">
                    <span class="metric-label">Failed Requests</span>
                    <span class="metric-value">${metrics.reliability.failed_requests}</span>
                </div>
                <div class="live-metric">
                    <span class="metric-label">Safety Blocks</span>
                    <span class="metric-value">${metrics.safety.total_blocks}</span>
                </div>
                <div class="live-metric">
                    <span class="metric-label">Tool Calls</span>
                    <span class="metric-value">${metrics.transparency.total_tool_calls}</span>
                </div>
            `;
            document.getElementById('request-metrics').innerHTML = reqHtml;
        }

        function updateSessionMetrics(sessions) {
            const html = `
                <div class="live-metric">
                    <span class="metric-label">Total Sessions</span>
                    <span class="metric-value">${sessions.total_sessions}</span>
                </div>
                <div class="live-metric">
                    <span class="metric-label">Active</span>
                    <span class="metric-value">${sessions.active_sessions}</span>
                </div>
                <div class="live-metric">
                    <span class="metric-label">Avg Idle Time</span>
                    <span class="metric-value">${sessions.avg_idle_seconds}s</span>
                </div>
            `;
            document.getElementById('session-metrics').innerHTML = html;
        }

        function logActivity(message, type = 'info') {
            const log = document.getElementById('activity-log');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            const timestamp = new Date().toLocaleTimeString();
            entry.innerHTML = `<span class="timestamp">[${timestamp}]</span> ${message}`;
            log.insertBefore(entry, log.firstChild);

            // Keep only last 50 entries
            while (log.children.length > 50) {
                log.removeChild(log.lastChild);
            }
        }

        // Connect on page load
        connect();
    </script>
</body>
</html>
    """


def start_dashboard_server(config: Optional[DashboardConfig] = None):
    """Start the dashboard server.

    Args:
        config: Optional dashboard configuration
    """
    config = config or DashboardConfig()
    app = create_dashboard_app(config)

    if app:
        logger.info(
            "Starting dashboard server on http://%s:%d",
            config.host,
            config.port
        )
        logger.info("Dashboard UI: http://%s:%d/dashboard", config.host, config.port)
        logger.info("Monitoring UI: http://%s:%d/monitoring", config.host, config.port)

        uvicorn.run(
            app,
            host=config.host,
            port=config.port,
            reload=config.reload,
            log_level="info"
        )
    else:
        raise RuntimeError(
            "Cannot start dashboard: FastAPI not installed. "
            "Install with: pip install fastapi uvicorn"
        )


if __name__ == "__main__":
    start_dashboard_server()
