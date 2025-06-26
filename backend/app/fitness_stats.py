import azure.functions as func
import json
from .cosmos_client import get_fitness_stats

def main(req: func.HttpRequest) -> func.HttpResponse:
    device_id = req.params.get("device_id")
    days = int(req.params.get("days", 7))
    try:
        stats = get_fitness_stats(device_id, days)
        return func.HttpResponse(json.dumps(stats), mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500) 