import time 

class Chrono:
    def __init__(self):
        self.lastCheckpoint = time.time()
        self.SetCheckpoint()
    
    def GetTimeFromCheckpoint(self):
        return (time.time() - self.lastCheckpoint)
    
    def SetCheckpoint(self):
        timeFromLastCheckpoint = self.GetTimeFromCheckpoint()
        self.lastCheckpoint = time.time()
        return timeFromLastCheckpoint
    