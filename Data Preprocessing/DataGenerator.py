import os
import copy
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import to_categorical

class DataGenerator(tf.keras.utils.Sequence):

    def __init__(self, list_IDs, label_dic, labels, batch_size=32, dim=(256,256,20), n_channels=1, n_classes=3, shuffle=True):
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.current_dic = copy.deepcopy(label_dic)
        self.original_dic = label_dic
        self.label_map = {label:num for num, label in enumerate(self.labels)}
    
    def on_epoch_end(self):
        '''
            After epoch end create a new version of data dictionary for next epoch and shuffle it
        '''
        self.current_dic = copy.deepcopy(self.original_dic)
        for label in self.labels:
            np.random.shuffle(self.current_dic[label])

    def rest_words(self):
        '''
            update data after take batch from it
            Returns:
                The current data status
        '''
        word_list = random.choices(list(self.current_dic.keys()), k=self.batch_size)
        result_dic = {}

        for i in self.current_dic.keys():
            result_dic[i] = []

        undone = []
        while True:
            for idx in word_list:

                if idx in self.current_dic.keys():    
                    result_dic[idx].append(self.current_dic[idx][0])
                    del self.current_dic[idx][0]

                    if len(self.current_dic[idx]) == 0:
                        del self.current_dic[idx]

                else:
                    undone.append(idx)
            
            if len(undone) == 0:
                break
            else:
                word_list = random.choices(list(self.current_dic.keys()), k=len(undone))
                undone = []
            
        return result_dic


    def __data_generation(self, result_dic):
        '''
            Generates a batch of data
            Arguments:
                result_dic: data not feeded yet
            return :
                 a batch of data
        '''

        X = []
        y = []

        # Generate data
        for label in result_dic.keys():
            for i in result_dic[label]:
                # Store sample
                seq = np.load('drive/MyDrive/NPdata/' + label + '/' + str(i) + '.npy')
                X.append(seq)
                y.append(self.label_map[label])
        
        X = np.array(X) 
        y = np.array(y)
        
        X = np.transpose(X, (0,3,1,2))
        X = X.reshape(X.shape[0],X.shape[1], X.shape[2], X.shape[3], self.n_channels)

        return X, tf.keras.utils.to_categorical(y, num_classes=self.n_classes)
    
    def __len__(self):
        '''
            return number of batches
        '''

        length = int(np.floor(np.sum(list(self.list_IDs.values())) / self.batch_size)) - 1
        return length

    def __getitem__(self, index):
        '''
            get batch of data to feed to the model
        '''
        result_dic = self.rest_words()
        X, y = self.__data_generation(result_dic)
        return X, y