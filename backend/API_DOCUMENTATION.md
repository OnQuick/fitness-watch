# 📚 Fitness Watch API – Dokumentacja Endpointów

## Root

**GET** `/api/`  
Opis: Informacja o API i lista endpointów  
**Przykład odpowiedzi:**

```json
{
  "message": "Witaj w API Fitness Watch!",
  "endpoints": [
    "/api/health",
    "/api/fitness-data",
    "/api/fitness-stats",
    "/api/devices"
  ]
}
```

---

## Healthcheck

**GET** `/api/health`  
Opis: Sprawdzenie czy API działa  
**Przykład odpowiedzi:**

```json
{
  "status": "healthy"
}
```

---

## Fitness Data

### Pobieranie danych

**GET** `/api/fitness-data`  
Parametry (opcjonalne, jako query string):

- `device_id` – filtruj po urządzeniu
- `limit` – ile rekordów zwrócić (domyślnie 100)
- `start_date` – data od (YYYY-MM-DD)
- `end_date` – data do (YYYY-MM-DD)

**Przykład:**  
`GET /api/fitness-data?device_id=watch-001&limit=10&start_date=2024-01-01&end_date=2024-01-31`

**Przykład odpowiedzi:**

```json
[
  {
    "id": "uuid",
    "device_id": "watch-001",
    "timestamp": "2024-01-15T10:30:00Z",
    "heart_rate": 75,
    "steps": 8500,
    "calories": 450,
    "distance": 6.2,
    "sleep_hours": 7.5
  }
]
```

---

### Dodawanie danych

**POST** `/api/fitness-data`  
**Body (JSON):**

```json
{
  "device_id": "watch-001",
  "heart_rate": 75,
  "steps": 8500,
  "calories": 450,
  "distance": 6.2,
  "sleep_hours": 7.5
}
```

**Przykład odpowiedzi:**  
Zwraca dodany rekord (z `id` i `timestamp`).

---

### Aktualizacja danych

**PUT** `/api/fitness-data?id=<id>&device_id=<device_id>`  
**Body (JSON):**  
Podaj tylko pola, które chcesz zaktualizować.

**Przykład:**  
`PUT /api/fitness-data?id=uuid&device_id=watch-001`

```json
{
  "heart_rate": 80
}
```

**Przykład odpowiedzi:**  
Zwraca zaktualizowany rekord.

---

### Usuwanie danych

**DELETE** `/api/fitness-data?id=<id>&device_id=<device_id>`  
**Przykład:**  
`DELETE /api/fitness-data?id=uuid&device_id=watch-001`

**Przykład odpowiedzi:**

```json
{
  "deleted": "uuid"
}
```

---

## Statystyki

**GET** `/api/fitness-stats?device_id=<device_id>&days=<dni>`

- `device_id` – opcjonalnie, statystyki dla konkretnego urządzenia
- `days` – liczba dni do analizy (domyślnie 7)

**Przykład odpowiedzi:**

```json
{
  "device_id": "watch-001",
  "period_days": 7,
  "total_steps": 59500,
  "avg_heart_rate": 72.5,
  "total_calories": 3150,
  "total_distance": 43.4,
  "avg_sleep_hours": 7.2,
  "data_points_count": 7
}
```

---

## Lista urządzeń

**GET** `/api/devices`  
Opis: Zwraca listę wszystkich unikalnych `device_id`  
**Przykład odpowiedzi:**

```json
{
  "devices": ["watch-001", "watch-002"]
}
```

---

## Kody odpowiedzi

- `200 OK` – Sukces
- `400 Bad Request` – Brak wymaganych parametrów
- `404 Not Found` – Endpoint nie istnieje
- `500 Internal Server Error` – Błąd serwera
