import os
from pydoc import describe
import asyncio
import logging
import sys
import html
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
load_dotenv()
API=os.getenv("API")
TOKEN = os.getenv("Bot")
dp = Dispatcher()


@dp.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

import aiohttp
async def OBU_Havo(site:str) ->  None:
    url="https://api.openweathermap.org/data/2.5/weather"
    params={"q":site,"appid":API,"units":"metric"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url,params=params) as resp:
            if resp.status != 200:
                return None
            return  await resp.json()

WEATHER_UZ = {
    800: "Ochiq, bulutsiz havo",
    801: "Kam bulutli",
    802: "Qisman bulutli",
    500: "Yengil yomg'ir",
    601: "Qor",
    # ...
}

GROUP_UZ = {2: "Momaqaldiroq", 3: "Shivalama", 5: "Yomg'ir",
            6: "Qor", 7: "Tuman", 8: "Bulutli"}

def describe(weather_id: int) -> str:
    return WEATHER_UZ.get(weather_id) or GROUP_UZ.get(weather_id // 100, "Noma'lum")
from datetime import datetime, timedelta, timezone

def local_time(ts: int, shift: int) -> str:
    tz = timezone(timedelta(seconds=shift))
    return datetime.fromtimestamp(ts, tz=tz).strftime("%H:%M")
WIND_DIRS = ["Shimoliy", "Sh-Sharqiy", "Sharqiy", "J-Sharqiy",
             "Janubiy", "J-G'arbiy", "G'arbiy", "Sh-G'arbiy"]

def wind_direction(deg: float) -> str:
    return WIND_DIRS[round(deg / 45) % 8]


def formatlash(data:dict) -> str:
    ICON_EMOJI = {
        "01d": "☀️", "01n": "🌙",
        "02d": "🌤", "02n": "☁️",
        "10d": "🌦", "10n": "🌧",
        "13d": "❄️", "13n": "❄️",
        "50d": "🌫", "50n": "🌫",
    }  # "🌡"
    name = html.escape(data["name"])
    country=data['sys'].get("country","")
    w = data["weather"][0]
    main=data["main"]
    shift = data['timezone']
    emoji=ICON_EMOJI.get(w['icon'],"🌡")

    return (
        f"{emoji} <b>{name}, {country}</b>\n"
        f"<i>{describe(w['id'])}</i>\n\n"
        f"🌡 Harorat: <b>{main['temp']:.0f}°C</b> "
        f"(his qilinishi {main['feels_like']:.0f}°C)\n"
        f"💧 Namlik: {main['humidity']}%\n"
        f"💨 Shamol: {data['wind']['speed']:.1f} m/s, "
        f"{wind_direction(data['wind'].get('deg', 0))}\n\n"
        f"🌅 Quyosh chiqishi: {local_time(data['sys']['sunrise'], shift)}\n"
        f"🌇 Quyosh botishi: {local_time(data['sys']['sunset'], shift)}"
    )


@dp.message()
async def echo_handler(message: Message) -> None:
    lupa = await message.answer("🔎")
    try:
        obu = await OBU_Havo(message.text)
        obu = formatlash(obu)
        await message.answer(obu)
    except TypeError:
        await message.answer("Xato")
    finally:
        await lupa.delete()


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
