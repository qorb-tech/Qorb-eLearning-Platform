import json
import pandas as pd

class Charts:

    def __init__(self, data_path) -> None:
        """
        Initialize the class
        data_path: str
        """
        self.data = pd.read_csv(data_path)
        self.pred = self.data['prediction']
        self.time = self.data['time']    
    
    def getStates(self):
        """
        Get the status of the meeting
        return: student status throught the meeting
        """
        # length of the meeting
        maxi = max(self.time) + 1

        # Initialize the status
        neutral = [0] * maxi
        sad = [0] * maxi
        angry = [0] * maxi
        surprise = [0] * maxi
        fear = [0] * maxi
        happy = [0] * maxi

        # Count the number of each emotion
        for i in range(len(self.data)):
            if self.pred[i] == 'neutral':
                neutral[self.time[i]] += 1
            elif self.pred[i] == 'Surprise':
                surprise[self.time[i]] += 1
            elif self.pred[i] == 'Fear':
                fear[self.time[i]] += 1
            elif self.pred[i] == 'Surprise':
                happy[self.time[i]] += 1
            elif self.pred[i] == 'Sad':
                sad[self.time[i]] += 1
            elif self.pred[i] == 'Angry':
                angry[self.time[i]] += 1

        result = {
            'neutral':neutral,
            'sad':sad,
            'angry':angry,
            'surprise':surprise,
            'fear':fear,
            'happy':happy,
            'y':list(range(0,maxi+1))
        }

        return json.dumps(result)


    def CustomizedBar(self):
        """
        Get the name and count of the emotion throught the meeting
        return: name, value
        """
        
        mymap = {}
        for i in range(len(self.data)):
            if self.pred[i] not in mymap.keys():
                mymap[self.pred[i]] = 1
            else:
                mymap[self.pred[i]] += 1
        
        result = {
            'value': list(mymap.values()),
            'name': list(mymap.keys())
        }
        
        return json.dumps(result)
