"""
    取得cal_approches的所有keys
    和
    methods的key
    以及
    methods底下有什麼source
"""
import os
import sys
rootPath = os.getcwd() + '/../'
sys.path.append(rootPath)
import configparser
from connection.mongo_connection import MongoConn
from connection.mysql_connection import MySQLConn
import pymysql
from utils.util import get_logger
from bson import ObjectId
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
    client = MongoConn(config['mongo_dev_v1_nxmap'])
    client.connect()

    # Get database
    db = client.get_database()

    pipeline = [
        {"$project": {"arrayofkeyvalue": {"$objectToArray": "$$ROOT"}}},
        {"$unwind": "$arrayofkeyvalue"},
        {"$group": {"_id": None, "allkeys": {"$addToSet": "$arrayofkeyvalue.k"}}}
    ]

    result = db.cal_approaches.aggregate(pipeline)
    for res in result:
        logger.debug(res)
        logger.debug("")

    
    data = db.cal_approaches.find({})

    method_keys = set()
    method_source = []

    for d in data:
        for method in d['methods']:
            method_keys.update(method.keys())
            if method['source'] not in method_source:
                method_source.append(method['source'])
    
    logger.debug(method_keys)
    logger.debug(method_source)

    client.close()