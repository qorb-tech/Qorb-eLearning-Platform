# Importing Essential Libraries
import os
import time
import cv2 as cv
import numpy as np

def preprocess(word, video_path, ArabicToEnglish):
    '''
        Apply Filters, background subtraction and save frames
        Arguments:
            word(str): current word to aplly on it
            video_path(str): Video path
            ArabicToEnglish: map from arabic word to english words
    '''

    # create diretory to save frames
    save_path = create_word_directory(word, ArabicToEnglish)                     
    
    backSub = cv.createBackgroundSubtractorMOG2()               # define background subtraction method
    capture = cv.VideoCapture(video_path)                       # Capture first frame from video path
    
    i = 1                                                       # current frame number
    while True:
        i += 1                                                  # Increment frame number

        ret, frame = capture.read()                             # Capture a frame
        if frame is None:                                       # Check if there is a frame or not
            break
        
        frame = cv.resize(frame, (800, 800))                    # Resize the frame

        fgMask = backSub.apply(frame)                           # Apply background subtraction
        

        erKernel = np.ones((4,4), np.uint8)
        dilKernel = np.ones((4,4), np.uint8)

        fgMask = cv.erode(fgMask, erKernel, iterations=2)       # Erode
        fgMask = cv.dilate(fgMask, dilKernel, iterations=2)     # Dilate
        fgMask = cv.GaussianBlur(fgMask, (1,1), 0)              # Blur
        fgMask[np.abs(fgMask) < 250] = 0

        cv.imwrite(save_path + '\\frame{}.jpg'.format(i), cv.bitwise_not(fgMask))

       
        keyboard = cv.waitKey(30)
        if keyboard == 'q' or keyboard == 27:
            break


def create_word_directory(word, ArabicToEnglish):
    '''
        Create the directory for each coming word and return the path for each word
        Arguments:
            word(str): current word
            ArabicToEnglish(dic): Map from Arabic words to English words
        Return:
            save_path: a path to save current word
    '''
    # check if word directory created or make a new one
    word_save_path = 'done/' + str(ArabicToEnglish[word])
    if not os.path.isdir(word_save_path):
        os.mkdir(word_save_path)
    
    # check how many person saved in this file
    persons_numbers = len(os.listdir(word_save_path))

    # create directory to save frames
    os.mkdir(word_save_path + '/' + str(persons_numbers))

    # save path
    save_path = word_save_path + '/' + str(persons_numbers)

    return save_path

# Main Function
def main():
    # Map arabic and english words
    arabic = ['+', '-', '0', '1', '10', '2', '3', '4', '5', '6', '7', '8', '9', '=', 'يوم', 'هذا', 'موعد', 'مهم', 'لو سمحت', 'فسر لي', 'فسحة', 'عاوز', 'ضرب', 'صفحة', 'سؤال', 'رقم', 'تسليم', 'تاني', 'امشي', 'الواجب', 'الموعد النهائي النهاية', 'الموضوع', 'القسمة', 'القادم', 'السلام عليكم', 'السبت', 'الخميس', 'الجمعة', 'الجزء', 'الثلاثاء', 'الامتحانات', 'الاجتماع', 'الأربعاء', 'الأحد', 'الأثنين', 'افهم', 'اشرح لي', 'استفهام كيف_متي', 'إجابة', 'أسبوع']
    english = ['plus', 'minus', 'zero', 'one', 'ten', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
               'nine', 'equal', 'day', 'this', 'appointment', 'important', 'please', 'explicate', 'break',
               'need', 'multiply', 'page', 'question', 'number', 'submission', 'again', 'go', 'homework', 'deadline',
               'subject', 'division', 'next', 'hello', 'saturday', 'thursday', 'friday', 'part', 'tuesday', 'exams',
               'meeting', 'wednesday', 'sunday', 'monday', 'understand', 'explain', 'how', 'answer', 'week']
    
    ArabicToEnglish = dict(zip(arabic, english))

    # Create directory to save data if not created before
    if not os.path.isdir('done'):
        os.mkdir('done')

    # get person list
    persons = os.listdir('data')
    
    # Go throw all persons in dataset
    for person in persons:
        
        # get words list
        words = os.listdir('data/' + str(person))

        # go throw all words
        for word in words:
            word_path = 'data/' + str(person) + '/' + str(word)               # word path
            videos = os.listdir(word_path)

            for video in videos:
                video_path = word_path + '/' + video
                preprocess(word, video_path, ArabicToEnglish)                       # start preprocessing
    
if __name__ == '__main__':
    main()
