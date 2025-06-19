# --- db_utils.py ---
import sqlite3
import os
import cv2
import time

DB_PATH = 'logs/plates.db'
IMG_DIR = 'logs/snaps'

os.makedirs('logs', exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS plate_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate TEXT,
            timestamp TEXT,
            confidence REAL,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_log(plate, timestamp, confidence, image_path):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO plate_logs (plate, timestamp, confidence, image_path)
        VALUES (?, ?, ?, ?)
    ''', (plate, timestamp, confidence, image_path))
    conn.commit()
    conn.close()

def save_snapshot(frame, plate_text):
    filename = f"{plate_text}_{int(time.time())}.jpg"
    full_path = os.path.join(IMG_DIR, filename)
    cv2.imwrite(full_path, frame)
    return full_path
