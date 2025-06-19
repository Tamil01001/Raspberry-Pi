# --- mqtt_subscriber.py ---
import os
import base64
import json
import sqlite3
import paho.mqtt.client as mqtt

# Create local directories to store logs and snapshots
os.makedirs("logs/snaps", exist_ok=True)

# HiveMQ Public Broker
BROKER = "broker.hivemq.com"
PORT = 1883

TOPICS = [
    ("plates/log", 0),
    ("plates/db", 0),
    ("plates/image", 0),
    ("plates/logfile", 0)
]

DB_PATH = "logs/plates.db"
LOG_PATH = "logs/detection.log"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Connected to HiveMQ broker")
        client.subscribe(TOPICS)
    else:
        print("❌ Failed to connect. Return code:", rc)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode(errors="ignore")

    if topic == "plates/db":
        with open(DB_PATH, "wb") as f:
            f.write(base64.b64decode(payload))
        print("✅ Received updated database.")

    elif topic == "plates/logfile":
        with open(LOG_PATH, "wb") as f:
            f.write(base64.b64decode(payload))
        print("✅ Received updated log file.")

    elif topic == "plates/image":
        data = json.loads(payload)
        image_path = os.path.join("logs/snaps", data["filename"])
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(data["data"]))
        print("🖼️ Received image:", data["filename"])

    elif topic == "plates/log":
        data = json.loads(payload)
        print(f"🔍 Plate: {data['plate']}, Time: {data['timestamp']}, Confidence: {data['confidence']:.2f}")

# Initialize MQTT client
client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

# Connect to HiveMQ broker
client.connect(BROKER, PORT)

# Blocking call that processes network traffic, dispatches callbacks
client.loop_forever()
