import azure.functions as func
import logging
import json
import os
import sys
from datetime import datetime, timezone

# Add parent directory to path to import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

async def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function endpoint for Eden Agent chat interactions.
    
    POST /api/agent
    Body: {"message": "user message", "session_id": "optional"}
    """
    logging.info('Eden Agent endpoint triggered')
    
    # Get client principal for authentication
    client_principal = req.headers.get('x-ms-client-principal')
    if client_principal:
        logging.info('Authenticated request received')
    
    try:
        # Parse request body
        req_body = req.get_json()
        message = req_body.get('message')
        session_id = req_body.get('session_id', 'default')
        
        if not message:
            return func.HttpResponse(
                json.dumps({"error": "Message is required"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Import and initialize agent
        from src.agent.core import Agent
        from src.tools.calculator import CalculatorTool
        
        agent = Agent(tools=[CalculatorTool()])
        
        # Process chat message
        response = await agent.chat(message)
        
        return func.HttpResponse(
            json.dumps({
                "response": response,
                "session_id": session_id,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }),
            status_code=200,
            mimetype="application/json"
        )
        
    except ValueError as e:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON in request body"}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.exception("Error processing agent request")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )
