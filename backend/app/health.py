import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"status": "healthy"}),
        mimetype="application/json"
    ) 