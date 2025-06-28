# 📋 Instrukcje importowania kolekcji Postman

## Jak zaimportować kolekcję

### Krok 1: Otwórz Postman

1. Uruchom aplikację Postman
2. Zaloguj się na swoje konto (opcjonalne, ale zalecane)

### Krok 2: Zaimportuj kolekcję

1. Kliknij przycisk **"Import"** w lewym górnym rogu
2. Wybierz zakładkę **"File"**
3. Kliknij **"Upload Files"** i wybierz plik `Fitness_Watch_API_Collection.json`
4. Kliknij **"Import"**

### Krok 3: Skonfiguruj zmienne środowiskowe

Po zaimportowaniu kolekcji, skonfiguruj zmienne:

1. Kliknij na ikonę **"Environment"** (około) w prawym górnym rogu
2. Kliknij **"Add"** aby utworzyć nowe środowisko
3. Nazwij je np. **"Fitness Watch Local"**
4. Dodaj następujące zmienne:

| Variable    | Initial Value           | Current Value           | Description                 |
| ----------- | ----------------------- | ----------------------- | --------------------------- |
| `base_url`  | `http://localhost:7071` | `http://localhost:7071` | URL Twojego API             |
| `device_id` | `watch-001`             | `watch-001`             | ID urządzenia do testowania |
| `record_id` | `example-uuid`          | `example-uuid`          | ID rekordu do testowania    |

5. Kliknij **"Save"**

## 🚀 Jak używać kolekcji

### 1. Uruchom API lokalnie

```bash
cd backend
func start
```

### 2. Testuj endpointy w kolejności:

#### a) Sprawdź czy API działa

- Uruchom **"Health Check"** - powinien zwrócić `{"status": "healthy"}`

#### b) Sprawdź dostępne endpointy

- Uruchom **"Root"** - pokaże listę wszystkich endpointów

#### c) Dodaj dane testowe

- Uruchom **"Add Fitness Data"** - doda nowy rekord
- Skopiuj `id` z odpowiedzi i zaktualizuj zmienną `record_id` w środowisku

#### d) Pobierz dane

- Uruchom **"Get Fitness Data"** - pobierze wszystkie dane
- Możesz modyfikować parametry query (device_id, limit, start_date, end_date)

#### e) Sprawdź statystyki

- Uruchom **"Get Fitness Stats"** - pokaże statystyki dla urządzenia

#### f) Sprawdź listę urządzeń

- Uruchom **"Get Devices"** - pokaże wszystkie urządzenia

#### g) Aktualizuj dane

- Uruchom **"Update Fitness Data"** - zaktualizuje istniejący rekord

#### h) Usuń dane

- Uruchom **"Delete Fitness Data"** - usunie rekord

## 🔧 Konfiguracja dla różnych środowisk

### Lokalne środowisko

```
base_url: http://localhost:7071
```

### Azure Functions (po wdrożeniu)

```
base_url: https://your-function-app-name.azurewebsites.net
```

### Środowisko deweloperskie

```
base_url: https://dev-fitness-watch.azurewebsites.net
```

## 📝 Przykłady użycia

### Pobieranie danych z filtrami

```
GET {{base_url}}/api/fitness-data?device_id=watch-001&limit=10&start_date=2024-01-01&end_date=2024-01-31
```

### Dodawanie nowych danych

```json
POST {{base_url}}/api/fitness-data
Content-Type: application/json

{
  "device_id": "watch-001",
  "heart_rate": 75,
  "steps": 8500,
  "calories": 450,
  "distance": 6.2,
  "sleep_hours": 7.5
}
```

### Aktualizacja danych

```json
PUT {{base_url}}/api/fitness-data?id=uuid&device_id=watch-001
Content-Type: application/json

{
  "heart_rate": 80,
  "steps": 9000
}
```

## 🎯 Automatyzacja testów

Możesz dodać testy automatyczne do każdego requestu:

### Przykład testu dla Health Check:

```javascript
pm.test("Status code is 200", function () {
  pm.response.to.have.status(200);
});

pm.test("Response has status field", function () {
  var jsonData = pm.response.json();
  pm.expect(jsonData).to.have.property("status");
  pm.expect(jsonData.status).to.eql("healthy");
});
```

### Przykład testu dla dodawania danych:

```javascript
pm.test("Status code is 200", function () {
  pm.response.to.have.status(200);
});

pm.test("Response has required fields", function () {
  var jsonData = pm.response.json();
  pm.expect(jsonData).to.have.property("id");
  pm.expect(jsonData).to.have.property("device_id");
  pm.expect(jsonData).to.have.property("timestamp");
});

// Zapisz ID do zmiennej środowiskowej
if (pm.response.json().id) {
  pm.environment.set("record_id", pm.response.json().id);
}
```

## 🔍 Debugowanie

Jeśli endpointy nie działają:

1. **Sprawdź czy API jest uruchomione** - `func start` w folderze backend
2. **Sprawdź URL** - upewnij się, że `base_url` jest poprawny
3. **Sprawdź logi** - w terminalu gdzie uruchomiłeś `func start`
4. **Sprawdź zmienne środowiskowe** - czy są poprawnie ustawione

## 📚 Dodatkowe zasoby

- [Dokumentacja API](../backend/API_DOCUMENTATION.md)
- [Azure Functions Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/)
- [Postman Learning Center](https://learning.postman.com/)
