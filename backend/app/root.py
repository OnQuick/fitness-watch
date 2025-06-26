import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({
            "message": "Witaj w API Fitness Watch!",
            "endpoints": [
                "/api/health",
                "/api/fitness-data",
                "/api/fitness-stats",
                "/api/devices"
            ]
        }),
        mimetype="application/json"
    ) 