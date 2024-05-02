from connection.mysql_connection import MySQLConn
from utils.util import get_logger
import os

import configparser
import pandas as pd

file = __file__
basename = os.path.basename(file)
logFile = os.path.splitext(basename)[0]+'.log'

logger = get_logger('./log/', logFile)

config = configparser.ConfigParser()
config.read("config.ini")

conn_azure = MySQLConn(config["mysql_fn_azure"])

with conn_azure.cursor() as cursor:
    sqlCommand = f"""
        SHOW COLUMNS FROM dataPlatform.flow;
    """
    columns = []
    cursor.execute(sqlCommand)
    for res in cursor.fetchall():
        columns.append(res[0])
    
    sqlCommand = f"""
        SELECT DISTINCT(CAST(SUBSTRING_INDEX(name, '#', -1) AS UNSIGNED)) AS extracted_number
        FROM dataPlatform.flow
        ORDER BY extracted_number;
    """

    cursor.execute(sqlCommand)
    result = {}
    for (res, ) in cursor.fetchall():
        name = f'flow#{res}'
        result[name] = []
        sqlCommand = f"""
            SELECT * FROM dataPlatform2023.flow_10 WHERE name='{name}'
            UNION
            SELECT * FROM dataPlatform.flow WHERE name='{name}';
        """
        cursor.execute(sqlCommand)
        for info in cursor.fetchall():
            result[name].append(info)

    with pd.ExcelWriter('flow.xlsx', engine='xlsxwriter') as writer:
        for name, value in result.items():
            df = pd.DataFrame(value, columns=columns)
            df.to_excel(writer,sheet_name=name, index=False)

            worksheet = writer.sheets[name]

            for idx, col in enumerate(df):
                series = df[col]
                max_len = max(
                    series.astype(str).map(len).max(),
                    len(str(series.name))
                )+5
                worksheet.set_column(idx,idx,max_len)
        