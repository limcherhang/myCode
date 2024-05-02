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
    sqlCommand = "SELECT * FROM iotmgmt.zigbeeRawModbus;"
    cursor_42.execute(sqlCommand)
    result = cursor_42.fetchall()

conn_42.close()
conn_own = MySQLConn(config["mysql_own"])

with conn_own.cursor() as cursor_own:
    cursor_own.execute("SET SQL_SAFE_UPDATES = 0;")
    cursor_own.execute("DELETE FROM iotmgmt.zigbeeRawModbus;")
    cursor_own.execute("SET SQL_SAFE_UPDATES = 1;")
    for row in result:
        (
            ts, gatewayId, linkQuality, ieee, receivedSync, modbusCmd, responseData
        ) = row
        
        logger.info(row)

        if linkQuality and receivedSync:
            sqlCommand = f"INSERT INTO iotmgmt.zigbeeRawModbus(ts, gatewayId, linkQuality, ieee, receivedSync, modbusCmd, responseData) VALUES ('{ts}', {gatewayId}, {linkQuality}, '{ieee}', '{receivedSync}', '{modbusCmd}', '{responseData}')"
            cursor_own.execute(sqlCommand)
        elif linkQuality:
            sqlCommand = f"INSERT INTO iotmgmt.zigbeeRawModbus(ts, gatewayId, linkQuality, ieee, modbusCmd, responseData) VALUES ('{ts}', {gatewayId}, {linkQuality}, '{ieee}', '{modbusCmd}', '{responseData}')"
            cursor_own.execute(sqlCommand)
        elif receivedSync:
            sqlCommand = f"INSERT INTO iotmgmt.zigbeeRawModbus(ts, gatewayId, ieee, receivedSync, modbusCmd, responseData) VALUES ('{ts}', {gatewayId}, '{ieee}', '{receivedSync}', '{modbusCmd}', '{responseData}')"
            cursor_own.execute(sqlCommand)

        logger.info(f"INSERT {row} Succeed")

conn_own.close()