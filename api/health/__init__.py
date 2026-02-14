import azure.functions as func
import logging
import json


async def main(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint for Azure Static Web Apps."""
    logging.info('Health check endpoint triggered')
    
    return func.HttpResponse(
        json.dumps({
            "status": "healthy",
            "service": "Eden Agent API",
            "version": "0.1.0-beta.1"
        }),
        status_code=200,
        mimetype="application/json"
    )
