import azure.functions as func
import logging
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
import asyncio
from azure.iot.hub import IoTHubRegistryManager
import os
from dotenv import load_dotenv
from .cosmos_client import get_fitness_data
from .models import FitnessData
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

# Ładowanie zmiennych środowiskowych
load_dotenv()

app = FastAPI(title="Fitness Watch API")

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W produkcji należy to ograniczyć do konkretnych domen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Witaj w API Fitness Watch!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/fitness-data", response_model=List[FitnessData])
async def get_data(
    device_id: Optional[str] = Query(None, description="ID urządzenia"),
    limit: int = Query(100, description="Maksymalna liczba rekordów do zwrócenia")
):
    """
    Pobiera dane fitness z Cosmos DB.
    Można filtrować po ID urządzenia i ograniczyć liczbę zwracanych rekordów.
    """
    try:
        data = get_fitness_data(device_id, limit)
        return data
    except Exception as e:
        logging.error(f"Błąd podczas pobierania danych: {str(e)}")
        raise

# Główna funkcja Azure Function
async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Konwertowanie żądania Azure Function na format FastAPI
    async def receive():
        return {
            "type": "http",
            "method": req.method,
            "headers": dict(req.headers),
            "query_params": dict(req.params),
            "body": await req.get_body()
        }

    # Tworzenie obiektu Request dla FastAPI
    request = Request(scope={
        "type": "http",
        "method": req.method,
        "headers": [(k.lower().encode(), v.encode()) for k, v in req.headers.items()],
        "query_string": req.url.split("?")[1].encode() if "?" in req.url else b"",
        "path": req.route_params.get("route", ""),
        "raw_path": req.route_params.get("route", "").encode(),
    })

    # Obsługa żądania przez FastAPI
    try:
        response = await app(request)
        return func.HttpResponse(
            body=response.body,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return func.HttpResponse(
            body=str(e).encode(),
            status_code=500
        )
