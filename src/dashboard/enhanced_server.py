"""Enhanced dashboard with real-time monitoring and metrics."""

import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict, List, Any
import json
from datetime import datetime
from pathlib import Path


app = FastAPI(title="Eden Agent Dashboard", version="3.0.1")


class MetricsManager:
    """Manage real-time metrics tracking."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.metrics_history: List[Dict[str, Any]] = []
        self.max_history = 1000
    
    async def connect(self, websocket: WebSocket):
        """Connect a new websocket client."""
        await websocket.accept()
        self.active_connections.append(websocket)
        
        # Send initial metrics history
        await websocket.send_json({
            "type": "history",
            "data": self.metrics_history[-100:]  # Last 100 entries
        })
    
    def disconnect(self, websocket: WebSocket):
        """Disconnect a websocket client."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def broadcast_metric(self, metric_data: Dict[str, Any]):
        """Broadcast metric to all connected clients."""
        metric_data["timestamp"] = datetime.now().isoformat()
        
        # Add to history
        self.metrics_history.append(metric_data)
        if len(self.metrics_history) > self.max_history:
            self.metrics_history = self.metrics_history[-self.max_history:]
        
        # Broadcast to all clients
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json({
                    "type": "metric",
                    "data": metric_data
                })
            except Exception:
                disconnected.append(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)


metrics_manager = MetricsManager()


@app.get("/")
async def get_dashboard():
    """Serve the main dashboard HTML."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Eden Agent Dashboard</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                padding: 20px;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            
            header {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            
            h1 {
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .status-badge {
                display: inline-block;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 0.9em;
            }
            
            .status-online {
                background: #10b981;
                color: white;
            }
            
            .status-offline {
                background: #ef4444;
                color: white;
            }
            
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }
            
            .card {
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            
            .card h2 {
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.3em;
            }
            
            .metric {
                margin: 15px 0;
            }
            
            .metric-label {
                font-size: 0.9em;
                color: #666;
                margin-bottom: 5px;
            }
            
            .metric-value {
                font-size: 2em;
                font-weight: bold;
                color: #333;
            }
            
            .metric-unit {
                font-size: 0.8em;
                color: #999;
            }
            
            .chart-container {
                height: 200px;
                margin-top: 15px;
                background: #f9fafb;
                border-radius: 5px;
                padding: 10px;
            }
            
            .recent-requests {
                max-height: 400px;
                overflow-y: auto;
            }
            
            .request-item {
                padding: 12px;
                margin: 8px 0;
                background: #f9fafb;
                border-left: 4px solid #667eea;
                border-radius: 4px;
            }
            
            .request-success {
                border-left-color: #10b981;
            }
            
            .request-error {
                border-left-color: #ef4444;
            }
            
            .timestamp {
                font-size: 0.85em;
                color: #666;
            }
            
            .tool-list {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-top: 10px;
            }
            
            .tool-badge {
                background: #667eea;
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 0.85em;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            .loading {
                animation: pulse 1.5s ease-in-out infinite;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🤖 Eden Agent Dashboard</h1>
                <p style="color: #666; margin-top: 10px;">Real-time monitoring and analytics</p>
                <div style="margin-top: 15px;">
                    <span class="status-badge" id="connection-status">
                        ⚫ Connecting...
                    </span>
                </div>
            </header>
            
            <div class="grid">
                <div class="card">
                    <h2>📊 Request Statistics</h2>
                    <div class="metric">
                        <div class="metric-label">Total Requests</div>
                        <div class="metric-value" id="total-requests">0</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Success Rate</div>
                        <div class="metric-value">
                            <span id="success-rate">0</span><span class="metric-unit">%</span>
                        </div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Avg Response Time</div>
                        <div class="metric-value">
                            <span id="avg-response-time">0</span><span class="metric-unit">s</span>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h2>🔧 Tool Usage</h2>
                    <div class="tool-list" id="tool-list">
                        <span class="loading">Loading tools...</span>
                    </div>
                    <div class="chart-container" id="tool-chart">
                        <!-- Tool usage chart would go here -->
                    </div>
                </div>
                
                <div class="card">
                    <h2>⚡ Performance</h2>
                    <div class="metric">
                        <div class="metric-label">Total Tokens</div>
                        <div class="metric-value" id="total-tokens">0</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Tool Calls</div>
                        <div class="metric-value" id="total-tool-calls">0</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Error Count</div>
                        <div class="metric-value" id="error-count">0</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>📝 Recent Requests</h2>
                <div class="recent-requests" id="recent-requests">
                    <p class="loading">Waiting for requests...</p>
                </div>
            </div>
        </div>
        
        <script>
            let ws = null;
            let metrics = {
                total_requests: 0,
                successful_requests: 0,
                failed_requests: 0,
                total_tokens: 0,
                total_tool_calls: 0,
                avg_response_time: 0,
                tool_usage_stats: {}
            };
            
            function connectWebSocket() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws/metrics`;
                
                ws = new WebSocket(wsUrl);
                
                ws.onopen = () => {
                    console.log('WebSocket connected');
                    document.getElementById('connection-status').className = 'status-badge status-online';
                    document.getElementById('connection-status').textContent = '🟢 Connected';
                };
                
                ws.onmessage = (event) => {
                    const message = JSON.parse(event.data);
                    
                    if (message.type === 'metric') {
                        updateMetrics(message.data);
                    } else if (message.type === 'history') {
                        // Load historical data
                        message.data.forEach(updateMetrics);
                    }
                };
                
                ws.onclose = () => {
                    console.log('WebSocket disconnected');
                    document.getElementById('connection-status').className = 'status-badge status-offline';
                    document.getElementById('connection-status').textContent = '🔴 Disconnected';
                    
                    // Reconnect after 3 seconds
                    setTimeout(connectWebSocket, 3000);
                };
                
                ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                };
            }
            
            function updateMetrics(data) {
                // Update metrics object
                Object.assign(metrics, data);
                
                // Update UI
                document.getElementById('total-requests').textContent = metrics.total_requests || 0;
                
                const successRate = metrics.total_requests > 0 
                    ? (metrics.successful_requests / metrics.total_requests * 100).toFixed(1)
                    : 0;
                document.getElementById('success-rate').textContent = successRate;
                
                document.getElementById('avg-response-time').textContent = 
                    (metrics.avg_response_time || 0).toFixed(2);
                
                document.getElementById('total-tokens').textContent = metrics.total_tokens || 0;
                document.getElementById('total-tool-calls').textContent = metrics.total_tool_calls || 0;
                document.getElementById('error-count').textContent = metrics.failed_requests || 0;
                
                // Update tool usage
                const toolList = document.getElementById('tool-list');
                if (metrics.tool_usage_stats && Object.keys(metrics.tool_usage_stats).length > 0) {
                    toolList.innerHTML = '';
                    for (const [tool, count] of Object.entries(metrics.tool_usage_stats)) {
                        const badge = document.createElement('span');
                        badge.className = 'tool-badge';
                        badge.textContent = `${tool}: ${count}`;
                        toolList.appendChild(badge);
                    }
                }
            }
            
            // Connect on page load
            connectWebSocket();
            
            // Refresh every 5 seconds
            setInterval(() => {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({type: 'ping'}));
                }
            }, 5000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.websocket("/ws/metrics")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics."""
    await metrics_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle ping/pong or other messages
            if data == '{"type":"ping"}':
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        metrics_manager.disconnect(websocket)


@app.get("/api/metrics")
async def get_metrics():
    """Get current metrics via REST API."""
    if metrics_manager.metrics_history:
        return metrics_manager.metrics_history[-1]
    return {
        "total_requests": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "total_tokens": 0,
        "tool_usage_stats": {}
    }


@app.post("/api/metrics")
async def post_metrics(metrics: Dict[str, Any]):
    """Post new metrics (for agent to report)."""
    await metrics_manager.broadcast_metric(metrics)
    return {"status": "success"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "active_connections": len(metrics_manager.active_connections),
        "metrics_history_size": len(metrics_manager.metrics_history)
    }



@app.get("/travel/partner/{partner_name}")
async def get_travel_partner_dashboard(partner_name: str):
    """Get travel partner dashboard for a specific partner."""
    from src.tools.travel_coordination import travel_coordinator
    
    # Normalize the partner name for comparison
    normalized_name = partner_name.lower().strip()
    coordinator_name = travel_coordinator.name.lower()
    
    if normalized_name in [coordinator_name, "greg", "greg plett"]:
        context = travel_coordinator.get_coordination_context()
        timeline = travel_coordinator.get_wedding_timeline()
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Travel Partner Dashboard - {travel_coordinator.name}</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #333;
                    padding: 20px;
                    min-height: 100vh;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                
                header {{
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                
                h1 {{
                    color: #667eea;
                    margin-bottom: 10px;
                    font-size: 2.5em;
                }}
                
                .subtitle {{
                    color: #666;
                    font-size: 1.1em;
                }}
                
                .nav {{
                    margin-top: 20px;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                }}
                
                .nav a {{
                    display: inline-block;
                    padding: 10px 20px;
                    margin-right: 10px;
                    background: #667eea;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    transition: background 0.3s;
                }}
                
                .nav a:hover {{
                    background: #764ba2;
                }}
                
                .content {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin-bottom: 20px;
                }}
                
                .card {{
                    background: white;
                    padding: 25px;
                    border-radius: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}
                
                .card h2 {{
                    color: #667eea;
                    margin-bottom: 15px;
                    font-size: 1.5em;
                    border-bottom: 2px solid #667eea;
                    padding-bottom: 10px;
                }}
                
                .info-row {{
                    display: flex;
                    justify-content: space-between;
                    padding: 12px 0;
                    border-bottom: 1px solid #eee;
                }}
                
                .info-row:last-child {{
                    border-bottom: none;
                }}
                
                .label {{
                    font-weight: 600;
                    color: #666;
                }}
                
                .value {{
                    color: #333;
                    font-weight: 500;
                }}
                
                .full-width {{
                    grid-column: 1 / -1;
                }}
                
                .wedding-info {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                
                .wedding-info h2 {{
                    color: white;
                    border-bottom-color: white;
                }}
                
                .wedding-info .label {{
                    color: rgba(255, 255, 255, 0.8);
                }}
                
                .wedding-info .value {{
                    color: white;
                }}
                
                .status-badge {{
                    display: inline-block;
                    padding: 8px 12px;
                    background: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    font-size: 0.9em;
                    font-weight: 600;
                }}
                
                .team-member {{
                    margin-bottom: 15px;
                    padding: 10px;
                    background: #f5f5f5;
                    border-left: 4px solid #667eea;
                    border-radius: 3px;
                }}
                
                .team-member strong {{
                    color: #667eea;
                }}
                
                footer {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    color: #666;
                    margin-top: 20px;
                }}
                
                @media (max-width: 768px) {{
                    .content {{
                        grid-template-columns: 1fr;
                    }}
                    
                    h1 {{
                        font-size: 1.8em;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Travel Partner Dashboard</h1>
                    <p class="subtitle">
                        Coordinating travel for <strong>{context['bride']}</strong> &amp; <strong>{context['groom']}</strong>'s wedding
                    </p>
                    <nav class="nav">
                        <a href="/">← Back to Main Dashboard</a>
                    </nav>
                </header>
                
                <div class="content">
                    <!-- Coordinator Info -->
                    <div class="card">
                        <h2>Coordinator Information</h2>
                        <div class="info-row">
                            <span class="label">Name</span>
                            <span class="value"><strong>{travel_coordinator.name}</strong></span>
                        </div>
                        <div class="info-row">
                            <span class="label">Role</span>
                            <span class="value">{context['role']}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">Specialization</span>
                            <span class="value">{', '.join(travel_coordinator.specialization)}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">Status</span>
                            <span class="value"><span class="status-badge">Active</span></span>
                        </div>
                        <div class="info-row">
                            <span class="label">Payment Provider</span>
                            <span class="value">{context['travel_payment_provider']}</span>
                        </div>
                    </div>
                    
                    <!-- Wedding Timeline -->
                    <div class="card wedding-info full-width">
                        <h2>Wedding Timeline</h2>
                        <div class="info-row">
                            <span class="label">Wedding Date</span>
                            <span class="value"><strong>{timeline['wedding_date']}</strong></span>
                        </div>
                        <div class="info-row">
                            <span class="label">Days Until Wedding</span>
                            <span class="value"><strong>{timeline['days_until_wedding']}</strong> days</span>
                        </div>
                        <div class="info-row">
                            <span class="label">Wedding Year</span>
                            <span class="value">{timeline['wedding_year']}</span>
                        </div>
                    </div>
                    
                    <!-- Couple Information -->
                    <div class="card">
                        <h2>Couple Information</h2>
                        <div class="team-member">
                            <strong>Groom:</strong> {context['groom']}
                        </div>
                        <div class="team-member">
                            <strong>Bride:</strong> {context['bride']}
                        </div>
                        <div class="team-member">
                            <strong>Wedding Date:</strong> {context['wedding_date']}
                        </div>
                    </div>
                    
                    <!-- Travel Coordination Status -->
                    <div class="card">
                        <h2>Coordination Status</h2>
                        <div class="info-row">
                            <span class="label">Travel Enabled</span>
                            <span class="value">
                                <span class="status-badge">{"Yes" if context['travel_enabled'] else "No"}</span>
                            </span>
                        </div>
                        <div class="info-row">
                            <span class="label">Payment Processing</span>
                            <span class="value">
                                <span class="status-badge">{"Active" if travel_coordinator.travel_payment_enabled else "Inactive"}</span>
                            </span>
                        </div>
                        <div class="info-row">
                            <span class="label">Provider</span>
                            <span class="value">{travel_coordinator.travel_payment_provider}</span>
                        </div>
                    </div>
                </div>
                
                <footer>
                    <p>Eden - Enterprise Development &amp; Evaluation Network</p>
                    <p>Travel Coordination Module v1.0</p>
                </footer>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    else:
        raise HTTPException(status_code=404, detail=f"Travel partner '{partner_name}' not found")


@app.get("/travel/dashboard")
async def get_travel_dashboard():
    """Get main travel coordination dashboard."""
    from src.tools.travel_coordination import travel_coordinator
    
    context = travel_coordinator.get_coordination_context()
    timeline = travel_coordinator.get_wedding_timeline()
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Travel Coordination Dashboard</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                padding: 20px;
                min-height: 100vh;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            
            header {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            
            h1 {{
                color: #667eea;
                margin-bottom: 10px;
                font-size: 2.5em;
            }}
            
            .nav {{
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid #eee;
            }}
            
            .nav a {{
                display: inline-block;
                padding: 10px 20px;
                margin-right: 10px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background 0.3s;
            }}
            
            .nav a:hover {{
                background: #764ba2;
            }}
            
            .partners-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }}
            
            .partner-card {{
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s, box-shadow 0.3s;
                cursor: pointer;
            }}
            
            .partner-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
            }}
            
            .partner-card h2 {{
                color: #667eea;
                margin-bottom: 10px;
                font-size: 1.5em;
            }}
            
            .partner-card p {{
                color: #666;
                margin-bottom: 15px;
                line-height: 1.6;
            }}
            
            .partner-card .btn {{
                display: inline-block;
                padding: 10px 20px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background 0.3s;
            }}
            
            .partner-card .btn:hover {{
                background: #764ba2;
            }}
            
            footer {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                color: #666;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>Travel Coordination Dashboard</h1>
                <p>Wedding: {context['bride']} & {context['groom']} - {timeline['wedding_date']}</p>
                <nav class="nav">
                    <a href="/">← Back to Main Dashboard</a>
                </nav>
            </header>
            
            <h2 style="color: white; margin-bottom: 20px;">Travel Partners</h2>
            <div class="partners-grid">
                <div class="partner-card">
                    <h2>{travel_coordinator.name}</h2>
                    <p><strong>Role:</strong> {context['role']}</p>
                    <p><strong>Specialization:</strong> {', '.join(travel_coordinator.specialization)}</p>
                    <p><strong>Payment Provider:</strong> {context['travel_payment_provider']}</p>
                    <a href="/travel/partner/{travel_coordinator.name.replace(' ', '%20')}" class="btn">View Dashboard</a>
                </div>
            </div>
            
            <footer>
                <p>Eden - Enterprise Development & Evaluation Network</p>
                <p>Travel Coordination Module v1.0</p>
            </footer>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
