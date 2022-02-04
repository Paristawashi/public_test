import requests
import json
from datetime import datetime
import os
from slack_sdk import WebClient


class Read_weather:
    def __init__(self):
        self.url = "https://api.openweathermap.org/data/2.5/onecall?"
        self.city = "1853295"
        self.api = ""
        self.param = {"lat":"35.57","lon":"139.40","appid":self.api,"exclude":"current,minutely","units":"metric"}
        self.dic = {}

    def read_weather(self):
        response = requests.get(self.url,params=self.param).json()
        hourly = response["hourly"]
        daily = response["daily"]
        today_weather = daily[0]
        time = today_weather["dt"]
        time = datetime.fromtimestamp(time)
        temp = today_weather["temp"]
        max_temp = temp["max"]
        min_temp = temp["min"]
        day_temp = temp["day"]
        pop = today_weather["pop"]
        self.dic ={"time":time,"max_temp":max_temp,"min_temp":min_temp,"day_temp":day_temp,"pop":pop}
        return self.dic

class Slack_send:
    def __init__(self,weather_dic):
        self.weather_dic = weather_dic
        self.client = WebClient(token = os.environ.get("SLACK_BOT_TOKEN"))
        self.channel_id = ""

    def slack_send(self):
        result = self.client.chat_postMessage(
            channel = self.channel_id,
            text = str(self.weather_dic["max_temp"])
        )

read_weather = Read_weather()
weather_dic = read_weather.read_weather()

slack_send = Slack_send(weather_dic)
slack_send.slack_send()
