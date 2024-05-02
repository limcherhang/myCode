import requests
from bs4 import BeautifulSoup

# 要爬取的網頁 URL
url = "https://data.moenv.gov.tw/dataset/detail/CFP_P_02"

# 使用 requests 库获取网页内容
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 在这里可以使用 BeautifulSoup 提供的方法来提取数据
    # 例如，获取页面标题
    title = soup.title.text
    print(f"網頁標題：{title}")
    
    # 获取页面的所有文本
    all_text = soup.get_text()
    print(all_text)
else:
    print(f"無法獲取網頁內容，錯誤代碼：{response.status_code}")