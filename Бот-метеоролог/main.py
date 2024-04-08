import asyncio

import discord
import requests
from discord.ext import commands

from config import BOT_TOKEN

API_URL = "https://api.weather.yandex.ru/v2/forecast"

# бесплатный на 7 дней
YANDEX_API_KEY = "66c26159-3595-4c81-87fa-8b5809952357"

local_storage = {}


class Place:
    def __init__(self, latitude, longitude, name):
        self.latitude = latitude
        self.longitude = longitude
        self.placename = name


WIND_DIRECTION = {
    "nw": "северо-западное", "n": "северное", "sw": "юго-западное",
    "ne": "северо-восточное", "e": "восточное", "w": "западное",
    "se": "юго-восточное", "s": "южное", "c": "штиль"
}

PREC = {
    0: "без осадков", 1: "дождь", 2: "дождь со снегом",
    3: "снег", 4: "град"
}


class YLBotClient(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help_bot')
    async def help(self, ctx):
        await ctx.send(f"/help_bot - инструкция по работе команд\n"
                       f'/place <place> - задать место прогноза\n'
                       f"/current - сообщение о текущей погоде\n"
                       f"/forecast <days> - прогноз на <days> дней")

    @commands.command(name="place")
    async def place(self, ctx, *, place_name):
        geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
        response = requests.get(geocoder_uri, params={
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "format": "json",
            "geocode": place_name
        })

        if not response:
            await ctx.send("Ошибка выполнения HTTP запроса\n"
                           f"HTTP статус: {response.status_code} ({response.reason})")
            return

        results = response.json()["response"]["GeoObjectCollection"]["featureMember"]
        if len(results) == 0:
            await ctx.send(
                f"Не удалось найти место по переданному тексту: {place_name}. Проверьте, может вы ошиблись в написании."
            )
            return

        toponym = results[0]["GeoObject"]
        longitude, latitude = toponym["Point"]["pos"].split()
        local_storage[ctx.message.author] = Place(
            latitude, longitude, toponym['name'] + ", " + toponym['description']
        )
        message = "Место прогноза успешно установлено: " + toponym['name'] + ", " + toponym['description']
        await ctx.send(message)

    @commands.command(name="current")
    async def current(self, ctx):
        place = local_storage.get(ctx.message.author, None)
        if not place:
            return await ctx.send(
                "Ошибка. Укажите место прогноза."
            )

        r = requests.get(API_URL, params={
            "latitude": place.latitude, "longitude": place.longitude,
            "lang": "ru_RU", "limit": 1, "hours": "false"
        }, headers={"X-Yandex-Weather-Key": YANDEX_API_KEY})
        print(r.text)
        resp = r.json()["fact"]

        await ctx.send(
            f"Прогноз на сегодня, {place.placename}:\n"
            f"Температура: {resp['temp']} °C\n"
            f"Давление: {resp['pressure_mm']} мм рт. ст.\n"
            f"Влажность: {resp['humidity']}%\n"
            f"Направление ветра: {WIND_DIRECTION[resp['wind_dir']]}\n"
            f"Сила ветра: {resp['wind_speed']} м/c"
        )

    @commands.command(name="forecast")
    async def forecast(self, ctx, days):
        place = local_storage.get(ctx.message.author, None)
        if not place:
            return await ctx.send(
                "Ошибка. Укажите место прогноза."
            )
        if int(days) > 7:
            return await ctx.send(
                "Извините. Мы можем выдавать прогноз максимум на 7 дней"
            )

        r = requests.get(API_URL, params={
            "lat": place.latitude, "lon": place.longitude,
            "lang": "ru_RU", "limit": int(days), "hours": "false"
        }, headers={"X-Yandex-API-Key": YANDEX_API_KEY})
        resp = r.json()["forecasts"]

        resp_text = ""
        for forecast in resp:
            resp_text += f"Прогноз погоды на {forecast['date']} дн., {place.placename}:\n" \
                         f"Средняя дневная температура: {forecast['parts']['evening']['temp_avg']}\n" \
                         f"Тип осадков: {PREC[forecast['parts']['evening']['prec_type']]}\n\n"

        await ctx.send(resp_text)


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


async def main():
    await bot.add_cog(YLBotClient(bot))
    await bot.start(BOT_TOKEN)


asyncio.run(main())
