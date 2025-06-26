from azure.cosmos import CosmosClient
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import uuid
from .models import FitnessDataCreate

# Ładowanie zmiennych środowiskowych
load_dotenv()

# Pobieranie konfiguracji z zmiennych środowiskowych
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME")
CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME")

def get_cosmos_client():
    """Tworzy i zwraca klienta Cosmos DB"""
    return CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

def get_container():
    """Zwraca kontener z danymi"""
    client = get_cosmos_client()
    database = client.get_database_client(DATABASE_NAME)
    return database.get_container_client(CONTAINER_NAME)

def get_fitness_data(device_id: str = None, limit: int = 100, start_date: str = None, end_date: str = None):
    """Pobiera dane fitness z Cosmos DB"""
    container = get_container()
    
    # Przygotowanie zapytania
    query = "SELECT * FROM c"
    conditions = []
    
    if device_id:
        conditions.append(f"c.device_id = '{device_id}'")
    
    if start_date:
        conditions.append(f"c.timestamp >= '{start_date}T00:00:00Z'")
    
    if end_date:
        conditions.append(f"c.timestamp <= '{end_date}T23:59:59Z'")
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += f" ORDER BY c.timestamp DESC OFFSET 0 LIMIT {limit}"
    
    # Wykonanie zapytania
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    
    return items

def add_fitness_data(data: FitnessDataCreate):
    """Dodaje nowe dane fitness do Cosmos DB"""
    container = get_container()
    
    # Przygotowanie dokumentu
    document = {
        "id": str(uuid.uuid4()),
        "device_id": data.device_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "heart_rate": data.heart_rate,
        "steps": data.steps,
        "calories": data.calories,
        "distance": data.distance,
        "sleep_hours": data.sleep_hours
    }
    
    # Usuń None wartości
    document = {k: v for k, v in document.items() if v is not None}
    
    # Dodanie do CosmosDB
    result = container.create_item(document)
    return result

def get_fitness_stats(device_id: str = None, days: int = 7):
    """Pobiera statystyki fitness dla określonego okresu"""
    container = get_container()
    
    # Obliczenie daty początkowej
    start_date = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
    
    # Przygotowanie zapytania
    query = f"""
    SELECT 
        c.device_id,
        COUNT(1) as data_points_count,
        SUM(c.steps) as total_steps,
        AVG(c.heart_rate) as avg_heart_rate,
        SUM(c.calories) as total_calories,
        SUM(c.distance) as total_distance,
        AVG(c.sleep_hours) as avg_sleep_hours
    FROM c 
    WHERE c.timestamp >= '{start_date}'
    """
    
    if device_id:
        query += f" AND c.device_id = '{device_id}'"
    
    query += " GROUP BY c.device_id"
    
    # Wykonanie zapytania
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    
    # Przygotowanie wyników
    if items:
        stats = items[0]  # Bierzemy pierwszy wynik
        return {
            "device_id": stats.get("device_id", device_id or "all"),
            "period_days": days,
            "total_steps": int(stats.get("total_steps", 0)),
            "avg_heart_rate": round(float(stats.get("avg_heart_rate", 0)), 2),
            "total_calories": int(stats.get("total_calories", 0)),
            "total_distance": round(float(stats.get("total_distance", 0)), 2),
            "avg_sleep_hours": round(float(stats.get("avg_sleep_hours", 0)), 2),
            "data_points_count": int(stats.get("data_points_count", 0))
        }
    else:
        return {
            "device_id": device_id or "all",
            "period_days": days,
            "total_steps": 0,
            "avg_heart_rate": 0.0,
            "total_calories": 0,
            "total_distance": 0.0,
            "avg_sleep_hours": 0.0,
            "data_points_count": 0
        } 