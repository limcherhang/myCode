from flask import Flask
from flask import request # import request object
import json

app = Flask(
    __name__,
    static_folder = 'test_static',              # 資料夾名稱
    static_url_path = '/test_static'            # 網址路徑
)       # 建立 Application 物件

# 建立網站首頁的回應方式
@app.route("/")
def index():
    return "Hello Flask"

@app.route("/getSum")       # http://127.0.0.1:3000/getSum?max=21&min=20
def getSum():
    maxdata = request.args.get("max", 100)
    mindata = request.args.get("min", 0)
    
    result = 0
    for n in range(int(mindata), int(maxdata)+1):
        result += n

    return f"The sum result from {mindata} to {maxdata} is {result}"


# 啟動網站伺服器
app.run(host="0.0.0.0",port=3000,debug=True)