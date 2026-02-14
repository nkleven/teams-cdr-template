# Eden Dashboard

Real-time session monitoring dashboard for Eden.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python -m src.dashboard

# Or with custom configuration
DASHBOARD_HOST=0.0.0.0 DASHBOARD_PORT=3000 python -m src.dashboard
```

## Endpoints

- `GET /` - Dashboard UI
- `GET /health` - Health check
- `GET /api/sessions` - Get all sessions (REST)
- `WS /ws` - WebSocket for real-time updates

## WebSocket Messages

### Client → Server
```json
{"type": "get_sessions"}
{"type": "get_session", "session_id": "123"}
```

### Server → Client
```json
{"type": "init", "sessions": [...]}
{"type": "sessions", "data": [...]}
{"type": "session_data", "session_id": "123", "data": {...}}
{"type": "error", "message": "..."}
```

## Development

The server will auto-reload on file changes when `DASHBOARD_RELOAD=true`.
