# --- mqtt_publisher.py ---
import json
import paho.mqtt.client as mqtt
import base64



MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPICS = {
    "log": "plates/log",
    "db": "plates/db",
    "img": "plates/image"
}

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)

def publish_log_entry(plate, timestamp, confidence, image_path):
    payload = {
        "plate": plate,
        "timestamp": timestamp,
        "confidence": confidence,
        "image_path": image_path
    }
    client.publish(MQTT_TOPICS["log"], json.dumps(payload))

def publish_db():
    with open("logs/plates.db", "rb") as f:
        b64data = base64.b64encode(f.read()).decode()
        client.publish(MQTT_TOPICS["db"], b64data)

def publish_log_file():
    with open("logs/detection.log", "rb") as f:
        b64data = base64.b64encode(f.read()).decode()
        client.publish("plates/logfile", b64data)

def publish_image(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        payload = {
            "filename": path.split("/")[-1],
            "data": b64
        }
        client.publish(MQTT_TOPICS["img"], json.dumps(payload))

