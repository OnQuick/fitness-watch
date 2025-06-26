import azure.functions as func
import json
from .cosmos_client import get_fitness_data

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        devices = get_fitness_data()
        unique_devices = list(set(item.get('device_id') for item in devices if item.get('device_id')))
        return func.HttpResponse(json.dumps({"devices": unique_devices}), mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500) 