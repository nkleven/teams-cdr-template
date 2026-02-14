import azure.functions as func
import logging
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


async def main(req: func.HttpRequest) -> func.HttpResponse:
    """Azure Function endpoint for Eden Agent chat (Ollama backend)."""
    logging.info('Eden Agent endpoint triggered')

    try:
        req_body = req.get_json()
        message = req_body.get('message')
        session_id = req_body.get('session_id', 'default')

        if not message:
            return func.HttpResponse(
                json.dumps({"error": "Message is required"}),
                status_code=400,
                mimetype="application/json"
            )

        from src.agent.core import Agent
        from src.tools.calculator import CalculatorTool

        agent = Agent(tools=[CalculatorTool()])
        response = await agent.chat(message)

        return func.HttpResponse(
            json.dumps({
                "response": response,
                "session_id": session_id,
            }),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON"}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Agent error: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )