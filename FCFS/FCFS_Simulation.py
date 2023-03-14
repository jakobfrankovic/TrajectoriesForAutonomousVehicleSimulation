from collections import deque
import pandas as pd
import Car 
import Event as ev
import SimResults 
import FES 

class GGcSimulation :
    def __init__(self, nrServers=1): # constructor
        # self.arrDist = arrDist
        # self.arrDist2 = arrDist2
        self.nrServers = nrServers 

    def simulate(self, arrDist, arrDist2):

        def getNextCar(arrDist, arrDist2):
            if len(arrDist2) == 0:
                nextCar = Car.Car(arrDist.pop(0), 0)
            elif len(arrDist) ==0:
                nextCar = Car.Car(arrDist2.pop(0), 1)
            elif arrDist[0] < arrDist2[0]:
                nextCar = Car.Car(arrDist.pop(0), 0)
            else:
                nextCar = Car.Car(arrDist2.pop(0), 1)
            return nextCar
        
        fes = FES.FES() # future event set
        res = SimResults.SimResults() # simulation results
        queue = deque() # the queue

        arrival0 = arrDist
        arrival1 = arrDist2

        previousDepartureTime = 0
        earliestTime = 0
        currentLane = 0

        # Choosing which car from which lane goes first
        if arrival0[0] < arrival1[0]:
            earliestTime = arrival0.pop(0)
        else:
            earliestTime = arrival1.pop(0)
            currentLane = 1

        t = 0 # current time
        c0 = Car.Car(earliestTime, currentLane) # first car
        firstEvent = ev.Event(ev.Event.ARRIVAL , c0.arrivalTime , c0)

        # print("Arrival " + str(c0.arrivalTime))
        fes.add(firstEvent) # schedule first arrival event

        while (len(arrival0) != 0 or len(arrival1) != 0) or len(queue) > 0: # main loop
            # print(len(queue))
            e = fes.next() # jump to next event
            t = e.time # update the time
            c1 = e.car # car associated with this event
            res.registerQueueLength(t, len(queue)) # register queue length

            if e.type == ev.Event.ARRIVAL: # handle an arrival event
                queue.append(c1) # add car to the queue
                if len(queue) <= self.nrServers : # there was a free server
                    res.registerWaitingTime(t - c1.arrivalTime)
                    if c1.lane == currentLane  :
                        dep = ev.Event(ev.Event.DEPARTURE, t, c1)
                        previousDepartureTime = t
                    else:
                        if (c1.arrivalTime - previousDepartureTime >= 2.4): #If the arrival time of the different lane is more than 2.4, then it can immediately move again
                            dep = ev.Event(ev.Event.DEPARTURE, t, c1)
                        else:
                            dep = ev.Event(ev.Event.DEPARTURE, previousDepartureTime + 2.4, c1)
                        previousDepartureTime = t
                        currentLane = c1.lane

                    fes.add(dep) # schedule his departure

                ## Next car if there are still cars coming
                if (len(arrival0) != 0 or len(arrival1) != 0):
                    c2 =  getNextCar(arrival0, arrival1) # create next arrival
                    arr = ev.Event(ev.Event.ARRIVAL , c2.arrivalTime , c2)
                    # print("Arrival " + str(c2.arrivalTime))
                    fes.add(arr) # schedule the next arrival

            elif e.type == ev.Event.DEPARTURE : # handle a departure event 
                # print("Departure " + str(t))
                previousDepartureTime = t
                queue.remove(c1) # remove the car
                res.registerWaitingTime(t - c1.arrivalTime)
                # print(t - c1.arrivalTime)

                if len(queue) >= self.nrServers : # someone was waiting
                    c2 = queue[self.nrServers-1] # longest waiting car
                    # res.registerWaitingTime(t - c2.arrivalTime)

                    # If lanes are changed then time added is different
                    if c2.lane == currentLane:
                        dep = ev.Event(ev.Event.DEPARTURE, previousDepartureTime + 1, c2)
                        previousDepartureTime = t
                    else:
                        dep = ev.Event(ev.Event.DEPARTURE, previousDepartureTime + 2.4, c2)
                        currentLane = c2.lane
                        previousDepartureTime = t

                    fes.add(dep) # schedule this departure 
        return res
            
# arrDist = Distribution(stats.expon(scale=1/2.4)) # interarrival time distr.
# servDist = Distribution(stats.expon(scale=1/1.0)) # service time distribution 

dataframe = pd.read_excel('arrivals30.xlsx', header=None)

arrivalTime1 = dataframe[dataframe.columns[0]].to_list()
arrivalTime2 = dataframe[dataframe.columns[1]].to_list()

# arrivalTime1 = arrivalTime1[:10]
# arrivalTime2 = arrivalTime2[:10]

# arrivalTime1 = [1, 2, 4.816, 9.158]
# arrivalTime2 = [2.309, 3.309, 5.169, 6.985, 8.051, 9.996]

# arrivalTime1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# arrivalTime2 = [13, 14, 15, 16, 17, 18, 19, 20]

sim = GGcSimulation() # the simulation model
res = sim.simulate(arrivalTime1, arrivalTime2) # perform simulation

print(res) # print the results
# res.histQueueLength() # plot of the queue length
# res.histWaitingTimes() # histogram of waiting times