################################
#
#  Author: Henry
#  Code version: 0.1
#  Release date: 2019/11/26
#
################################
import pymysql
import requests
import datetime
import threading
import sys

url = 'https://notify-api.line.me/api/notify'
#  Evercomm Line notification service
groupToken = 'LDvENIXBrG3tUnoWTM5DzPZhD39xDzfwqMCrH34ywiP'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+groupToken}

#  Read content from text file into string
messages = open(sys.argv[1], 'r').read()

#  Print content to terminal for debug monitoring
print(messages)

#  Push content to LINE Notify service
if messages != '':
  r = requests.post(url, headers=headers , data = {'message':messages})
  