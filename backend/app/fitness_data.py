import azure.functions as func
import json
from .cosmos_client import get_fitness_data, add_fitness_data
from .models import FitnessDataCreate

def main(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "GET":
        device_id = req.params.get("device_id")
        limit = int(req.params.get("limit", 100))
        start_date = req.params.get("start_date")
        end_date = req.params.get("end_date")
        try:
            data = get_fitness_data(device_id, limit, start_date, end_date)
            return func.HttpResponse(json.dumps(data), mimetype="application/json")
        except Exception as e:
            return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)
    elif req.method == "POST":
        try:
            body = req.get_json()
            data = FitnessDataCreate(**body)
            result = add_fitness_data(data)
            return func.HttpResponse(json.dumps(result), mimetype="application/json")
        except Exception as e:
            return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500)
    else:
        return func.HttpResponse("Method not allowed", status_code=405) 