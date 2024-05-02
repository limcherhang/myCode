"""
    從emissionAsset完善mysql的emissionFactor
"""
import os
import sys
rootPath = os.getcwd() + '/../'
sys.path.append(rootPath)
import configparser
from connection.mongo_connection import MongoConn
from connection.mysql_connection import MySQLConn
import pymysql
import pymongo
from utils.util import get_logger
from bson import ObjectId
import time

def getEmissionAsset(cursor: pymysql.cursors.Cursor):
    sqlCommand = f"""
        SELECT companyId, sourceOfEmission, vehicleType, fuelEfficiency, co2Factor, ch4Factor, n2oFactor, ar4Factor, ar5Factor, baseUnit, source, urlName, sheetName, file, link, year, emissionUnit, ch4Unit, n2oUnit, sourceType, sId FROM emissionFactor.emissionAsset;
    """

    cursor.execute(sqlCommand)
    return cursor.fetchall()

if __name__ == '__main__':
    startTime = time.time()
    config = configparser.ConfigParser()
    config.read(rootPath+'/config.ini')

    file = __file__
    basename = os.path.basename(file)
    logFile = os.path.splitext(basename)[0]+'.log'

    logger = get_logger('./log/', logFile)

    conn = MySQLConn(config['mysql_azureV2'])

    with conn.cursor() as cursor:
        emissionAsset = getEmissionAsset(cursor)

        for companyId, sourceOfEmission, vehicleType, fuelEfficiency, co2Factor, ch4Factor, n2oFactor, ar4Factor, ar5Factor, baseUnit, source, urlName, sheetName, _file, link, year, emissionUnit, ch4Unit, n2oUnit, sourceType, sId in emissionAsset:
            value_string = f"""("{sourceOfEmission}", '{companyId}', '{vehicleType}', {fuelEfficiency}, {co2Factor}, {ch4Factor}, {n2oFactor}, {ar4Factor}, {ar5Factor}, '{baseUnit}', '{source}', '{urlName}', '{sheetName}', '{_file}', '{link}', {year}, '{emissionUnit}', '{ch4Unit}', '{n2oUnit}', '{sourceType}', {sId})""".replace("None", "NULL").replace("'NULL'","NULL").replace('"NULL"',"NULL")

            replace_sql = f"""
                REPLACE INTO emissionFactor.emissionFactor(sourceOfEmission, companyId, vehicleType, fuelEfficiency, co2Factor, ch4Factor, n2oFactor, ar4Factor, ar5Factor, baseUnit, source, urlName, sheetName, file, link, year, emissionUnit, ch4Unit, n2oUnit, sourceType, sId) VALUES {value_string}
            """
            
            logger.debug(replace_sql)
            cursor.execute(replace_sql)
            logger.debug("REPLACE SUCCEED!")
    
    conn.close()