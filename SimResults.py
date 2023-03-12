import numpy as np
class SimResults :
    MAX_QL = 10000
    def __init__(self):
        self.sumQL = 0
        self.oldTime = 0
        self.queueLengthHistogram = np.zeros(self.MAX_QL + 1)

    def registerQueueLength(self, time, ql):
        self.sumQL += ql * (time - self.oldTime)
        self.queueLengthHistogram[min(ql, self.MAX_QL)] += (time - self.oldTime)
    
    def getMeanQueueLength(self):
        return self.sumQL / self.oldTime
    
    def getQueueLengthProbabilites(self):
        return [x/self.oldTime for x in self.queueLengthHistogram]