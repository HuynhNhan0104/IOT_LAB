from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np

class AI_model:
    def __init__(self,model_file,label_file):
        self.model_file = model_file
        self.label_file = label_file
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
        class_name = self.class_names[index]
       
        confidence_score = prediction[0][index]
        
        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        return class_name, confidence_score