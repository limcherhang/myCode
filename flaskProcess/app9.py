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
    return render_template("index4.html")

@app.route("/show")
def show():
    name = request.args.get("n")

    return f"{name} 你好，歡迎光臨"

@app.route("/count", methods=['POST'])
def count():
    num = int(request.form['num'])
    ans = 0
    for i in range(1, num+1):
        ans += i
    
    return render_template("result4.html", Sum=str(ans))

# 啟動網站伺服器
app.run(host="0.0.0.0",port=3000,debug=True)