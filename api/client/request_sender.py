import httpx
from fastapi import HTTPException
from typing import Dict, Any


class ImeiRequestSender:
    """
    Класс для отправки запросов к API IMEI.
    Реализует интерфейс ImeiApiClient.
    """

    def __init__(self, api_key: str):
        """
        Инициализация клиента.

        :param api_key: API-ключ для авторизации.
        """
        self.api_key = api_key

    async def check_imei(self, url: str, headers: Dict[str, str], body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Отправляет запрос на проверку IMEI.

        :param url: URL API для отправки запроса.
        :param headers: Заголовки HTTP-запроса.
        :param body: Тело запроса в формате JSON.
        :return: Ответ от API в виде словаря.
        :raises HTTPException: Если произошла ошибка при запросе к API.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=body)

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Ошибка при запросе к API. Статус: {response.status_code}, Ответ: {response.text}"
                    )
                return response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=500, detail=f"Ошибка при запросе к API: {str(e)}")
            except httpx.RequestError as e:
                raise HTTPException(status_code=500, detail=f"Ошибка сети: {str(e)}")
            except ValueError as e:
                raise HTTPException(status_code=500, detail=f"Некорректный ответ от сервера: {str(e)}")