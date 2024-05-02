from flask import Flask

app = Flask(
    __name__,
    static_folder = 'test_static',              # 資料夾名稱
    static_url_path = '/test_static'            # 網址路徑
)       # 建立 Application 物件

# 建立網站首頁的回應方式
@app.route("/")
def index():
    return "Hello Flask"    # 回傳網站首頁的內容

# 啟動網站伺服器
app.run(host="0.0.0.0",port=3000,debug=True)