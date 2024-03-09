from mqtt import MQTT_Module
from uart import Serial_module
import time
    
AIO_FEED_IDs  = [
    "NhanHuynh/feeds/led", 	
    "NhanHuynh/feeds/temp",
    "NhanHuynh/feeds/mask",
    "NhanHuynh/feeds/humi",
    "NhanHuynh/feeds/button",
    "NhanHuynh/feeds/fan"
]

AIO_USERNAME = "NhanHuynh"
AIO_KEY= ""
BROKER_ADDRESS = "io.adafruit.com"
PORT = 1883    

def send_command_to_node(serial,topic,data):
    if topic == "NhanHuynh/feeds/led":
        message = f"!LED:{data}#"
        serial.writeData(message)
        
    elif topic == "NhanHuynh/feeds/button":
        message = f"!BUTTON:{data}#"
        serial.writeData(message)
        
    elif topic == "NhanHuynh/feeds/fan":
        message = f"!FAN:{data}#"
        serial.writeData(message)
        
        
    
def main():
    serial_handler = Serial_module("COM3",115200)
    mqtt_handler = MQTT_Module(username= AIO_USERNAME,access_token= AIO_KEY, feed_ids= AIO_FEED_IDs,broker_address=BROKER_ADDRESS,port=PORT)
    mqtt_handler.set_serial(serial_handler)
    mqtt_handler.set_on_message_callback(send_command_to_node)
    while True:
        try:
            serial_handler.readSerial(mqtt_handler)
            time.sleep(1)
        except KeyboardInterrupt:
            break 
if __name__ == "__main__":
    main()