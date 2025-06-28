# Symulator Fitness Watch

Symulator urządzenia fitness watch, który wysyła dane do Azure IoT Hub.

## Wymagania

- Python 3.7+
- Konto Azure z IoT Hub
- Connection string do urządzenia IoT

## Instalacja

1. Przejdź do katalogu symulatora:

```bash
cd device-simulator
```

2. Utwórz wirtualne środowisko Python:

```bash
python -m venv venv
```

3. Aktywuj wirtualne środowisko:

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

4. Zainstaluj wymagane zależności:

```bash
pip install -r requirements.txt
```

## Konfiguracja

Przed uruchomieniem symulatora upewnij się, że:

1. Masz poprawny connection string do Azure IoT Hub w pliku `main.py`
2. Urządzenie jest zarejestrowane w IoT Hub
3. Masz odpowiednie uprawnienia do wysyłania danych

## Uruchomienie

```bash
python main.py
```

## Co robi symulator

- Generuje losowe dane fitness co 30 sekund
- Wysyła dane do Azure IoT Hub
- Wyświetla status wysyłania w konsoli

## Struktura danych

Symulator wysyła dane w formacie JSON:

```json
{
  "device_id": "fitness-watch-001",
  "heart_rate": 75,
  "steps": 15,
  "calories": 8,
  "distance": 0.25,
  "sleep_hours": 1.5
}
```

## Zatrzymanie

Aby zatrzymać symulator, naciśnij `Ctrl+C` w terminalu.
