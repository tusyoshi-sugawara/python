import requests
import json
import setting
import os

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

def main():
    load_dotenv()
    params = {
        "APPID" : os.getenv('API_KEY'),
        "units" : setting.units,
        "zip" : setting.zipcode,
        "lang" : setting.lang
    }
    data = requests.get(setting.weatherurl, params=params, timeout=setting.timeout).json()
    output_dict = {}
    output_dict['description'] = 'openweathermap summary data.'
    output_dict['readtime'] = int(datetime.timestamp(datetime.now()))
    output_dict['country'] = data["sys"]["country"]
    output_dict['city'] = data["name"]

    weather = {}
    weather['main'] = data['weather'][0]['main']
    weather['description'] = data['weather'][0]['description']
    weather['icon'] = data['weather'][0]['icon']
    output_dict['weather'] = weather

    main = {}
    main['temp'] = data['main']['temp']
    main['temp_max'] = data['main']['temp_max']
    main['temp_min'] = data['main']['temp_min']
    main['feels_like'] = data['main']['feels_like']
    main['humidity'] = data['main']['humidity']
    main['pressure'] = data['main']['pressure']
    output_dict['main'] = main

    wind = {}
    wind['deg'] = data['wind']['deg']
    wind['speed'] = data['wind']['speed']
    output_dict['wind'] = wind

    with open(setting.weatherpath, 'w') as file:
        json.dump(output_dict, file, indent=2)

if __name__ == "__main__":
    main()
