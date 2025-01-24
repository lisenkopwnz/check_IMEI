from api.client.config import API_TOKEN


class ImeiValidator:
    """
    Класс для валидации IMEI.
    """

    @staticmethod
    def validate(device_id: str) -> bool:
        """
        Проверяет, является ли строка корректным IMEI.

        :param device_id: Строка для проверки.
        :return: True, если строка является корректным IMEI, иначе False.
        """
        return len(device_id) == 15 and device_id.isdigit()

    @staticmethod
    def validate_secret_key(key):
        """
        Проверяю ключь на соответствие
        :param key: ключь передаваемый клиентским кодом
        :return: True, если строка является корректным APIREY, иначе False.
        """
        return key == API_TOKEN
