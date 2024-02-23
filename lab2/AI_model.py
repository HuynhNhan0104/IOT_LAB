from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import queue
import threading

class Camera:
    def __init__(self,source):
        self.camera = self.get_camera(source)
        # self.frame_buffer = queue.Queue()
        self.stream_thread = threading.Thread(target=self.run)
        self.stream_thread.daemon = True
        self.stream_thread.start()
        self.last_frame = None
        
    def get_last_image(self):
        #return bool, img
        return self.last_frame

    def get_camera(self,source):
        return cv2.VideoCapture(source)
    
    def release_camera(self):
        self.camera.release()
        
    def run(self):
        while True:
            ret, self.last_frame = self.camera.read()
            if not ret:
                break
        # self.frame_buffer.put(self.last_frame)
        
        
        
class AI_model:
    def __init__(self,model_file,label_file,source = 0):
        self.model_file = model_file
        self.label_file = label_file
        self.camera = Camera(source)
        # Load the model
        self.model = load_model(model_file, compile=False)
        # Load the labels
        self.class_names = open(label_file, "r").readlines()
    
    def predict(self,image):
        # Resize the raw image into (224-height,224-width) pixels
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)        
         # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        
        # Normalize the image array
        image = (image / 127.5) - 1
        
        # Predicts the model
        prediction = self.model.predict(image)
        index = np.argmax(prediction)
        
        # Print prediction and confidence score
        class_name = self.class_names[index].strip("\n")
        confidence_score = prediction[0][index]
        
        print("Class:", class_name[2:], end=",")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        return class_name[2:], confidence_score
    
    
    def image_detector(self):
    # Grab the webcamera's image.
        image = self.camera.get_last_image()
        cv2.imshow("my camera",image)
        return self.predict(image)