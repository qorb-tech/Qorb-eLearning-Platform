import os
import cv2 as cv
import numpy as np

def load_frame(word, sequence, frame_num, data_path):
    '''
        load one frame from data
        Argument:
            word(str): current word
            sequence(int): current sequence
            frame_num(int): Frame number
            data_path(str): all data path
        Returns
            A frame 
    '''

    frame = cv.imread(data_path + '/' + word + '/' + str(sequence) + '/' + str(frame_num) + '.jpg')
    frame = cv.resize(frame, (128, 128))        # resize the frame
    frame = frame[:,:,0]

    return frame

def main():
    # words to combine and save
    words = []

    # Loading Data
    data_path = 'data'
    save_path = 'NPdata/'

    # number of sequence
    no_sequences = 150
                                
    # number of frames
    sequence_length = 20

    for word in words:
        for sequence in range(no_sequences):
            window = []

            for frame_num in range(sequence_length):
                # Combine Frames
                frame1 = load_frame(word, sequence, 4 * frame_num, data_path)
                frame2 = load_frame(word, sequence, 4 * frame_num + 1, data_path)
                frame3 = load_frame(word, sequence, 4 * frame_num + 2, data_path)
                frame4 = load_frame(word, sequence, 4 * frame_num + 3, data_path)

                c1 = np.concatenate([frame1,frame2], axis = 1)
                c2 = np.concatenate([frame3,frame4], axis = 1)
                combinedFrame = np.concatenate([c1, c2])
        
                window.append(combinedFrame)

            X = np.array(window)
            X = np.transpose(X, (1, 2, 0))

            np.save(save_path + word + '/' + str(sequence) + '.npy', X)
            print('Done {} seq {}'.format(word, sequence))

if __name__ == '__main__':
    main()