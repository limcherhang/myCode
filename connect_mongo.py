import configparser
from connection.mongo_connection import MongoConn
from bson import ObjectId

config = configparser.ConfigParser()
config.read('config.ini')

# 创建MongoConn实例
client = MongoConn(config['mongo_production_nxmap'])
client.connect()

# 获取数据库
db = client.get_database()

# 查询数据
users_info = db.users.find({})

for user in users_info:
    companyId = user['companyId']
    print(companyId, type(companyId))
    print()
    site_module = db.site_modules.find({
        "_id": ObjectId(companyId)
    })

    print(user)
    print()
    for site in site_module:
        print("site", site)
    
    break

client.close()