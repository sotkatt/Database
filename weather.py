import requests
from pprint import pprint
from datetime import datetime

API = "f79bd8676437b40dbd8b56cf03c1f75c"
city = "Almaty"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric"

res =  requests.get(url)
data = res.json()

sunrise = datetime.fromtimestamp(data["sys"]["sunrise"])
sunset = datetime.fromtimestamp(data["sys"]["sunset"])

info = f"""
Город: {data["name"]}
Температура: {data["main"]["temp"]}
Давление: {data["main"]["pressure"]}
Влажность: {data["main"]["humidity"]}
Скорось ветра: {data["wind"]["speed"]}

Пагода: {data["weather"][0]["description"]}
Восход солнце: {sunrise.time()}
Продол-ть дня: {sunset - sunrise}
Закат солнце: {sunset.time()}
"""
print(info)
