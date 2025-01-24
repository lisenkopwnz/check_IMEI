import logging
import httpx
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from bot.services import format_imei_response


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BOT_TOKEN = '7896585189:AAGM10SovQUOSeRo5PaMKZ6LWIZbG4d0VrY'
API_TOKEN = 'MY_SECRET_TOKEN'

# URL api
FASTAPI_API_URL = 'http://127.0.0.1:8000/api/check_imei'

# белый список в демнстративных цнлях такой (нужно добавить свой id лоя проверки
WHITELIST = [1144354970]


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция для проверки доступа
def is_user_allowed(user_id):
    return user_id in WHITELIST

# Обработка команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    if not is_user_allowed(message.from_user.id):
        await message.reply("Доступ запрещен.")
        return

    logger.info(f"Пользователь {message.from_user.id} отправил команду /start")
    await message.reply("Привет! Отправь мне IMEI для проверки.")

@dp.message(Command("help"))
async def send_help(message: Message):
    await message.reply(
        "Доступные команды:\n"
        "/start - Начать работу\n"
        "/help - Получить справку\n\n"
        "Отправьте IMEI для проверки."
    )

# Обработка ввода imei
@dp.message()
async def check_imei(message: Message):
    try:
        if not is_user_allowed(message.from_user.id):
            await message.reply("Доступ запрещен.")
            return

        logger.info(f"Пользователь {message.from_user.id} отправил IMEI: {message.text}")
        imei = message.text.strip()

        if not imei.isdigit() or len(imei) != 15:
            await message.reply("Неверный формат IMEI. IMEI должен состоять из 15 цифр.")
            return

        # Подготовка данных
        payload = {
            "deviceId": imei,
            "serviceId": 1,
            "token": API_TOKEN
        }
        timeout = httpx.Timeout(
            connect=10.0,
            read=10.0,
            write=10.0,
            pool=10.0
        )
        # Отправка запроса
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(FASTAPI_API_URL, json=payload)

            response.raise_for_status()
            result = response.json()
            logger.error(f"result: {result}")

            # форматирвание ответа
            formatted_response = format_imei_response(result)

            await message.reply(formatted_response, parse_mode="Markdown")

    except httpx.HTTPStatusError as e:
        logger.error(f"Ошибка при запросе к API: {e.response.text}")
        await message.reply(f"Ошибка при запросе к API: {e.response.text}")
    except httpx.NetworkError as e:
        logger.error(f"Ошибка сети: {e}")
        await message.reply("Ошибка сети. Проверьте подключение к интернету.")
    except Exception as e:
        logger.error(f"Ошибка при обработке IMEI: {repr(e)}")
        await message.reply("Произошла ошибка при обработке запроса.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
