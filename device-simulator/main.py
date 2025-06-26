import os
import time
import random
from azure.iot.device import IoTHubDeviceClient, Message

# Konfiguracja Azure IoT Hub
IOT_HUB_NAME = "tf-iota7a8b266"
DEVICE_ID = "fitness-watch-001"
IOT_HUB_CONNECTION_STRING = "HostName=tf-iotb7e61c13.azure-devices.net;DeviceId=fitness-watch-001;SharedAccessKey=0eJE7CSkx2qQf9PmHyk4RQtNqdVg3swETbLwDrkiovE="
SIMULATION_INTERVAL = 30  # sekundy

# Funkcja generująca losowe dane
def generate_data():
    steps = random.randint(0, 20)  # liczba kroków w interwale
    heart_rate = random.randint(60, 100)  # tętno
    return {"deviceId": DEVICE_ID, "steps": steps, "heart_rate": heart_rate}

# Inicjalizacja klienta IoT
client = IoTHubDeviceClient.create_from_connection_string(IOT_HUB_CONNECTION_STRING)

print("Symulator uruchomiony. Wysyłanie danych...")

while True:
    data = generate_data()
    message = Message(str(data))
    try:
        client.send_message(message)
        print(f"Wysłano: {data}")
    except Exception as e:
        print(f"Błąd wysyłania: {e}")
    time.sleep(SIMULATION_INTERVAL)

# UWAGA: Zamień 'YOUR_KEY_HERE' na właściwy klucz z portalu Azure!
# Instalacja wymaganych bibliotek:
# pip install azure-iot-device
