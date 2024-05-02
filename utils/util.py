import os
import logging
from logging.handlers import TimedRotatingFileHandler

def get_logger(logPath: str, filename: str, level: str=logging.DEBUG):
    
    check_if_folder_exists(logPath)
    logfile = f"{logPath}/{filename}"

    logging.basicConfig(handlers=[TimedRotatingFileHandler(logfile , when='midnight')], level=level, encoding='utf-8', format='%(asctime)s.%(msecs)03d %(name)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    
    logger = logging.getLogger(__name__)
    return logger

def check_if_folder_exists(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass