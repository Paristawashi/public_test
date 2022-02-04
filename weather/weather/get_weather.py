import requests
import json

"""
dtはtimestamp担っているので、使用する際には

-----------
from datetime import datetime

dt = datetime.fromtimestamp(dt)
-----------
等を用いて日付表示等に直して使ってください
"""

def get_weather(lat = 35.57,lon = 139.40,take_type = "daily",get_num = 0):
    url = "https://api.openweathermap.org/data/2.5/onecall?"
    take_type = "daily"
    api = "55975281b7070279ccae4910e8276de7"

    param = {"lat":lat,"lon":lon,"appid":api,"units":"metric"}

    response = requests.get(url,params = param).json()
    str = response[take_type][get_num]

    dt = str["dt"]
    pop = str["pop"]
    max_temp = str["temp"]["max"]
    min_temp = str["temp"]["min"]
    day_temp = str["temp"]["day"]

    dic = {"dt":dt,"pop":pop,"max_temp":max_temp,"min_temp":min_temp,"day_temp":day_temp}
    return dic
