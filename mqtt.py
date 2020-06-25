import paho.mqtt.client as mqttClient
import time

# PAYLOAD : mosquitto_pub -h 150.95.27.220 -u air4thai -P  asd1357 -m 25 -t air4thai/lamphun01  -p 1883
# $ mosquitto_sub -h 150.95.27.220 -u air4thai -P  asd1357 -t air4thai/lamphun01
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected    # Use global variable
        Connected = True    # Signal connection 
 
    else:
 
        print("Connection failed")

Connected = False   # global variable for the state of the connection
 
broker_address= "150.95.27.220"  #Broker address
port = 1883                         #Broker port
user = "air4thai"                    #Connection username
password = "asd1357"            #Connection password
topic = "air4thai/lamphun01"
client = mqttClient.Client("dxdxydy")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop

while Connected != True:    #Wait for connection
    time.sleep(0.1)

def publish(data):
    client.publish(topic,data)
    print("send MQTT")

    
