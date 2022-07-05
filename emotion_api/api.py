import json
import csv
import cv2 as cv
import numpy as np
import tensorflow as tf
from charts import Charts
from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import os

# Load the model 
model = tf.keras.models.load_model('final_xception.h5')    

# Define the classes
classes = {
    0:'Angry',
    1:'Fear',
    2:'Happy',
    3:'neutral',
    4:'Sad',
    5:'Surprise'
}

# BaseModel for the request body
class Item(BaseModel):
    frame : list = []
    time : int
    meeting_name:str

# Predict the emotion of the frame 
def predict(image, time, meeting_name):
    """
    Predict the emotion of the image and save the data in a csv file
    image: numpy array
    time: int
    meeting_name: str
    """

    # preprocess
    print("HHHHHHH")
    image = image.astype(np.uint8)
    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    image = cv.resize(image, (48,48)).reshape(1,48,48)
    
    # Predict
    pred = model.predict(image)
    pred = np.argmax(pred, axis = 1)
    status = classes[pred[0]]
    
    # Save prediction
    if not os.path.exists('/root/project/qorb_project/emotion_api/data/' + meeting_name + '.csv'):
        f = open('/root/project/qorb_project/emotion_api/data/' + meeting_name + '.csv', 'w')
        writer = csv.writer(f)
        writer.writerow(['prediction', 'time'])

    path = '/root/project/qorb_project/emotion_api/data/' + meeting_name + '.csv'
    row = [status, time]
    
    
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)


# API for the emotion detection 
app = FastAPI()

# CORS middleware for allowing cross-origin requests from other domains
origins = ['*']

# Add the CORS middleware to the API 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Post request with the frame and the time of the frame
@app.post('/sendphoto/')
async def post_image(item: Item, background_tasks:BackgroundTasks):
    image = np.array(item.frame).reshape(48, 48, 4)[:,:,:3]
    time = item.time
    meeting_name = item.meeting_name

    # model prediction
    background_tasks.add_task(predict, image, time, meeting_name)

    data = {
        'Wasl Ya Ba4a': len(item.frame)        
    }
    # return
    return json.dumps(data)

@app.get('/status/')
async def get_status(data_path: str):
    chart = Charts(data_path)
    return chart.getStates()

@app.get('/bar/')
async def bar(data_path: str):
    chart = Charts(data_path)
    return chart.CustomizedBar()
