# citim de la tastatura un oras si ne intoarce vreamea
# avem un config si daca acele valori sunt depasite sa ne dea o notificare
# notificarea va fi ori pe notification plyer or cu whatsapp
# prima noastra interfata grafica cu gradio
import json
import os
import time
import pywhatkit as wapp
from plyer import notification
import requests


# with statement este context manager
def read_config(path: str = "config.json"):
    try:
        with open(path, "r") as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print("please add the config file!")
        return {}
    return data

def get_weather(config: dict, city: str) -> dict:
    try:
        headers = {"key": os.environ['weather_api_key']}
        url = config['url'] + f"?q={city}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            weather = json.loads(response.text)

            return {"temp": weather['current']['temp_c'],
                    "pressure": weather['current']['pressure_mb'],
                    "wind_speed": weather['current']['wind_kph']
                    }

        elif response.status_code == 401:
            print("plz add a valid API key!")
            return {}

    except Exception as e:
        print(f"Something went wrong {e}!")

def is_worth_notifying(config: dict, weather: dict) -> bool:
    if weather['temp'] > config['max_temp'] or weather['pressure'] > config['max_pressure'] or \
        weather['wind_speed'] > config['max_wind_velocity']:
        return True
    return False



def send_notification(config: dict, weather: dict):
    if is_worth_notifying(config, weather):
        message = f"""
                        Temp: {weather['temp']}
                        Pressure: {weather['pressure']}
                        Wind speed: {weather['wind_speed']}
                        """
        for alert in config['notification_system']:
            if alert == "plyer":
                notification.notify(title=city, message=message, timeout=3)

            elif alert == "whatsapp":
                wapp.sendwhatmsg_instantly(phone_no=os.environ['personal_phone_number'], message=message)
    else:
        pass


#pressure_mb
#wind_kph
#temp_c

if __name__ == '__main__':
    config = read_config()
    while True:
        for city in config['cities']:
            weather = get_weather(config, city)
            print(city + "\n" + json.dumps(weather, indent=4))
            send_notification(config, weather)
            time.sleep(config['sleep_time'])
