import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_imei_response(api_response):
    """
    Форматирует ответ от API в читаемый вид.
    """
    try:
        response_data = json.loads(api_response['detail'].split("Ответ: ")[1])

        device_name = response_data['properties']['deviceName']
        imei = response_data['properties']['imei']
        warranty_status = response_data['properties']['warrantyStatus']
        purchase_country = response_data['properties']['purchaseCountry']
        model_name = response_data['properties']['apple/modelName']
        image_url = response_data['properties']['image']


        formatted_response = (
            f"📱 *Информация об устройстве:*\n"
            f"- Модель: {device_name}\n"
            f"- IMEI: {imei}\n"
            f"- Статус гарантии: {warranty_status}\n"
            f"- Страна покупки: {purchase_country}\n"
            f"- Модель: {model_name}\n"
            f"- Изображение: [Ссылка]({image_url})"
        )
        return formatted_response
    except Exception as e:
        logger.error(f"Ошибка при форматировании ответа: {repr(e)}")
        return "Не удалось обработать ответ от API."
