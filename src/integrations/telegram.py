import os
import requests
from src.utils.logger import get_logger

logger = get_logger(__name__)

def send_message(text: str) -> bool:
    """
    Envía un mensaje formateado en Markdown a tu canal o chat de Telegram.
    Necesita en .env:
        TELEGRAM_BOT_TOKEN=
        TELEGRAM_CHAT_ID=
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logger.error("❌ TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID no están configurados.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }

    try:
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            logger.info("📩 Mensaje enviado a Telegram.")
            return True
        else:
            logger.error(f"❌ Error enviando mensaje: {resp.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Excepción enviando a Telegram: {e}")
        return False

