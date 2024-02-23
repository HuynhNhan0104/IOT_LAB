from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import time
import threading
#import my module
from AI_model import AI_model
from mqtt import MQTT_Module
from uart import Serial_module

AIO_FEED_ID  = [
    "NhanHuynh/feeds/led", 	
    "NhanHuynh/feeds/temperature" ,
    "NhanHuynh/feeds/mask"
]
AIO_USERNAME    = "NhanHuynh"
AIO_KEY         = "aio_cjdw41TQxexd6tdbOQ2mW7bYdc3r"
BROKER_ADDRESS  = "io.adafruit.com"
PORT            = 1883

# URL             = "http://192.168.9.67:8080/video"
# URL             = "http://192.168.137.4:8080/video"



result_in_Vietnamese = {
    "mask"      : "Deo khau trang",
    "noneMask"  : "Ko deo khau trang",
    "noneHuman" : "Ko co nguoi"
}

def processData_external(data,mqtt_handler):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    mqtt_handler.publish("NhanHuynh/feeds/temp",splitData[1])
    

def main():
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)
    my_serial = Serial_module("COM3",115200)
    my_serial.set_processData(processData_external)
    #     my_serial.set_processData(processData_external)
    my_ai = AI_model("model/keras_model.h5","model/labels.txt",0)
    mqtt_handler = MQTT_Module(AIO_USERNAME, AIO_KEY, AIO_FEED_ID, BROKER_ADDRESS, PORT)
    #create a counter
    count_ai = 0
    while True:
        my_serial.readSerial(mqtt_handler)
        if count_ai > 5:
            count_ai = 0
            result, _ = my_ai.image_detector()
            # mqtt_handler.publish("NhanHuynh/feeds/mask",result_in_Vietnamese[result])
        else: 
            count_ai += 1
        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)
        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break
        # time.sleep(1)

    my_ai.camera.release_camera()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
    # cam = cv2.VideoCapture(URL)
    # count = 0
    # while True:
    #     time_current = time.time()
    #     if count > 5:
    #         count = 0
    #         # Lấy số lượng frame trong stream
    #         # Đặt vị trí frame hiện tại thành giá trị cuối cùng
    #         # cam.set(cv2.CAP_PROP_POS_FRAMES, frame_count - 1)
    #         ret, image = cam.read()
    #         cv2.imshow("my cam",image)
    #     else: 
    #         count+=1
    #     keyboard_input = cv2.waitKey(1)
    #     # 27 is the ASCII for the esc key on your keyboard.
    #     if keyboard_input == 27:
    #         break
    #     time.sleep(1)


