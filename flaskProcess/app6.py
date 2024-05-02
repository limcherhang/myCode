from flask import Flask
from flask import request # import request object
from flask import redirect  # import redirect function
import json

app = Flask(
    __name__,
    static_folder = 'test_static',              # 資料夾名稱
    static_url_path = '/test_static'            # 網址路徑
)       # 建立 Application 物件

# 建立網站首頁的回應方式
@app.route("/")
def index():
    lang = request.headers.get("accept-language")
    if lang.startswith("en"):
        return redirect("/en/")
        # return json.dumps({
        #     "text": "Hello World",
        #     "status": "ok"
        # })
    else:
        return redirect("/zh/")
        # return json.dumps({
        #     "text": "您好，歡迎光臨",
        #     "status": "ok"
        # }, ensure_ascii=False)      # 指示不要用ascii編碼處理中文，而是顯示中文文字，默認為True

@app.route('/en/')
def redirectToEn():
    return "Hello flask"

@app.route('/zh/')
def redirectToZh():
    return "您好，歡迎光臨"

# 啟動網站伺服器
app.run(host="0.0.0.0",port=3000,debug=True)