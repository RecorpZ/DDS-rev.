import logging
from datetime import datetime

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Логи в файл
        logging.StreamHandler()          # Логи в консоль
    ]
)

logger = logging.getLogger(__name__)

def log_info(message):
    """Логирование информационных сообщений."""
    logger.info(message)

def log_error(message):
    """Логирование ошибок."""
    logger.error(message)

def log_warning(message):
    """Логирование предупреждений."""
    logger.warning(message)