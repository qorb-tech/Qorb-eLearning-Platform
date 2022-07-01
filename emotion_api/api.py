import json
import csv
import cv2 as cv
import numpy as np
#import tensorflow as tf
from charts import Charts
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# Load model
#model = tf.keras.models.load_model('model.h5')    

# Classes
classes = {
    0:'Angry',
    1:'Fear',
    2:'Happy',
    3:'neutral',
    4:'Sad',
    5:'Surprise'
}

class Item(BaseModel):
    frame : list = []
    time : int
    meeting_name:str

#def predict(image, time, meeting_name):
    # preprocess
#    image = image.astype(np.uint8)
#    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
#    image = cv.resize(image, (48,48)).reshape(1,48,48)
    
    # Predict
#    pred = model.predict(image)
#    pred = np.argmax(pred, axis = 1)
#    status = classes[pred[0]]
    
    # Save prediction
  ##  path = 'data/' + meeting_name + '/.csv'
  #  row = [status, time]

 #   with open(path, 'a', newline='') as f:
    #    writer = csv.writer(f)
   #     writer.writerow(row)
app = FastAPI()
origins = [
    "*" , 
"https://qorb.tech/",
"http://localhost",
"https://www.qorb.tech/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)    



@app.post('/sendphoto/')
async def post_image(item: Item, background_tasks:BackgroundTasks):
    
    image = np.array(item.frame)
    time = item.time
    meeting_name = item.meeting_name

    # model prediction
    #background_tasks.add_task(predict, image, time, meeting_name)

    data = {
        'Negm': image.shape       
    }
    # return
    return json.dumps(data)

@app.get('/states/')
async def get_states(data_path: str):
    chart = Charts(data_path)
    return chart.getStates()

@app.get('/bar/')
async def bar(data_path: str):
    chart = Charts(data_path)
    return chart.CustomizedBar()
