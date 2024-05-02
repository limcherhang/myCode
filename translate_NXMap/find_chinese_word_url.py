import os
import sys
rootPath = os.getcwd() + '/../'
sys.path.append(rootPath)
import configparser
from connection.mongo_connection import MongoConn
from utils.util import get_logger
import time

if __name__ == '__main__':
    startTime = time.time()
    config = configparser.ConfigParser()
    config.read(rootPath+'/config.ini')

    file = __file__
    basename = os.path.basename(file)
    logFile = os.path.splitext(basename)[0]+'.log'

    logger = get_logger('./log/', logFile)


    # Create mongo connection
    client = MongoConn(config['mongo_staging'])
    client.connect()

    # Get database
    db = client.get_database()

    translation = db.translations.find({"tran.name":'tw'}, {"_id":0, "url":1, "tran.$":1})
    target = "啟動專案"
    for res in translation:
        url = res["url"]
        for t in res['tran']:
            tw = 

    client.close()