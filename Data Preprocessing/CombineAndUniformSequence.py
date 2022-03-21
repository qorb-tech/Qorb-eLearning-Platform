import os
import cv2 as cv
import numpy as np

def main():
    # directories to combine
    dirs = ['s1', 's2']

    # Create Directories to save data
    data = 'data'
    if not os.path.isdir(data):
        os.mkdir(data)
        words = ['plus', 'minus', 'zero', 'one', 'ten', 'two', 'three', 'four','five', 'six', 'seven', 'eight', 'nine', 'equal', 'day', 'this', 'appointment', 'important', 'please', 'explicate', 'break', 'need', 'multiply', 'page', 'question', 'number', 'submission', 'again', 'go', 'homework', 'deadline', 'subject', 'division', 'next', 'hello', 'saturday', 'thursday', 'friday', 'part', 'tuesday', 'exams', 'meeting', 'wednesday', 'sunday', 'monday', 'understand', 'explain', 'how', 'answer', 'week']
        for word in words:
            word_path = 'data/' + word
            os.mkdir(word_path)                                                

    # Go throw directories
    for dir in dirs:
        # Get all words
        words = list(os.listdir(dir))
        
        # Go throw all words
        for word in words:
            sample_path = 'data/' + word  
            samples = list(os.listdir(sample_path))

            for sample in samples:
                frames_path = sample_path + '/' + sample
                frames = list(os.listdir(frames_path))

                while len(frames) > 80:
                    # get first frame in list
                    current_frame = cv.imread(frames_path + '/' + frames[0])
                    current_frame = current_frame[:,:,0].reshape(800,800,1)

                    # Check if first frame is white frame
                    if np.sum(current_frame) == np.sum(white_frame):
                        frames.pop(0)
                    else:
                        break
                
                # Get number of added frames 
                num_add_frames = max(0, 80 - len(frames))

                # Add White Frames

                # Create new samples directory
                new_word_path = data + '/' + word
                new_samples_count = len(os.listdir(new_word_path))
                new_sample_path = new_word_path + '/' + str(new_samples_count)
                os.makedirs(new_sample_path)

                j = 0
                for i in range(num_add_frames):
                    cv.imwrite(new_sample_path + '/{}.jpg'.format(j), white_frame)
                    j += 1
                
                k = j
                for f in range(80 - k):
                    saved_frame = cv.imread(frames_path + '/' + frames[f])
                    saved_frame = saved_frame[:,:,0].reshape(800,800,1)
                    cv.imwrite(new_sample_path + '/{}.jpg'.format(j), saved_frame)
                    j += 1
                    


if __name__ == '__main__':
    main()


