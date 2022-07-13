# importing libraries
import csv
import json
import cv2 as cv
import numpy as np
import mediapipe as mp
import tensorflow as tf
from charts import Charts
from pydantic import BaseModel
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware



# Loading Models
sign_model = None
emotion_model = tf.keras.models.load_model('model.h5')



# Sign results (sign)
currentFrames = []
currentResult = 'Nothing'



# Create background subtraction (sign)
BACKSUB = cv.createBackgroundSubtractorMOG2()
WHITE_FRAME = np.ones((800, 800)) * 255



# To Detect Hands (sign)
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)


# Define Classes (emotion)
classes = {
    0:'Angry',
    1:'Fear',
    2:'Happy',
    3:'neutral',
    4:'Sad',
    5:'Surprise'
}


# Define Labels (Sign)
LABELS = ['plus', 'equal', 'day', 'important', 'explicate', 'break', 'need', 'multiply', 'page',
          'question', 'number', 'submission', 'again', 'go', 'homework', 'deadline', 'subject',
          'division', 'next', 'hello', 'exams', 'meeting', 'understand', 'explain', 'how', 'answer',
          'week', 'monday', 'saturday', 'thursday', 'tuesday', 'wednesday']



# Emotion predict function (emotion)
# Predict the emotion of the frame 
def predict_emotion(image, time, meeting_name):
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
        


# Preprocess frames for sign langauge model (sign)
def preprocess(frames):
    """
    Preprocess frames for prediction.
    frames: list of frames
    returns: preprocessed frames
    """

    # Store new frames after preprocessing
    new_frames = []

    # drop first frame from subtraction
    frames.pop(0)
    
    # check if frames numbers more than 80
    while len(frames) > 80:
        # Check if first frame is white frame
        if np.sum(frames[0]) == np.sum(WHITE_FRAME):
            frames.pop(0)
        else:
            break
            
    # Get number of added frames 
    num_add_frames = max(0, 80 - len(frames))

    # FILL WITH WHITE FRAMES
    for i in range(num_add_frames):
        new_frames.append(WHITE_FRAME)
        
    # add frames
    k = len(new_frames)
    for f in range(80 - k):
        new_frames.append(frames[f])

    window = []
    for i in range(20):
        frame1 = new_frames[i * 4]
        frame1 = cv.resize(frame1, (128, 128))

        frame2 = new_frames[i * 4 + 1]
        frame2 = cv.resize(frame2, (128, 128))

        frame3 = new_frames[i * 4 + 2]
        frame3 = cv.resize(frame3, (128, 128))

        frame4 = new_frames[i * 4 + 3]
        frame4 = cv.resize(frame4, (128, 128))

        c1 = np.concatenate([frame1,frame2], axis = 1)
        c2 = np.concatenate([frame3,frame4], axis = 1)
        combinedFrame = np.concatenate([c1, c2])

        window.append(combinedFrame)

    X = np.array(window).tolist()
    return X


def predict(frames):
    """
    Predict sign from frames.
    frames: list of frames
    returns: predicted sign
    """
    global currentResult
    frames = preprocess(frames)
    # pred = model.predict(frames)
    # pred = np.argmax(pred, axis=1)
    # result = LABELS[pred[0]]
    currentResult = 'Aboda'



def detectHand(frame):
    """
    Detects hands in the frame add it to current frames.
    frame: frame as np.array
    """
    global currentFrames
    global currentResult

    # detect hand
    handResults = hands.process(frame)

    # if sign start
    # if handResults.multi_hand_landmarks != None:
    # frame = cv.resize(frame, (800, 800))
    # Apply background subtraction
    for frame in frames:
        fgMask = BACKSUB.apply(frame)  
            
        # apply filters
        erKernel = np.ones((4,4), np.uint8)
        dilKernel = np.ones((4,4), np.uint8)
        fgMask = cv.erode(fgMask, erKernel, iterations=2)       # Erode
        fgMask = cv.dilate(fgMask, dilKernel, iterations=2)     # Dilate
        fgMask = cv.GaussianBlur(fgMask, (1,1), 0)              # Blur
        fgMask[np.abs(fgMask) < 250] = 0                    
        fgMask = cv.bitwise_not(fgMask)                         # (800, 800)    

        currentFrames.append(frame)
        #print('length of current frame:', len(currentFrames))
        """
        else:
            if len(currentFrames) < 50:
                currentFrames = []
            else:
        """
        if len(currentFrames) > 50:
            currentResult = predict(currentFrames)
            currentFrames = []



# API
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


# BaseModel for the request body (emotion)
class ItemEmotion(BaseModel):
    frame : list = []
    time : int
    meeting_name:str

# BaseModel for the request body (sign)
class ItemSign(BaseModel):
    frame: list = []

# post request for image
@app.post("/postframe/")
async def post_frame(item: ItemSign, background_tasks: BackgroundTasks):
    """
    Post frame to API.
    item: frame
    returns: prediction
    """

    # Get the image from the request
    frame = item.frame

    # Convert the image to a numpy array
    frame = np.array(frame, dtype=np.uint8)
    print("XXXXXXXXXXXXXX",frame.shape)
    frames = []
    for i in range(frame.shape[0]):
        frames.append(frame[i,:].reshape(128, 128, 4)[:,:,:3])
    
    # Send the image to the background task
    background_tasks.add_task(detectHand, frames)

    # Return the result
    return json.dumps({"result": len(currentFrames),
                       "prediction": currentResult})
    

# Post request with the frame and the time of the frame
@app.post('/sendphoto/')
async def post_image(item: ItemEmotion, background_tasks:BackgroundTasks):
    
    image = np.array(item.frame)
    time = item.time
    meeting_name = item.meeting_name

    # model prediction
    background_tasks.add_task(predict_emotion, image, time, meeting_name)

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
