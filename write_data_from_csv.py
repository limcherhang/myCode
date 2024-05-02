import os
import sys
rootPath = os.getcwd()
sys.path.append(rootPath)
import configparser
import pandas as pd
import datetime
from sqlalchemy import create_engine

from connection.mysql_connection import MySQLConn
from utils.util import get_logger

# [mysql_azureV2]
# host= 20.205.24.18
# port= 3306
# user= eco
# password= ECO4ever

if __name__ == '__main__':
    
    file = __file__
    basename = os.path.basename(file)
    filename = os.path.splitext(basename)[0]
    logPath = os.getcwd()+ '/log'

    config = configparser.ConfigParser()
    config.read(rootPath+'/config.ini')

    con = 'mysql+pymysql://eco:ECO4ever@20.205.24.18:3306/rawData2023'
    engine = create_engine(con)

    logger = get_logger(logPath, f"{filename}.log")

    path = './result'

    files = [os.path.join(path, file) for file in os.listdir(path)]

    for file in files:
        df = pd.read_csv(file)
        
        df.to_sql(name='zigbee_11', con=engine, if_exists='append', index=False)
    
    engine.dispose()