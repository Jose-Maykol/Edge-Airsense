import ssl
import paho.mqtt.client as mqtt
import time
import asyncio
import queue
import json

# Configuraciones del broker MQTT
MQTT_CONFIG = {
    "broker": "ahee5r1ym27qz-ats.iot.sa-east-1.amazonaws.com",
    "puerto": 8883,
    "ca_cert": "./certs/rootCA.pem",
    "certfile": "./certs/cert.crt",
    "keyfile": "./certs/private.key",
}

class MQTTClient:
    def __init__(self, userID, broker, puerto, ca_cert, certfile, keyfile, topic=None):
        self.client = mqtt.Client(userID)
        self.broker = broker
        self.puerto = puerto
        self.ca_cert = ca_cert
        self.certfile = certfile
        self.keyfile = keyfile
        self.topic = topic
        self.messages_received = queue.Queue()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conectado exitosamente al broker MQTT")
            if self.topic:
                client.subscribe(self.topic, qos=1)
        else:
            print(f"Fallo al conectar, código de resultado: {rc}")

    def on_message(self, client, userdata, msg):
        try:
            decoded_message = msg.payload.decode()
            self.messages_received.put(decoded_message)
        except Exception as e:
            print(f"Error al procesar el mensaje recibido: {e}")

    def on_publish(self, client, userdata, mid):
        print(f"Mensaje {mid} publicado")

    def connect(self):
        try:
            if self.ca_cert and self.certfile and self.keyfile:
                self.client.tls_set(ca_certs=self.ca_cert, certfile=self.certfile, keyfile=self.keyfile, tls_version=ssl.PROTOCOL_TLS)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.on_publish = self.on_publish
            self.client.connect(self.broker, self.puerto, 60)
        except Exception as e:
            print(f"Error al configurar el broker MQTT: {e}")
    
    def subscribe(self, topic):
        try:
            self.client.subscribe(topic, qos=1)
        except Exception as e:
            print(f"Error al suscribirse al tópico MQTT: {e}")

    def publish_messages(self, topic, payload, qos=1):
        try:
            self.client.publish(topic, payload, qos=qos)
        except Exception as e:
            print(f"Error al publicar: {e}")

    def get_messages(self):
        if not self.messages_received.empty():
            return self.messages_received.get()
        return None

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()