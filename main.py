import requests
import pytz
import mqtt
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup

tz = pytz.timezone('Asia/Bangkok')

refresh_time = [
    '00:00',
    '00:15',
    '00:30',
    '00:45',
    '01:00',
    '01:15',
    '01:30',
    '01:45',
    '02:00',
    '02:15',
    '02:30',
    '02:45',
    '03:00',
    '03:15',
    '03:30',
    '03:45',
    '04:00',
    '04:15',
    '04:30',
    '04:45',
    '05:00',
    '05:15',
    '05:30',
    '05:45',
    '06:00',
    '06:15',
    '06:30',
    '06:45',
    '07:00',
    '07:15',
    '07:30',
    '07:45',
    '08:00',
    '08:15',
    '08:30',
    '08:45',
    '09:00',
    '09:15',
    '09:30',
    '09:45',
    '10:00',
    '10:15',
    '10:30',
    '10:45',
    '11:00',
    '11:15',
    '11:30',
    '11:45',
    '12:00',
    '12:15',
    '12:30',
    '12:45',
    '13:00',
    '13:15',
    '13:30',
    '13:45',
    '14:00',
    '14:15',
    '14:30',
    '14:45',
    '15:00',
    '15:15',
    '15:30',
    '15:45',
    '16:00',
    '16:15',
    '16:30',
    '16:45',
    '17:00',
    '17:15',
    '17:30',
    '17:45',
    '18:00',
    '18:15',
    '18:30',
    '18:45',
    '19:00',
    '19:15',
    '19:30',
    '19:45',
    '20:00',
    '20:15',
    '20:30',
    '20:45',
    '21:00',
    '21:15',
    '21:30',
    '21:45',
    '22:00',
    '22:15',
    '22:30',
    '22:45',
    '23:00',
    '23:15',
    '23:30',
    '23:45',
    '24:00']
    
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

