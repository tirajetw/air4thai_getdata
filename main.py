import requests
import pytz
import mqtt
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup

tz = pytz.timezone('Asia/Bangkok')
refresh_time = ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00","24:00"]
def get_data():
    url = "http://air4thai.pcd.go.th/webV2/station.php?station=68t"
    data = requests.get(url)
    data.encoding = "utf-8"
    # print(data.content)
    soup = BeautifulSoup(data.text,'lxml')
    # print(soup.prettify())
    x = soup.find_all("td") # <- ค่าที่ใช้ในการค้นหา

    data_payload = []

    for i in range(49,58):
        temp = str(x[i])[19:]
        temp = temp[:-5]
        data_payload.append(temp)

    data_payload[8] = data_payload[8][40:]
    data_payload[8] = data_payload[8][:-8]

    payload = ('{' + 
        '\"{}\":\"{}\", '.format('date',data_payload[0]) + 
        '\"{}\":\"{}\", '.format('pm2.5',data_payload[1]) +
        '\"{}\":\"{}\", '.format('pm10',data_payload[2]) +
        '\"{}\":\"{}\", '.format('O3',data_payload[3]) +
        '\"{}\":\"{}\", '.format('CO',data_payload[4]) +
        '\"{}\":\"{}\", '.format('NO2',data_payload[5]) +
        '\"{}\":\"{}\", '.format('SO2',data_payload[6]) +
        '\"{}\":\"{}\", '.format('AQI',data_payload[7]) +
        '\"{}\":\"{}\"'.format('quality',data_payload[8]) +
        '}')
    print(payload)
    mqtt.publish(payload)
    
while True:
    try:
        now = datetime.now(tz)
        dt_string = now.strftime("%H:%M")

        for i in refresh_time:
            if i == dt_string:
                get_data()
                time.sleep(60)
        
        else:
            print(dt_string)
            time.sleep(30)
            pass

    except Exception as e:
        print(str(e))

