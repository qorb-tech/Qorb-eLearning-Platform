import json
import pandas as pd

class Charts:

    def __init__(self, data_path) -> None:
        self.data = pd.read_csv(data_path)
        self.pred = self.data['prediction']
        self.time = self.data['time']    
    
    def getStates(self):  
        maxi = max(self.time) + 1

        neutral = [0] * maxi
        sad = [0] * maxi
        angry = [0] * maxi
        surprise = [0] * maxi
        fear = [0] * maxi
        happy = [0] * maxi

        for i in range(len(self.data)):
            if self.pred[i] == 'neutral':
                neutral[self.time[i]] += 1
            elif self.pred[i] == 'surprise':
                surprise[self.time[i]] += 1
            elif self.pred[i] == 'fear':
                fear[self.time[i]] += 1
            elif self.pred[i] == 'surprise':
                happy[self.time[i]] += 1
            elif self.pred[i] == 'sad':
                sad[self.time[i]] += 1
            elif self.pred[i] == 'angry':
                angry[self.time[i]] += 1

        result = {
            'neutral':neutral,
            'sad':sad,
            'angry':angry,
            'surprise':surprise,
            'fear':fear,
            'happy':happy,
            'y':list(range(0,maxi))
        }

        return json.dumps(result)


    def CustomizedBar(self):
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
