import os
import time
import random
import json
from azure.iot.device import IoTHubDeviceClient, Message

# Konfiguracja Azure IoT Hub
IOT_HUB_NAME = "tf-iot377ae0b7"
DEVICE_ID = "fitness-watch-001"
IOT_HUB_CONNECTION_STRING = "HostName=tf-iot377ae0b7.azure-devices.net;DeviceId=fitness-watch-001;SharedAccessKey=Ynj3F4gddhPJD+KhdwVf6WwPYJDboQYqMzGHkXSgOmc="
SIMULATION_INTERVAL = 30  

def generate_fitness_data():
    """Generuje kompletne dane fitness zgodne z modelem API"""
    return {
        "device_id": DEVICE_ID,  
        "heart_rate": random.randint(60, 100),
        "steps": random.randint(0, 20),
        "calories": random.randint(0, 15),
        "distance": round(random.uniform(0, 0.5), 2),  
        "sleep_hours": round(random.uniform(0, 2), 1)  
    }


client = IoTHubDeviceClient.create_from_connection_string(IOT_HUB_CONNECTION_STRING)

print("🚀 Symulator Fitness Watch uruchomiony")
print(f"📱 Device ID: {DEVICE_ID}")
print(f"⏱️  Interwał: {SIMULATION_INTERVAL} sekund")
print("📊 Wysyłanie danych...")
print("-" * 50)

while True:
    try:
        data = generate_fitness_data()
        
        message_json = json.dumps(data)
        message = Message(message_json)
        
        message.content_encoding = "utf-8"
        message.content_type = "application/json"
        
        client.send_message(message)
        
        print(f"✅ Wysłano: {json.dumps(data, indent=2)}")
        
    except Exception as e:
        print(f"❌ Błąd wysyłania: {e}")
    
    time.sleep(SIMULATION_INTERVAL)

