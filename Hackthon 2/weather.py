import requests
import socket
import json

API_KEY = "1ce7b1997960070a3b5fc6d5de870bef" 
CITY = "Tiruvannamalai"                      
SERVER_IP = "192.168.52.153"       
SERVER_PORT = 5005                    

def fetch_weather():
    """Fetch weather data from OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    weather_info = {
        "temperature": data["main"]["temp"],
        "pressure": data["main"]["pressure"],
        "condition": data["weather"][0]["main"]
    }
    return weather_info

def send_to_pi(data):
    """Send weather data to the Raspberry Pi server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, SERVER_PORT))
        s.sendall(json.dumps(data).encode('utf-8'))
        print("Data sent to Raspberry Pi.")

def main():
    try:
        weather_data = fetch_weather()
        print("Weather data:", weather_data)
        send_to_pi(weather_data)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
