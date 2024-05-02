from connection.mysql_connection import MySQLConn
from utils.util import get_logger

import configparser

filename = __file__
last_slash = filename.rfind('/')
logFile = filename[last_slash+1:-2]+'log'

logger = get_logger('./log/', logFile)


config = configparser.ConfigParser()
config.read("config.ini")


conn_42 = MySQLConn(config["mysql_42"])

with conn_42.cursor() as cursor_42:
    sqlCommand = "SELECT * FROM mgmtETL.vDataETLInfo;"
    cursor_42.execute(sqlCommand)
    result = cursor_42.fetchall()

conn_42.close()
conn_own = MySQLConn(config["mysql_own"])

with conn_own.cursor() as cursor_own:
    cursor_own.execute("SET SQL_SAFE_UPDATES = 0;")
    cursor_own.execute("DELETE FROM mgmtETL.vDataETLInfo;")
    cursor_own.execute("SET SQL_SAFE_UPDATES = 1;")
    for row in result:
        (
        siteId, siteName, name, nameDesc, ieee, gatewayId, typeDesc, logicDesc, dataTableRaw, dataTableETL
        ) = row
        
        # sqlCommand = f"""INSERT INTO mgmtETL.Device(siteId, name, ieee, `deviceLogic`, `gatewayId`) VALUES ({siteId}, "{name}","{ieee}", {deviceLogic}, {gatewayId})"""
        # cursor_own.execute(sqlCommand)


        # if description:
        #     sqlCommand = f"""REPLACE INTO mgmtETL.Device(siteId, name, ieee, `deviceLogic`, `gatewayId`, description) VALUES ({siteId}, "{name}","{ieee}", {deviceLogic}, {gatewayId}, "{description}")"""
        #     cursor_own.execute(sqlCommand)

        # if deviceType:
        #     sqlCommand = f"""REPLACE INTO mgmtETL.Device(siteId, name, ieee, `deviceLogic`, `gatewayId`, deviceType) VALUES ({siteId}, "{name}","{ieee}", {deviceLogic}, {gatewayId},"{deviceType}")"""
        #     cursor_own.execute(sqlCommand)
        
        # if syncSec:
        #     sqlCommand = f"""REPLACE INTO mgmtETL.Device(siteId, name, ieee, `deviceLogic`, `gatewayId`, syncSec) VALUES ({siteId}, "{name}","{ieee}", {deviceLogic}, {gatewayId},{syncSec})"""
        #     cursor_own.execute(sqlCommand)
        
        # if remark:
        #     sqlCommand = f"""REPLACE INTO mgmtETL.Device(siteId, name, ieee, `deviceLogic`, `gatewayId`, remark) VALUES ({siteId}, "{name}","{ieee}", {deviceLogic}, {gatewayId},"{remark}")"""
        #     cursor_own.execute(sqlCommand)
        
        # if InsID:
        #     sqlCommand = f"""REPLACE INTO mgmtETL.Device(siteId, name, ieee, `deviceLogic`, `gatewayId`, InsID) VALUES ({siteId}, "{name}","{ieee}", {deviceLogic}, {gatewayId},"{InsID}")"""
        #     cursor_own.execute(sqlCommand)
        
        # if InsDT:
        #     sqlCommand = f"""REPLACE INTO mgmtETL.Device(siteId, name, ieee, `deviceLogic`, `gatewayId`, InsDT) VALUES ({siteId}, "{name}","{ieee}", {deviceLogic}, {gatewayId},"{InsDT}")"""
        #     cursor_own.execute(sqlCommand)

        # if UpdID:
        #     sqlCommand = f"""REPLACE INTO mgmtETL.Device(siteId, name, ieee, `deviceLogic`, `gatewayId`, UpdID) VALUES ({siteId}, "{name}","{ieee}", {deviceLogic}, {gatewayId},"{UpdID}")"""
        #     cursor_own.execute(sqlCommand)
    
        # if UpdDT:
        #     sqlCommand = f"""REPLACE INTO mgmtETL.Device(siteId, name, ieee, `deviceLogic`, `gatewayId`, UpdDT) VALUES ({siteId}, "{name}","{ieee}", {deviceLogic}, {gatewayId},"{UpdDT}")"""
        #     cursor_own.execute(sqlCommand)

        sqlCommand = f"""INSERT INTO mgmtETL.vDataETLInfo(siteId, siteName, name, nameDesc, ieee, gatewayId, typeDesc, logicDesc, dataTableRaw, dataTableETL) VALUES ({siteId}, '{siteName}', '{name}', '{nameDesc.replace("'", '"')}', '{ieee}', {gatewayId}, '{typeDesc}', '{logicDesc}', '{dataTableRaw}', '{dataTableETL}')"""
        logger.info(sqlCommand)
        cursor_own.execute(sqlCommand)

        logger.info(f"INSERT {row} Succeed")


conn_own.close()