import socket
import json
from gpiozero import LED
from time import sleep
from PIL import Image, ImageDraw, ImageFont
from oled import SSD1306

RST = 19  # Reset pin
DC = 16   # Data/Command pin
oled = SSD1306(rst_pin=RST, dc_pin=DC)

led = LED(26)
TEMP_THRESHOLD = 30.0

font = ImageFont.load_default()

def display_weather(temp, pressure, condition):
    """Render weather data on the OLED screen."""
    image = Image.new('1', (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), f"Temp: {temp:.1f} C", font=font, fill=255)
    draw.text((0, 16), f"Press: {pressure} hPa", font=font, fill=255)
    draw.text((0, 32), f"Cond: {condition}", font=font, fill=255)

    oled.image(image)
    oled.show()

def handle_led(temp):
    """Turn LED on GPIO26 ON if temp > 30°C"""
    if temp > TEMP_THRESHOLD:
        led.on()
    else:
        led.off()

def start_server(host='', port=5005):
    """Socket server to receive weather data from client."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print(f"[SERVER] Listening on port {port}...")

    while True:
        conn, addr = s.accept()
        print(f"[SERVER] Connected by {addr}")
        data = conn.recv(1024)
        if data:
            try:
                weather = json.loads(data.decode('utf-8'))
                temp = weather["temperature"]
                pressure = weather["pressure"]
                condition = weather["condition"]

                print(f"[SERVER] Received: {weather}")
                display_weather(temp, pressure, condition)
                handle_led(temp)

            except Exception as e:
                print("[SERVER] Error:", e)
        conn.close()

if __name__ == "__main__":
    start_server()
