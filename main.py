import logging
import wikipedia
from aiogram import Bot, Dispatcher, types


API_TOKEN = "8821798694:AAHa9B9Tbcsf4BivaWILrHYBL9ZJwUTyqBk"
wikipedia.set_lang('uz')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()




@dp.message_handler(Command('start''hello'))
async def send_welcome(message: types.Message):
    await message.answer(f"Assalomu aleykum, {html.bold(message.from_user.full_name)}!")
    await message.answer(f"Sizga qande yordam bera olaman, {message.from_user.full_name}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        respond = wikipedia.summary(message.text)
        await message.answer(respond)
        if (message.text).lower() == "seni kim yaratdi":
            await message.answer("Meni Jasurbek yaratdi")
        elif (message.text).lower() == "sen nima qila olasan":
            await message.answer("Malumot bera olaman")

        else:

            await message.reply(message.text)
    except TypeError:
        await message.answer("Bu mavzuga oid maqola topilmadi!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


