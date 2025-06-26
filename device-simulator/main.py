import os
import time
import random
import json
from azure.iot.device import IoTHubDeviceClient, Message

# Konfiguracja Azure IoT Hub
IOT_HUB_NAME = "fitness-hubb3a0ece8"
DEVICE_ID = "fitness-watch-001"
IOT_HUB_CONNECTION_STRING = "HostName=fitness-hubb3a0ece8.azure-devices.net;DeviceId=fitness-watch-001;SharedAccessKey=EfXeKFQILIhNpSSG6T+5kvdGsee+TrOn9sGSZRrSgH0="
SIMULATION_INTERVAL = 30  # sekundy

# Funkcja generująca losowe dane fitness
def generate_fitness_data():
    """Generuje kompletne dane fitness zgodne z modelem API"""
    return {
        "device_id": DEVICE_ID,  # Zmienione z deviceId na device_id
        "heart_rate": random.randint(60, 100),
        "steps": random.randint(0, 20),
        "calories": random.randint(0, 15),
        "distance": round(random.uniform(0, 0.5), 2),  # km
        "sleep_hours": round(random.uniform(0, 2), 1)  # godziny snu w tym interwale
    }

# Inicjalizacja klienta IoT
client = IoTHubDeviceClient.create_from_connection_string(IOT_HUB_CONNECTION_STRING)

print("🚀 Symulator Fitness Watch uruchomiony")
print(f"📱 Device ID: {DEVICE_ID}")
print(f"⏱️  Interwał: {SIMULATION_INTERVAL} sekund")
print("📊 Wysyłanie danych...")
print("-" * 50)

while True:
    try:
        # Generuj dane
        data = generate_fitness_data()
        
        # Konwertuj na JSON string
        message_json = json.dumps(data)
        message = Message(message_json)
        
        # Dodaj właściwości wiadomości
        message.content_encoding = "utf-8"
        message.content_type = "application/json"
        
        # Wyślij wiadomość
        client.send_message(message)
        
        # Wyświetl status
        print(f"✅ Wysłano: {json.dumps(data, indent=2)}")
        
    except Exception as e:
        print(f"❌ Błąd wysyłania: {e}")
    
    time.sleep(SIMULATION_INTERVAL)

# UWAGA: Zamień 'YOUR_KEY_HERE' na właściwy klucz z portalu Azure!
# Instalacja wymaganych bibliotek:
# pip install azure-iot-device
