import logging
from logging import handlers
import os.path

if os.path.exists('logging.log'):
    open("logging.log", "w").close()

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - %(lineno)d - %(levelname)s - %(message)s')
handler = logging.handlers.RotatingFileHandler('logging.log')
handler.setFormatter(formatter)
logger.addHandler(handler)