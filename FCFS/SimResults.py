from collections import deque
import numpy 
import matplotlib.pyplot as plt

class SimResults:

    MAX_QL = 10000 # maximum queue length that will be recorded
    def __init__(self):
        self.sumQL = 0
        self.sumQL2 = 0
        self.oldTime = 0
        self.queueLengthHistogram = numpy.zeros(self.MAX_QL + 1)
        self.sumW = 0
        self.sumW2 = 0
        self.nW = 0
        self.waitingTimes = deque()

    def registerQueueLength(self, time, ql):
        self.sumQL += ql * (time - self.oldTime)
        self.sumQL2 += ql * ql * (time - self.oldTime)
        self.queueLengthHistogram[min(ql, self.MAX_QL)] += (time - self.oldTime)
        self.oldTime = time

    def registerWaitingTime(self, w):
        self.waitingTimes.append(w) 
        self.nW += 1
        self.sumW += w
        self.sumW2 += w * w

    def getMeanQueueLength(self):
        return self.sumQL / self.oldTime 
    def getVarianceQueueLength(self):
        return self.sumQL2 / self.oldTime - self.getMeanQueueLength()**2

    def getMeanWaitingTime(self):
        return self.sumW / self.nW 
    def getVarianceWaitingTime(self):
        return self.sumW2 / self.nW - self.getMeanWaitingTime()**2

    def getQueueLengthHistogram(self) :
        return [x/self.oldTime for x in self.queueLengthHistogram] 
    def getWaitingTimes(self): 
        return self.waitingTimes

    def __str__(self):
        s = 'Mean queue length: ' + str(self.getMeanQueueLength()) + '\n'
        s += 'Variance queue length: '+str(self.getVarianceQueueLength()) + '\n'
        s += 'Mean waiting time: '+str(self.getMeanWaitingTime()) + '\n'
        s += 'Variance waiting time: '+str(self.getVarianceWaitingTime()) + '\n'
        return s 
    
    def histQueueLength(self, maxq=50):
        ql = self.getQueueLengthHistogram()
        maxx = maxq + 1
        plt.figure()
        plt.bar(range(0, maxx), ql[0:maxx])
        plt.ylabel('P(Q = k)')
        plt.xlabel('k')
        plt.show()

    def histWaitingTimes(self, nrBins=100): 
        plt.figure()
        plt.hist(self.waitingTimes, bins=nrBins, rwidth=0.8, density=True) 
        plt.show()