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
    data = requests.get(setting.metricurl, params=params, timeout=setting.timeout).json()
    output_dict = {}
    output_dict['description'] = 'openweathermap metric summary data.'
    output_dict['readtime'] = int(datetime.timestamp(datetime.now()))
    output_dict['country'] = data["city"]["country"]
    output_dict['city'] = data["city"]["name"]

    tz = timezone(timedelta(hours =+ 9), "JST")
    i = 0
    list = []
    for val in data["list"]:
        value_dict = {}
        value_dict['datetime'] = datetime.fromtimestamp(val["dt"], tz).strftime('%Y/%m/%d %H')

        weather = {}
        weather['main'] = val["weather"][0]["main"]
        weather['description'] = val["weather"][0]["description"]
        weather['icon'] = val["weather"][0]["icon"]
        value_dict['weather'] = weather

        main = {}
        main['temp'] = val["main"]["temp"]
        main['feels_like'] = val["main"]["feels_like"]
        main['pressure'] = val["main"]["pressure"]
        main['humidity'] = val["main"]["humidity"]
        value_dict['main'] = main

        wind = {}
        wind['wind_deg'] = val["wind"]["deg"]
        wind['wind_speed'] = val["wind"]["speed"]
        value_dict['wind'] = wind

        list.append(value_dict)
    output_dict['list'] = list
    with open(setting.metricpath, 'w') as file:
        json.dump(output_dict, file, indent=2)

if __name__ == "__main__":
    main()
