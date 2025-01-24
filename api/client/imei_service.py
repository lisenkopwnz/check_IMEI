from typing import Dict, Any

from api.client.interface import ImeiApiClient
from api.client.request_sender import ImeiRequestSender


class ImeiService(ImeiApiClient):
    """
    Высокоуровневый сервис для работы с API IMEI.
    Использует низкоуровневый клиент для отправки запросов.
    """

    def __init__(self, api_client: ImeiRequestSender):
        """
        Инициализация сервиса.

        :param api_client: Клиент для отправки запросов к API.
        """
        self.api_client = api_client

    async def check_imei(self, url: str, headers: Dict[str, str], body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Отправляет запрос на проверку IMEI через API-клиент.

        :param url: URL API для отправки запроса.
        :param headers: Заголовки HTTP-запроса.
        :param body: Тело запроса в формате JSON.
        :return: Ответ от API в виде словаря.
        """
        result = await self.api_client.check_imei(url=url, headers=headers, body=body)
        return result