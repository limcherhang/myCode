import os
import sys
rootPath = os.getcwd() + '/../../'
sys.path.append(rootPath)
from connection.mysql_connection import MySQLConn
import configparser
import threading
import sched

from flask import Flask, render_template, request, session

app = Flask(__name__)

app.secret_key = 'aaron'

# 全局变量，用于存储数据库连接对象
# conn = None

# def reconnect_db():
#     global conn
    # 创建新的数据库连接
    # config = configparser.ConfigParser()
    # config.read(rootPath+'/config.ini')
    # new_conn = MySQLConn(config['mysql_azureV2'])

    # # 更新全局变量中的数据库连接对象
    # conn = new_conn

    # # 定时任务，每十分钟重新连接一次数据库
    # threading.Timer(600, reconnect_db).start()

# def start_reconnect_task():
#     # 在应用启动时启动定时任务
#     reconnect_db()

# 在应用启动时调用定时任务函数
# start_reconnect_task()

config = configparser.ConfigParser()
config.read(rootPath+'/config.ini')
new_conn = MySQLConn(config['mysql_azureV2'])

# 更新全局变量中的数据库连接对象
conn = new_conn

@app.route('/')
def index():
    with conn.cursor() as cursor:
        schemas = get_schemas(cursor)
        tables = get_tables(cursor)
        return render_template('index.html', schemas=schemas, tables=tables, query_result=None, column_titles=None, historys=None)

@app.route('/query', methods=['POST'])
def query():
    if request.method == 'POST':
        sql_query = request.form['sql_query']
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql_query)
                Count = cursor.rowcount
                query_result = cursor.fetchall()
                column_titles = [i[0] for i in cursor.description]
                schemas = get_schemas(cursor)
                tables = get_tables(cursor)
                # 获取会话中的历史记录，如果不存在则初始化为空列表
                historys = session.get('historys', [])
                # 将当前查询添加到历史记录中
                historys.append(sql_query)
                # 更新会话中的历史记录
                session['historys'] = historys
                # 手动保存会话
                session.modified = True
                return render_template('index.html', schemas=schemas, tables=tables, query_result=query_result, column_titles=column_titles, historys=historys, Count=Count)
            except Exception as e:
                error_message = str(e)
                return render_template('index.html', query_result=error_message)

def get_schemas(cursor):
    cursor.execute("SHOW DATABASES;")
    return [schema[0] for schema in cursor.fetchall()]

def get_tables(cursor):
    cursor.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('mysql', 'information_schema', 'performance_schema','sys');")
    tables = {}
    for table_schema, table_name in cursor.fetchall():
        if table_schema not in tables:
            tables[table_schema] = []
        tables[table_schema].append(table_name)
    return tables

if __name__ == '__main__':

    app.run(debug=True)