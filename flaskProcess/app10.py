from flask import Flask
from flask import request # import request object
from flask import render_template
from flask import session
import json

app = Flask(
    __name__,
    static_folder = 'test_static',              # 資料夾名稱
    static_url_path = '/'            # 網址路徑
)       # 建立 Application 物件

app.secret_key = "any string but secret"    # 設定密鑰

# 建立網站首頁的回應方式
@app.route("/")
def index():
    return render_template("index5.html")

@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    session["username"] = name
    return f"你好，{name}"

@app.route("/talk")
def talk():
    name = session.get("username", "")
    return f"很高興認識你{name}"


# 啟動網站伺服器
app.run(host="0.0.0.0",port=3000,debug=True)