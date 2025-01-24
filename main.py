import asyncio
import logging
import subprocess
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from api.client.config import IMEICHECK_API_TOKEN, URL
from api.client.imei_service import ImeiService
from api.client.request_sender import ImeiRequestSender
from api.client.validator import ImeiValidator
from bot.imei_bot import main


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запуск бота при старте приложения
    bot_task = asyncio.create_task(main())
    yield  # Приложение работает здесь
    bot_task.cancel()
    try:
        await bot_task
    except asyncio.CancelledError:
        print("Бот остановлен.")

app = FastAPI(lifespan=lifespan)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CheckImeiRequest(BaseModel):
    """
    Модель для тела запроса на проверку IMEI.
    """
    deviceId: str
    serviceId: int
    token: str


@app.post('/api/check_imei')
async def check_imei(request: CheckImeiRequest):
    """
    Эндпоинт для проверки IMEI.

    :param request: Тело запроса, содержащее IMEI и ID услуги.
    :return: Ответ от API в виде словаря.
    :raises HTTPException: Если IMEI некорректен или произошла ошибка при запросе к API.
    """
    # Создаю экземпляр валидатора
    validator = ImeiValidator()
    if not validator.validate(request.deviceId):
        raise HTTPException(status_code=400, detail="Некорректный IMEI")
    if not validator.validate_secret_key(request.token):
        raise HTTPException(status_code=403, detail="Неверный токен, отказано в доступе")
    logger.info(f"Полученный токен: {request.token}")

    url = URL

    # Заголовки запроса
    headers = {
        'Authorization': 'Bearer ' + IMEICHECK_API_TOKEN,
        'Content-Type': 'application/json'
    }

    # Тело запроса
    body = {
        "deviceId": request.deviceId,
        "serviceId": request.serviceId
    }
    # Создаю экземпляр клиента
    client = ImeiRequestSender(IMEICHECK_API_TOKEN)

    # Создаю экземпляр сервиса
    imei_service = ImeiService(api_client=client)

    # Отправляем запрос через сервис
    result = await imei_service.check_imei(url, headers, body)

    return result

if __name__ == '__main__':

    uvicorn.run(app, host="0.0.0.0", port=8000)
