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
    # print("請求方法", request.method)
    # print("通訊協定", request.scheme)
    # print("主機名稱", request.host)
    # print("完整的網址", request.url)
    # print("瀏覽器和作業系統", request.headers.get("user-agent"))
    # print("語言偏好", request.headers.get("accept-language"))
    # print("引薦網址", request.headers.get("referrer"))

    # return json.dumps({"請求方法": request.method, "通訊協定": request.scheme}, ensure_ascii=False)    # 回傳網站首頁的內容
    lang = request.headers.get("accept-language")
    if lang.startswith("en"):
        return "Hello Flask"
    else:
        return "你好，歡迎光臨"




# 啟動網站伺服器
app.run(host="0.0.0.0",port=3000,debug=True)