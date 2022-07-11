import json
import cv2 as cv
import mediapipe as mp
import numpy as np
import tensorflow as tf

# Load the model
model = None

# Define Labels
LABELS = ['plus', 'equal', 'day', 'important', 'explicate', 'break', 'need', 'multiply', 'page', 'question', 'number', 'submission', 'again', 'go', 'homework', 'deadline', 'subject', 'division', 'next', 'hello', 'exams', 'meeting', 'understand', 'explain', 'how', 'answer', 'week', 'monday', 'saturday', 'thursday', 'tuesday', 'wednesday']

# Create background subtraction
BACKSUB = cv.createBackgroundSubtractorMOG2()
WHITE_FRAME = np.ones((800, 800)) * 255

# To Detect Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

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
    frames = preprocess(frames)
    # pred = model.predict(frames)
    # pred = np.argmax(pred, axis=1)
    # result = LABELS[pred[0]]
    return frames.shape


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
    if handResults.multi_hand_landmarks != None:
        # frame = cv.resize(frame, (800, 800))
        # Apply background subtraction
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
        print('length of current frame:', len(currentFrames))
    else:
        if len(currentFrames) < 50:
            currentFrames = []
        else:
            currentResult = predict(currentFrames)
            currentFrames = []
