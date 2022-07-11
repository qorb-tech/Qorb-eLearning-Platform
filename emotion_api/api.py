import csv
import json
import numpy as np
from charts import Charts
from emotion import predict
from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sign import detectHand

# Sign results
currentFrames = []
currentResult = 'Nothing'


# BaseModel for the request body
class Item(BaseModel):
    frame : list = []
    time : int
    meeting_name:str

# BaseModel for the request body
class SignItem(BaseModel):
    frame: list = []

# CREATE API
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
    
    image = np.array(item.frame)
    time = item.time
    meeting_name = item.meeting_name

    # model prediction
    background_tasks.add_task(predict, image, time, meeting_name)

    data = {
        'Wasl Ya Ba4a': image.shape       
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

# post request for image
@app.post("/postframe/")
async def post_frame(item: Item, background_tasks: BackgroundTasks):
    """
    Post frame to API.
    item: frame
    returns: prediction
    """

    # Get the image from the request
    frame = item.frame

    # Convert the image to a numpy array
    frame = np.array(frame, dtype=np.uint8).reshape(128, 128, 4)[:,:,:3]

    # Send the image to the background task
    background_tasks.add_task(detectHand, frame)

    # Return the result
    return json.dumps({"result": len(currentFrames)})
