# thingsboard_sender.py

import paho.mqtt.client as mqtt
import json

# Replace with your actual ThingsBoard Cloud device token
THINGSBOARD_HOST = "mqtt.thingsboard.cloud"
ACCESS_TOKEN = "02xacuf95su6wkm3x6ma"

# Create MQTT client and connect
client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)

def send_to_thingsboard(plate, confidence):
    payload = {
        "plate": plate,
        "confidence": round(confidence, 2)
    }
    client.publish("v1/devices/me/telemetry", json.dumps(payload))

def disconnect_thingsboard():
    client.disconnect()

