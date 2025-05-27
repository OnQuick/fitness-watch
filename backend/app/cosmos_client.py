from azure.cosmos import CosmosClient
import os
from dotenv import load_dotenv

load_dotenv()

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

def get_fitness_data(device_id: str = None, limit: int = 100):
    """Pobiera dane fitness z Cosmos DB"""
    container = get_container()
    
    # Przygotowanie zapytania
    query = "SELECT * FROM c"
    if device_id:
        query += f" WHERE c.device_id = '{device_id}'"
    query += f" ORDER BY c.timestamp DESC OFFSET 0 LIMIT {limit}"
    
    # Wykonanie zapytania
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    
    return items 