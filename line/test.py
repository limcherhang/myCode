import sys
import time
import requests

class StdoutRedirector:
    def __init__(self):
        self.original_stdout = sys.stdout
        sys.stdout = self

    def write(self, text):
        # 解析輸出，這裡可以根據實際情況進行解析
        # if "Hi" in text:
        #     self.send_line_message("Hi is printed!")
        self.send_line_message(text)
        # 將輸出還原到原始的標準輸出
        self.original_stdout.write(text)

    def send_line_message(self, message):
        groupToken = 'hfdyKwyOOe8lOhRTks3dAA7oLdFxzM4dzXZXlr6HwIA'
        # 使用Line的API發送消息，需要替換為實際的Line API相關信息
        line_api_url = 'https://notify-api.line.me/api/notify'
        headers = {
            'Authorization': 'Bearer ' + groupToken,
        }
        payload = {
            'message': message,
        }

        # 發送Line消息
        response = requests.post(line_api_url, headers=headers, data=payload)

# 初始化重定向器
stdout_redirector = StdoutRedirector()

while True:
    # 獲取當前時間
    current_time = time.localtime(time.time())
    
    print("Hi")  # 這條消息會觸發發送Line消息的動作
    
    # 等待一段時間，以免無限迴圈造成過度的 CPU 使用
    time.sleep(60)  # 暫停 60 秒