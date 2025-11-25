# logger_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

# Папка для логов
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Общий формат логов
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] — %(message)s"

def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: str = "app.log",
    max_bytes: int = 5 * 1024 * 1024,   # 5 MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Создаёт и настраивает логер.
    Можно вызывать из любого файла: logger = setup_logger(__name__)
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # — чтобы логер не создавал дублирующие хендлеры при повторном импорте
    if logger.handlers:
        return logger

    # Handler: лог в файл (с ротацией)
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, log_file),
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    # Handler: вывод в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
