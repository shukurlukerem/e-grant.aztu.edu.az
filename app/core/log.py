import logging
from logging.handlers import RotatingFileHandler
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger("fastapi_app_logger")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("logs/app.log", maxBytes=5 * 1024 * 1024, backupCount=3)
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
