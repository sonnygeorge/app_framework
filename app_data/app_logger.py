import logging
from logging.handlers import RotatingFileHandler
import pathlib

folder_path = pathlib.Path("logs")
folder_path.mkdir(parents=True, exist_ok=True)
log_file = pathlib.Path(folder_path, "app.log")
log_file.parent.mkdir(parents=True, exist_ok=True)
format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(format)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=3)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
