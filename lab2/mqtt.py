import sys
# from Adafruit_IO import MQTTClient


import paho.mqtt.client as mqttclient
import time
import random



class MQTT_Module:
    feed_ids = []
    username = None
    access_token = None
    broker_address = "io.adafruit.com"
    port = 1883
    recieveCallback = None
    client = None
    
    def setRecieveCallback(self, func):
        self.recieveCallback = func

    def connected(self, client,usedata, flags, rc):
        print("Connected ...")
        for feed in self.feed_ids :
            client.subscribe(feed)

    def subscribe(self, client, userdata, mid, granted_qos):
        print("subscribed successfully")

    def disconnected(self, client):
        print("Disconnected...")
        sys.exit (1)

    def message(self, client, userdata, message):
        topic = message.topic
        data = message.payload.decode("utf-8")
        try:
            # process message here
            print(f"received message on topic {topic}: {data}")
        except:
            pass

    def __init__(self,  username = None,  access_token = None, feed_ids  = None , broker_address = None, port = 1883):
        self.feed_ids  = None  if ( feed_ids is None  ) else feed_ids 
        self.username =  None  if (username is None  ) else username
        self.access_token =  None  if (access_token is None  ) else access_token
        self.broker_address =  None  if (broker_address is None  ) else broker_address
        self.port =  None  if (port is None  ) else 1883
        
        self.client = mqttclient.Client("hello iot")
        self.client.username_pw_set(username, access_token)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect(broker_address,port)
        self.client.loop_start()

    def add_feed(self,feed_name):
        self.feed_ids.append(feed_name)
        self.client.subscribe(feed_name)
        
    def publish(self,feed_name,message):
        self.client.publish(feed_name,message,1)
         
    def set_username(self,username):
        self.username= username
        
    def set_access_token(self, token):
        self.access_token = token
        
    def set_feed_list(self,feed_list):
        self.feed_list = feed_list 
        
    def check_client_is_created(self):
        return self.client != None
        


# TEST in here


AIO_FEED_IDs  = ["NhanHuynh/feeds/led", 	"NhanHuynh/feeds/temperature"]
AIO_USERNAME = "NhanHuynh"
AIO_KEY= "aio_cjdw41TQxexd6tdbOQ2mW7bYdc3r"
BROKER_ADDRESS = "io.adafruit.com"
PORT = 1883
def main():
    test = MQTT_Module(username= AIO_USERNAME,access_token= AIO_KEY, feed_ids= AIO_FEED_IDs,broker_address=BROKER_ADDRESS,port=PORT)
    while True:
        try:
            temp = 51
            print("hello")
            # print(f"temp : {temp}")
            test.publish("NhanHuynh/feeds/temperature",temp)
            # print("end")
            time.sleep(10)
        except KeyboardInterrupt:
            break
if __name__ == "__main__":
    main()