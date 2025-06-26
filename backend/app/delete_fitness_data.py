import azure.functions as func
import json
from .cosmos_client import get_container

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        record_id = req.params.get("id")
        if not record_id:
            return func.HttpResponse(json.dumps({"error": "Brak parametru id"}), status_code=400)
        container = get_container()
        # Zakładamy, że partition key to device_id, więc musimy go znać
        device_id = req.params.get("device_id")
        if not device_id:
            return func.HttpResponse(json.dumps({"error": "Brak parametru device_id (partition key)"}), status_code=400)
        container.delete_item(item=record_id, partition_key=device_id)
        return func.HttpResponse(json.dumps({"deleted": record_id}), mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500) 