from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from api.client.imei_service import ImeiService
from api.client.request_sender import ImeiRequestSender
from api.client.validator import ImeiValidator

app = FastAPI()

IMEICHECK_API_TOKEN = "e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b"


class CheckImeiRequest(BaseModel):
    """
    Модель для тела запроса на проверку IMEI.
    """
    deviceId: str
    serviceId: int


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

    # Формируем URL запроса
    url = 'https://api.imeicheck.net/v1/checks'

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
