import pandas as pd
import configparser
from connection.mysql_connection import MySQLConn
import numpy as np

df = pd.read_excel('Park_Royal_Collection_on_Pickering_Road_Data_Mapping.xlsx', sheet_name='Device Mapping(dataETL)')
# df.columns = df[0]
# print(df.iloc[0, :])
columns = []
for d in df.iloc[0, :]:
    if '/' in d:
        columns.append(d.replace('/', '_'))
    elif ' ' in d:
        columns.append(d.replace(' ', '_'))
    else:
        columns.append(d)

df.columns = columns
df = df[1:]
df = df.replace({np.nan: None})
# print(df)

config = configparser.ConfigParser()
config.read('config.ini')

conn = MySQLConn(config['mysql_own'])

with conn.cursor() as cursor:
    for row in df.itertuples(index=False):
        S_N = row.S_N
        Description = row.Description
        # Device_Type = row.Device_Type
        Data_Type = row.Data_Type
        Sensor_Type = row.Sensor_Type
        Sensor_ID = row.Sensor_ID
        Device_ID = row.Device_ID
        Name = row.Name
        Gateway_ID = row.Gateway_ID
        remark = row.remark

        # print(S_N, Description, Data_Type, Sensor_Type, Sensor_ID, Device_ID, Name, Gateway_ID, remark)
        if remark is None:
            sqlCommand = f"INSERT INTO mgmtETL.DataETL(siteId, name, description, deviceId, deviceType, deviceLogic, gatewayId) VALUES (8, '{Name}', '{Description}', '{Device_ID}', '{Sensor_Type}', {Sensor_ID}, {Gateway_ID})"
        else:
            sqlCommand = f"INSERT INTO mgmtETL.DataETL(siteId, name, description, deviceId, deviceType, deviceLogic, gatewayId, remark) VALUES (8, '{Name}', '{Description}', '{Device_ID}', '{Sensor_Type}', {Sensor_ID}, {Gateway_ID}, {remark})"
        print(sqlCommand)
        # print(sqlCommand)
        cursor.execute(sqlCommand)

conn.close()