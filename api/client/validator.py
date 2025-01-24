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