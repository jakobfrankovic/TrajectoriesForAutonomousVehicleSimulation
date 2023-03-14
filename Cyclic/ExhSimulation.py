from Lane import *
from Event import *
from CES import *
from typing import *
from SimResults import *
from FES import *


class ExhaustiveSimulation:
    """Exhaustive simulation object"""
    def __init__(self, arrDist, nrServers = 1):
        self.arrDist = arrDist #arrival distributions of the cars
        self.nrServers = nrServers

    def Simulate(self, T, nLanes, arrDist, arrDist2):
        """Implementation of the main simulation
        T: integer denoting the maximum running time
        nLanes: amount of lanes"""
        lanes: List[Lane] = createLanes(nLanes) #create a list with nLanes lane objects

        nCars = 0 # current number of cars
        t = 0 #current time
        arrival0 = arrDist
        arrival1 = arrDist2

        previousDepartureTime = 0
        earliestTime = 0

        # Choosing which car from which lane goes first
        if arrival0[0] < arrival1[0]:
            earliestTime = arrival0.pop(0)
            activeLane = lanes[0]
        else:
            earliestTime = arrival1.pop(0)
            activeLane = lanes[1]

        c0 = Car(earliestTime, activeLane) # first customer
        res: SimResults = SimResults() #object to store the simulation results
        fes: FES = FES() #future event set
        firstEvent = Event(Event.ARRIVAL, c0.arrivalTime, c0)

        fes.add(firstEvent) #add the first event to the future event set
        cycQ: cyclicQueue = cyclicQueue() #create a cyclic queue object
        while t < T:
            """Main loop"""
            e = fes.next #go to next event
            t = e.time #update time
            c1 = e.car #car associated with this event
            res.registerQueueLength (t, nCars) #register lane length
            nLoops = 0 #needed to for the lane switching process to prevent an endless while loop

            while activeLane.isEmpty() and nLoops < len(lanes):
                activeLaneIndex = lanes.index(activeLane)  # get the index of the active lane

                # switch lanes
                try:
                     activeLane = lanes[activeLaneIndex + 1]
                # if the active lane is the last in the list of lanes, switch back to the very first one
                except:
                    activeLane = lanes[0]

                if not activeLane.isEmpty():
                    t += 2.4 #if lanes are switched, add intersection clearing time

                nLoops += 1


            if e.type == Event.ARRIVAL:
                c1.lane.addCar(t) #add a car with arrival time t to the correct lane
                nCars += 1
                if len(c1.lane) == 1: #if the arrived car is the only car in the lane
                    if c1.lane == activeLane:
                        res.registerWaitingTime(t - c1.arrivalTime)
                        #schedule a department
                        dep = Event(Event.DEPARTURE, t, c1)
                        previousDepartureTime = t
                    fes.add(dep)

            elif e.type == Event.DEPARTURE: # handle a departure event
                previousDepartureTime = t
                activeLane = c1.lane #change the active lane
                activeLane.remove(c1) # remove the car
                nCars -= 1
                res.registerWaitingTime(t - c1.arrivalTime)

                if len(activeLane) >= self.nrServers : # if there is a car waiting in the active lane
                    c2 = c1.lane[self.nrServers-1] # longest waiting customer in the lane

                    #create and schedule the next departure
                    dep = Event(Event.DEPARTURE, previousDepartureTime + c2.arrivalTime - c1.arrivalTime, c2)
                    fes.add(dep)

            if not activeLane.isEmpty():
                #schedule the departure of the longest waiting car in the active lane
                if t - previousDepartureTime > 1:
                    dep = Event(Event.DEPARTURE, t, activeLane[-1])
                else:
                    #if the cars are less than 1 second from each other, wait until the distance is 1 second for the departure
                    dep = Event(Event.DEPARTURE, previousDepartureTime + 1, activeLane[-1])

                previousDepartureTime = t
                fes.add(dep)


