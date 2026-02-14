import uvicorn
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Run the dashboard server"""
    host = os.getenv("DASHBOARD_HOST", "127.0.0.1")
    port = int(os.getenv("DASHBOARD_PORT", "8000"))
    reload = os.getenv("DASHBOARD_RELOAD", "true").lower() == "true"
    
    print(f"Starting Eden Dashboard on http://{host}:{port}")
    print(f"Auto-reload: {reload}")
    
    from src.dashboard.server import create_dashboard_app
    app = create_dashboard_app()
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
