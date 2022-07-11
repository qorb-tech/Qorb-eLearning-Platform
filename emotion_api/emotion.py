import json
import csv
import cv2 as cv
import numpy as np
import tensorflow as tf

# Load the model 
model = tf.keras.models.load_model('model.h5')

# Define the classes
classes = {
    0:'Angry',
    1:'Fear',
    2:'Happy',
    3:'neutral',
    4:'Sad',
    5:'Surprise'
}

# Predict the emotion of the frame 
def predict(image, time, meeting_name):
    """
    Predict the emotion of the image and save the data in a csv file
    image: numpy array
    time: int
    meeting_name: str
    """

    # preprocess
    image = image.astype(np.uint8)
    image = np.array(image)
    image = image[:,:,:3]
    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    image = cv.resize(image, (48,48)).reshape(1,48,48)
    
    # Predict
    pred = model.predict(image)
    pred = np.argmax(pred, axis = 1)
    status = classes[pred[0]]
    
    # Save prediction
    path = 'data/' + meeting_name + '.csv'
    row = [status, time]

    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)
