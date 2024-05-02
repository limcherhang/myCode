from flask import Flask
from flask import request # import request object
from flask import render_template 
import json

app = Flask(
    __name__,
    static_folder = 'test_static',              # 資料夾名稱
    static_url_path = '/'            # 網址路徑
)       # 建立 Application 物件

# 建立網站首頁的回應方式
@app.route("/")
def index():
    return render_template("index2.html")

@app.route("/page")
def page():
    return render_template("index3.html")

# 啟動網站伺服器
app.run(host="0.0.0.0",port=3000,debug=True)