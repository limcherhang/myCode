import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import datetime

now = datetime.datetime.now().replace(microsecond=0)

start = now - datetime.timedelta(minutes=10)

# 設置 SMTP 伺服器和埠號
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# 設置寄件人和收件人
from_email = 'Aaron Alerts'
to_email = 'cherhanglim0227@gmail.com'

# 設置郵件主題和內容
subject = f'ALERTS SYSTEM {start}'
message = """
Dear receipient
 
This is the test alert message from Aaron
 
Best Regards,
Aaron Alerts System.
"""

# 設置郵件身份驗證
username = 'alin@evercomm.com.sg'
password = 'xhzygviprwmqdutz'

# 建立 SMTP 連接
smtp = smtplib.SMTP(smtp_server, smtp_port)
smtp.starttls()
smtp.login(username, password)

# 建立郵件
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = subject
msg['Header-Name'] = "test header name"
msg.attach(MIMEText(message, 'plain'))
print(msg)


# 發送郵件
smtp.sendmail(from_email, to_email, msg.as_string())

# 關閉 SMTP 連接
smtp.quit()