# Fitness Watch API - Azure Functions + CosmosDB

To jest API dla aplikacji fitness watch, które używa Azure Functions do obsługi żądań HTTP i CosmosDB do przechowywania danych.

## Struktura projektu

```
backend/
├── app/
│   ├── main.py              # Główna funkcja Azure Functions + FastAPI
│   ├── cosmos_client.py     # Klient do CosmosDB
│   ├── models.py            # Modele danych Pydantic
│   └── function.json        # Konfiguracja Azure Functions
├── requirements.txt         # Zależności Python
├── host.json               # Konfiguracja hosta Azure Functions
└── env.example             # Przykład zmiennych środowiskowych
```

## Konfiguracja

### 1. Zmienne środowiskowe

Skopiuj `env.example` do `.env` i uzupełnij dane:

```bash
cp env.example .env
```

Edytuj `.env`:

```env
# CosmosDB Configuration
COSMOS_ENDPOINT=https://your-cosmos-account.documents.azure.com:443/
COSMOS_KEY=your-cosmos-primary-key
COSMOS_DATABASE_NAME=fitness-database
COSMOS_CONTAINER_NAME=fitness-data

# Azure Functions Configuration
FUNCTIONS_WORKER_RUNTIME=python
FUNCTIONS_EXTENSION_VERSION=~4
```

### 2. Konfiguracja CosmosDB

1. Utwórz konto CosmosDB w Azure Portal
2. Utwórz bazę danych o nazwie `fitness-database`
3. Utwórz kontener o nazwie `fitness-data` z partition key `/device_id`
4. Skopiuj endpoint i klucz do pliku `.env`

## Instalacja i uruchomienie

### Lokalne uruchomienie

1. Zainstaluj zależności:

```bash
cd backend
pip install -r requirements.txt
```

2. Uruchom Azure Functions lokalnie:

```bash
func start
```

3. API będzie dostępne pod adresem: `http://localhost:7071`

### Wdrożenie na Azure

1. Zaloguj się do Azure CLI:

```bash
az login
```

2. Wdróż funkcję:

```bash
func azure functionapp publish your-function-app-name
```

## Endpointy API

### 1. GET / - Informacje o API

```bash
curl http://localhost:7071/
```

### 2. GET /health - Sprawdzenie stanu

```bash
curl http://localhost:7071/health
```

### 3. GET /fitness-data - Pobieranie danych fitness

**Podstawowe użycie:**

```bash
curl "http://localhost:7071/fitness-data"
```

**Z filtrowaniem:**

```bash
# Po device_id
curl "http://localhost:7071/fitness-data?device_id=device123"

# Z limitem
curl "http://localhost:7071/fitness-data?limit=50"

# Z filtrowaniem po dacie
curl "http://localhost:7071/fitness-data?start_date=2024-01-01&end_date=2024-01-31"

# Kombinacja filtrów
curl "http://localhost:7071/fitness-data?device_id=device123&limit=10&start_date=2024-01-01"
```

### 4. POST /fitness-data - Dodawanie nowych danych

```bash
curl -X POST "http://localhost:7071/fitness-data" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "device123",
    "heart_rate": 75,
    "steps": 8500,
    "calories": 450,
    "distance": 6.2,
    "sleep_hours": 7.5
  }'
```

### 5. GET /fitness-stats - Statystyki fitness

```bash
# Statystyki dla wszystkich urządzeń (ostatnie 7 dni)
curl "http://localhost:7071/fitness-stats"

# Statystyki dla konkretnego urządzenia
curl "http://localhost:7071/fitness-stats?device_id=device123"

# Statystyki dla ostatnich 30 dni
curl "http://localhost:7071/fitness-stats?days=30"
```

### 6. GET /devices - Lista urządzeń

```bash
curl "http://localhost:7071/devices"
```

## Struktura danych

### FitnessData

```json
{
  "id": "uuid",
  "device_id": "device123",
  "timestamp": "2024-01-15T10:30:00Z",
  "heart_rate": 75,
  "steps": 8500,
  "calories": 450,
  "distance": 6.2,
  "sleep_hours": 7.5
}
```

### FitnessStats

```json
{
  "device_id": "device123",
  "period_days": 7,
  "total_steps": 59500,
  "avg_heart_rate": 72.5,
  "total_calories": 3150,
  "total_distance": 43.4,
  "avg_sleep_hours": 7.2,
  "data_points_count": 7
}
```

## Testowanie z device-simulator

Możesz użyć symulatora urządzeń do testowania API:

```bash
cd ../device-simulator
python main.py
```

## Dokumentacja API

Po uruchomieniu API, dokumentacja Swagger będzie dostępna pod adresem:

- `http://localhost:7071/docs` - Swagger UI
- `http://localhost:7071/redoc` - ReDoc

## Rozwiązywanie problemów

### Błędy połączenia z CosmosDB

1. Sprawdź czy zmienne środowiskowe są poprawnie ustawione
2. Sprawdź czy konto CosmosDB jest aktywne
3. Sprawdź czy klucz jest poprawny

### Błędy Azure Functions

1. Sprawdź czy masz zainstalowane Azure Functions Core Tools
2. Sprawdź czy Python 3.8+ jest zainstalowany
3. Sprawdź logi: `func start --verbose`

## Następne kroki

1. Dodaj autoryzację (Azure AD, API Keys)
2. Dodaj walidację danych
3. Dodaj cache'owanie (Redis)
4. Dodaj monitoring i alerty
5. Dodaj testy jednostkowe
