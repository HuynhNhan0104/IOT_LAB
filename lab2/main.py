# from keras.models import load_model  # TensorFlow is required for Keras to work
# import cv2  # Install opencv-python
import numpy as np
import time
import threading
#import my module
# from AI_model import AI_model, Camera
from mqtt import MQTT_Module
from uart import Serial_module

AIO_FEED_ID  = [
    "NhanHuynh/feeds/led", 	
    "NhanHuynh/feeds/temp" ,
    "NhanHuynh/feeds/mask",
    "NhanHuynh/feeds/humi"
]
AIO_USERNAME    = "NhanHuynh"
AIO_KEY         = "aio_zsWp90MrYtJoK2UOoiFU6XJ2csDK"
BROKER_ADDRESS  = "io.adafruit.com"
PORT            = 1883
URL             = "http://192.168.137.191:8080/video"



result_in_Vietnamese = {
    "mask"      : "Deo khau trang",
    "noneMask"  : "Ko deo khau trang",
    "noneHuman" : "Ko co nguoi"
}

def processData_external_define(data,mqtt_handler):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[0] == "TEMP":
        mqtt_handler.publish("NhanHuynh/feeds/temp",splitData[1])
    elif splitData[0] == "LED":
        mqtt_handler.publish("NhanHuynh/feeds/led",splitData[1])
    elif splitData[0] == "HUMI":
        mqtt_handler.publish("NhanHuynh/feeds/humi",splitData[1])
    else:
        print("we dont have that measurement to publish")
    

def main():
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)
    # serial init
    my_serial = Serial_module("COM3",115200)
    my_serial.set_processData(processData_external_define)
    
    #AI model init
    # my_ai = AI_model("model/keras_model.h5","model/labels.txt",0)
    
    #mqtt init
    mqtt_handler = MQTT_Module(AIO_USERNAME, AIO_KEY, AIO_FEED_ID, BROKER_ADDRESS, PORT)
    #create a counter
    # count_ai = 0
    while True:
        #serial read
        my_serial.readSerial(mqtt_handler)
    
        if count_ai > 5:
            count_ai = 0
            result, _ = my_ai.image_detector()
            mqtt_handler.publish("NhanHuynh/feeds/mask",result_in_Vietnamese[result])
        else: 
            count_ai += 1
        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)
        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break
        time.sleep(1)

    my_ai.camera.release_camera()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()



