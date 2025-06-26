import azure.functions as func
import json
from .cosmos_client import get_container

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        record_id = req.params.get("id")
        device_id = req.params.get("device_id")
        if not record_id or not device_id:
            return func.HttpResponse(json.dumps({"error": "Brak parametru id lub device_id"}), status_code=400)
        body = req.get_json()
        container = get_container()
        # Pobierz istniejący rekord
        item = container.read_item(item=record_id, partition_key=device_id)
        # Zaktualizuj pola
        item.update(body)
        updated = container.replace_item(item=record_id, body=item)
        return func.HttpResponse(json.dumps(updated), mimetype="application/json")
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500) 