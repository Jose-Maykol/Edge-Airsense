from ...utils.mqtt_client import MQTTClient, MQTT_CONFIG
import asyncio
import time
import datetime
import json

async def process_user_sensor(device_data):
    user_id = device_data.get('userID')
    device_type = device_data.get('type')
    device_id = device_data.get('deviceID')

    mqtt_client = MQTTClient(userID=user_id, topic=f"{user_id}/pub", **MQTT_CONFIG)
    mqtt_client.connect()
    mqtt_client.start()
    
    start_time = time.time()
    while time.time() - start_time < 30:  # Espera hasta 20 segundos
        if not mqtt_client.messages_received.empty():
            break  # Salir del bucle si hay mensajes
        await asyncio.sleep(1)  # Espera asíncrona de 1 segundo
    
    mqtt_client.stop()
    
    # Devolver el mensaje recibido
    message_recived = mqtt_client.get_messages()

    if message_recived is None:
        return

    message = json.loads(message_recived)

    # Clasificar los datos
    temperature = message["temperature"]
    humidity = message["humidity"]
    temperature_category = categorize_temperature(temperature)
    humidity_category = categorize_humidity(humidity)

    # Preparar los datos para Firebase
    data = {
        "categoryHumidity": humidity_category,
        "categoryTemperature": temperature_category,
        "deviceID": device_id,
        "humidity": humidity,
        "temperature": temperature,
        "timestamp": datetime.datetime.now(),
        "userID": user_id
    }

    # Almacenar en Firebase
    db.collection('temperature_data').add(data)


async def temperature_storage_task():
    devices_ref = db.collection('devices')
    devices = devices_ref.where('type', '==', 'temperature').get()

    tasks = []

    for device in devices:
        device_data = device.to_dict()
        task = asyncio.create_task(process_user_sensor(device_data))
        tasks.append(task)
    
    await asyncio.gather(*tasks)

def categorize_temperature(temperature):
    if temperature < 0:
        return "Muy Frío"
    elif 0 <= temperature <= 10:
        return "Frío"
    elif 11 <= temperature <= 20:
        return "Templado"
    elif 21 <= temperature <= 30:
        return "Cálido"
    else:
        return "Muy Cálido"

def categorize_humidity(humidity):
    if humidity < 20:
        return "Muy Seco"
    elif 20 <= humidity <= 40:
        return "Seco"
    elif 41 <= humidity <= 60:
        return "Moderado"
    elif 61 <= humidity <= 80:
        return "Húmedo"
    else:
        return "Muy Húmedo"
