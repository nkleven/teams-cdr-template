
import sys
import os
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if __name__ == "__main__":
    import uvicorn
    from src.dashboard.server import create_dashboard_app
    
    app = create_dashboard_app()
    
    print("Starting Travel Dashboard Server...")
    print("Open your browser to: http://localhost:8000")
    print("")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False
    )
