import azure.functions as func
import logging
import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from src.tracing.tracer import tracer

load_dotenv()

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

@app.route(route="chat")
def chat(req: func.HttpRequest) -> func.HttpResponse:
    with tracer.trace_operation("chat_request") as span:
        try:
            req_body = req.get_json()
            user_message = req_body.get("message", "")
            
            span.set_attribute("user.message_length", len(user_message))
            
            response = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            
            result = response.choices[0].message.content
            span.set_attribute("response.length", len(result))
            
            return func.HttpResponse(
                json.dumps({"response": result}),
                mimetype="application/json"
            )
        except Exception as e:
            logging.exception("Error processing chat request")
            span.record_exception(e)
            return func.HttpResponse(
                json.dumps({"error": "An internal error occurred. Please try again."}),
                status_code=500,
                mimetype="application/json"
            )
