from fastapi import APIRouter, Depends, HTTPException
from ..firestore_config import db
from ..dependencies import get_current_user
from ..utils.mqtt_client import MQTTClient, MQTT_CONFIG
import time
import asyncio

router = APIRouter()

@router.post("/subscribe-mqtt")
async def subscribe_mqtt(userID:str = Depends(get_current_user)):
    try:
        mqtt_client = MQTTClient(userID=userID, topic="esp32/pub", **MQTT_CONFIG)
        mqtt_client.connect()
        mqtt_client.start()

        start_time = time.time()
        while time.time() - start_time < 20:  # Espera hasta 20 segundos
            if not mqtt_client.messages_received.empty():
                break  # Salir del bucle si hay mensajes
            await asyncio.sleep(1)  # Espera asíncrona de 1 segundo

        mqtt_client.stop()

        # Devolver el mensaje recibido
        messages = mqtt_client.get_messages()

        # Aquí necesitas una forma de devolver el mensaje recibido
        return {"message": messages if messages else "No se recibió el mensaje"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_acl(user_id, device_id, permiso):
    with open('/etc/mosquitto/mosquitto.acl', 'a') as acl_file:
        acl_file.write(f"\nuser {user_id}\ntopic {permiso} device/{device_id}/#")
