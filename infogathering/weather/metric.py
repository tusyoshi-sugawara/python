import requests
import json
import setting
import os

from pprint import pprint
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

def main():
    load_dotenv()
    params = {
        "APPID" : os.getenv('API_KEY'),
        "units" : setting.units,
        "zip" : setting.zipcode
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
        value_dict['weather'] = val["weather"][0]["main"]
        value_dict['temp'] = val["main"]["temp"]
        value_dict['feels_like'] = val["main"]["feels_like"]
        value_dict['pressure'] = val["main"]["pressure"]
        value_dict['humidity'] = val["main"]["humidity"]
        value_dict['wind_deg'] = val["wind"]["deg"]
        value_dict['wind_speed'] = val["wind"]["speed"]
        list.append(value_dict)
    output_dict['list'] = list
    with open(setting.metricPath, 'w') as file:
        json.dump(output_dict, file, indent=2)

if __name__ == "__main__":
    main()
