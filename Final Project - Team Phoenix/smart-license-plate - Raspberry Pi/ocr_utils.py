# --- ocr_utils.py (Tesseract version) ---
import pytesseract
import cv2
import re

def extract_plate_text(image_region):
    text = pytesseract.image_to_string(image_region, config='--psm 7')
    clean = re.sub(r'[^A-Z0-9]', '', text.upper().strip())
    if 5 <= len(clean) <= 12:
        return clean, 0.95
    return None, 0.0
