import cv2
import os
import csv
import time
from datetime import datetime
from ocr_utils import extract_plate_text
from camera_utils import get_plate_region
from db_utils import init_db, insert_log, save_snapshot
from log_utils import get_logger
from mqtt_publisher import publish_log_entry, publish_db, publish_log_file, publish_image
from gpiozero import Button, LED
from time import sleep
from pioneer_buzzer import PioneerBuzzer
from thingsboard_mqtt import send_to_thingsboard, disconnect_thingsboard  # ← NEW

# GPIO setup
button = Button(20, pull_up=True)
led = LED(26)
buzzer = PioneerBuzzer()

# Camera setup
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
if not cap.isOpened():
    raise IOError("Cannot open USB camera.")

# Create folders
os.makedirs("snapshots", exist_ok=True)
os.makedirs("num_plate", exist_ok=True)

csv_file = "log_input.csv"
init_db()
logger = get_logger()

# Create CSV log file if not present
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as f:
        csv.writer(f).writerow(["plate", "timestamp", "confidence", "image"])

# State variables
last_seen = {}
duplicate_timeout = 15
capture_enabled = False
capture_list = []

print("System live. Detection is ON.")
print("Press the button to capture 3 unique detections.")
print("Hold button 3s to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera frame error.")
        break

    roi, bbox = get_plate_region(frame)

    if roi is not None:
        plate_text, confidence = extract_plate_text(roi)
        now = time.time()

        if plate_text:
            x, y, w, h = bbox
            cv2.putText(frame, f"{plate_text} ({confidence:.2f})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if capture_enabled and plate_text not in capture_list and \
                    (plate_text not in last_seen or now - last_seen[plate_text] > duplicate_timeout):

                last_seen[plate_text] = now
                capture_list.append(plate_text)

                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                snapshot_name = f"{plate_text}_{timestamp}.jpg"
                frame_path = os.path.join("snapshots", snapshot_name)
                plate_path = os.path.join("num_plate", f"plate_{timestamp}.jpg")

                cv2.imwrite(frame_path, frame)
                cv2.imwrite(plate_path, roi)

                with open(csv_file, mode='a', newline='') as f:
                    csv.writer(f).writerow([plate_text, timestamp, round(confidence, 2), frame_path])

                db_frame_path = save_snapshot(frame, plate_text)
                insert_log(plate_text, timestamp, confidence, db_frame_path)
                logger.info(f"[{len(capture_list)}] Detected: {plate_text}, Confidence: {confidence:.2f}")

                publish_log_entry(plate_text, timestamp, confidence, db_frame_path)
                publish_image(db_frame_path)
                publish_db()
                publish_log_file()

                # ✅ Send to ThingsBoard Cloud
                send_to_thingsboard(plate_text, confidence)

                print(f"[{len(capture_list)}] Detected: {plate_text} (Confidence: {confidence:.2f})")

                if len(capture_list) >= 3:
                    print("✅ 3 unique detections captured. Beeping...")
                    for _ in range(3):
                        buzzer.beep(0.5)
                        sleep(0.5)
                    capture_enabled = False
                    capture_list.clear()
                    led.off()  # Turn off LED

    # Show camera feed
    cv2.imshow("Live Plate Detection", frame)

    # Button press logic
    if button.is_pressed:
        press_start = time.time()
        while button.is_pressed:
            if time.time() - press_start >= 3:
                print("Long press detected. Exiting...")
                cap.release()
                cv2.destroyAllWindows()
                led.off()
                disconnect_thingsboard()  # ← NEW
                exit(0)
            sleep(0.01)

        capture_enabled = True
        capture_list.clear()
        led.on()  # Turn on LED on button press
        print("📸 Ready to capture 3 unique detections...")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
led.off()
disconnect_thingsboard()  # ← NEW
print("Application closed.")
