# Smart License Plate Detection System 🚘🔍

This project is a real-time smart license plate detection and logging system. It uses OpenCV for plate detection, Tesseract OCR for text recognition, and integrates with GPIO hardware for interaction on a Raspberry Pi using the Waveshare Pioneer600 HAT. It also supports MQTT and ThingsBoard integration for remote monitoring.

## 🔧 Features

- Live video feed for capturing vehicle license plates
- OCR using Tesseract to read plate numbers
- Button-triggered detection via GPIO
- Buzzer indication after successful detection
- Logs entries with timestamp, plate number, and snapshot
- Web dashboard (Flask) to view logs and snapshots
- MQTT integration for remote publishing
- Optional ThingsBoard integration

---

## 🧰 Requirements

### Hardware
- Raspberry Pi
- Waveshare Pioneer600 HAT
- USB Webcam
- Buzzer
- Button (on Pioneer600)

### Software
- Python 3.x
- OpenCV
- Tesseract OCR
- Flask
- SQLite
- MQTT (paho-mqtt)
- Pillow
- gpiozero / lgpio
- thingsboard_gateway (optional)

Install dependencies:

```bash
sudo apt update
sudo apt install python3-opencv python3-gpiozero tesseract-ocr
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
smart-license-plate/
│
├── app.py                      # Flask web dashboard
├── main.py                     # Main detection script
├── ocr_utils.py                # OCR helper functions
├── camera_utils.py             # Plate detection functions
├── gpio_control.py             # GPIO logic
├── mqtt_publisher.py           # MQTT logic
├── thingsboard_sender.py       # ThingsBoard integration
├── db_utils.py                 # SQLite logging
├── log_utils.py                # Logger config
├── templates/
│   └── dashboard.html          # Web dashboard UI
├── static/
│   └── snaps/                  # Snapshot images
├── logs/
│   ├── plates.db               # SQLite DB
│   └── snap/                   # Saved snapshots
└── README.md                   # You are here
```

---

## ▶️ Usage

### On Raspberry Pi:

1. **Start detection:**
   ```bash
   python3 main.py
   ```

   - Press the physical button on Pioneer600 to trigger detection.
   - After 3 presses, the script stops automatically.

2. **Access Web Dashboard:**
   ```bash
   python3 app.py
   ```

   Open your browser at: `http://<raspberry-pi-ip>:5000`

---

## 🌐 MQTT / ThingsBoard

- MQTT messages are published to broker (configure in `mqtt_publisher.py`)
- To use ThingsBoard, set your `ACCESS_TOKEN` and server in `thingsboard_sender.py`

---

## 📸 Snapshots & Logs

- Snapshots saved in: `logs/snaps/`
- Log entries saved in: `logs/plates.db`
- Dashboard displays a table of all logs with timestamps and images

---

## 🛠️ Notes

- Adjust Haar cascade or detection logic in `camera_utils.py` for best results
- For debugging, logs are handled by `log_utils.py`
