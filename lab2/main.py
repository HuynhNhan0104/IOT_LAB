from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
from AI_model import AI_model
import requests
import imutils 

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
my_ai = AI_model("model/keras_model.h5","model/labels.txt")
# CAMERA can be 0 or 1 based on default camera of your computer


url_using_cv2 = "http://192.168.137.4:8080/video"

url_using_imutils= "http://192.168.137.4:8080/shot.jpg"


def get_image_from_camera_of_PC(camera):
    return camera.read()

def get_camera(source):
    return cv2.VideoCapture(source)


# runing faster
def get_image_from_android_using_ip_webcam(url):
    #using android camera through app ip webcam
    image_resp = requests.get(url) 
    image_arr = np.array(bytearray(image_resp.content), dtype=np.uint8) 
    image = cv2.imdecode(image_arr, -1)
    image = imutils.resize(image, width=640, height=480) 
    # image = cv2.resize(image,(600,480),interpolation=cv2.INTER_AREA)
    return True, image





camera = get_camera(url_using_cv2)
while True:
    # Grab the webcamera's image.
    ret, image = get_image_from_android_using_ip_webcam(url_using_imutils)
    
    cv2.imshow("my camera",image)
    my_ai.predict(image)
    
    
    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()


