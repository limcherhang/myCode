import os
import sys
rootPath = os.getcwd() + '/../'
sys.path.append(rootPath)
import configparser
import datetime
import pandas as pd

from connection.mysql_connection import MySQLConn
from utils.util import get_logger

if __name__ == '__main__':
    file = __file__
    basename = os.path.basename(file)
    filename = os.path.splitext(basename)[0]
    logPath = os.getcwd()+ '/log'

    config = configparser.ConfigParser()
    config.read(rootPath+'/config.ini')

    checkFiles = [file for file in os.listdir('./') if '-' in file]
    Count = 0
    for file in checkFiles:
        df = pd.read_excel(file, sheet_name='DataETL')
        Count += len(df.values.tolist())
    print(Count)