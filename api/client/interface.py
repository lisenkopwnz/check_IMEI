from abc import ABC, abstractmethod
from typing import Dict, Any


class ImeiApiClient(ABC):
    """
    Абстрактный базовый класс для клиентов API, работающих с проверкой IMEI.
    Определяет контракт для методов, которые должны быть реализованы в дочерних классах.
    """

    @abstractmethod
    async def check_imei(self, url: str, headers: Dict[str, str], body: Dict[str, Any]) -> Dict[str, Any]:
        """
        Абстрактный метод для отправки запроса на проверку IMEI.

        :param url: URL API для отправки запроса.
        :param headers: Заголовки HTTP-запроса.
        :param body: Тело запроса в формате JSON.
        :return: Ответ от API в виде словаря.
        """
        pass