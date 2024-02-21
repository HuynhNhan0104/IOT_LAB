import paho.mqtt.client as mqttclient
import time
import json
import random

ADAFRUIT_IO_USERNAME = "NhanHuynh"
ADAFRUIT_IO_KEY = ""
BROKER_ADDRESS = "io.adafruit.com"
PORT = 1883

feeds_list = [
    "NhanHuynh/feeds/led",
    "NhanHuynh/feeds/temperature"
]

def on_subscribed(client, userdata, mid, granted_qos):
    print("subscribed successfully")
    pass

def on_messaged(client, userdata, message):
    topic = message.topic
    data = message.payload.decode("utf-8")
    try:
        # process message here
        print(f"received message on topic {topic}: {data}")
    except:
        pass
    
def on_connected(client, usedata, flags, rc):
    if rc == 0:
        for feed in feeds_list:
            client.subscribe(feed)
    else:
        print("Connection is failed")


client = mqttclient.Client("2013961")
client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

client.on_connect = on_connected
client.on_subscribe = on_subscribed
client.on_message = on_messaged
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

while True:
    try:
        temp = random.randrange(1,100)
        client.publish("NhanHuynh/feeds/temperature",temp, 1)
        time.sleep(20)
    except KeyboardInterrupt:
        break