import requests
import pytz
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup

tz = pytz.timezone('Asia/Bangkok')
refresh_time = "00:05"

url = "http://air4thai.pcd.go.th/webV2/station.php?station=68t"
data = requests.get(url)
data.encoding = "utf-8"
# print(data.content)
soup = BeautifulSoup(data.text,'lxml')
# print(soup.prettify())
x = soup.find_all("td") # <- ค่าที่ใช้ในการค้นหา

for i in range(49,58):
    print(x[i])