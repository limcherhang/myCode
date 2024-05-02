import requests

# 輸入您的 Line Notify 權杖
token = 'hfdyKwyOOe8lOhRTks3dAA7oLdFxzM4dzXZXlr6HwIA'

# 要發送的訊息
message = '這是一則測試訊息'

# Line Notify 的 API 網址
url = 'https://notify-api.line.me/api/notify'

# 設定標頭(header)，包括權杖和訊息
headers = {
    'Authorization': 'Bearer ' + token,
}

# 要傳送的資料
payload = {
    'message': message,
}

# 發送 POST 請求
response = requests.post(url, headers=headers, data=payload)

# 檢查回應
if response.status_code == 200:
    print('測試訊息已成功發送至 Line Notify!')
else:
    print('發送失敗，請檢查您的權杖或網路連線。')
