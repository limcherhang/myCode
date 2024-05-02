from flask import Flask

app = Flask(__name__)       # 建立 Application 物件

# 建立網站首頁的回應方式
@app.route("/")
def index():
    return "Hello Flask"    # 回傳網站首頁的內容

@app.route("/data")         # http://127.0.0.1:3000/data
def getData():
    return "Data Here"

@app.route("/hello/<name>") # http://127.0.0.1:3000/hello/aaron
def HelloUser(name):
    if name == 'aaron':
        return f"你好 {name}"
    else:
        return "Hello    " + name

# 啟動網站伺服器
app.run(host="0.0.0.0",port=3000,debug=True)