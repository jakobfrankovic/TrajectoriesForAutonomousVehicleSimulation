import numpy as np
import pandas as pd
from CES import *
from typing import *
from SimResults import *
from FES import *
from collections import deque

class Car:
    """Class for car objects"""
    def __init__(self, arrivalTime, lane):
        self.arrivalTime = arrivalTime
        self.lane = lane

class Event:
    ARRIVAL = 0
    DEPARTURE = 1

    def __init__(self, typ, time : int | float, car):  # type is a reserved word
        self.type = typ
        self.time = time
        self.car = car

    def __lt__(self, other) -> bool:
        """Method that returns whether an event takes place earlier or later than some other event"""
        return self.time < other.time

    def __str__(self) -> str:
        """String representation of the event"""
        s = ("Arrival", "Departure")
        return s[self.type] + "of customer" + str(self.customer) + "at t =" + str(self.time)


class Lane:
    """Lane/queue object"""
    def __init__(self):
        self.cars: deque = deque() #list of cars on the lane, initialized as empty

    def isEmpty(self) -> bool:
        """Returns whether a lane is empty or not"""
        return len(self.cars) == 0

    def addCar(self, arrTime: int | float, lane) -> None:
        """Function to add a car to a lane
        arrTime: float denoting the arrival time of the car
        laneNr: integer specifying what lane the car is added to"""
        assert type(arrTime) == int or float #test whether the given arrival time is an integer or float
        assert arrTime > 0 #check that the arrival time is positive
        car: Car = Car(arrTime, lane) #declare a new car instance
        self.cars.append(car)

    def remove_last_car(self):
        """Remove the car object that waited the longest in a lane"""
        del self.cars[-1]
        return self.cars

    def reverse(self):
        return self.cars.reverse()

    def length(self):
        return len(self.cars)

    def longestWaitingCar(self):
        return self.cars[-1]

def createLanes(nLanes):
    """Function that adds nLanes Lane objects to a list and returns it"""
    assert type(nLanes) == int
    lanes = deque() #empty list with all the lanes
    for i in range(nLanes):
        lanes.append(Lane())
    return lanes

class ExhaustiveSimulation:
    """Exhaustive simulation object"""
    def __init__(self, nrServers = 1):
        self.nrServers = nrServers

    def Simulate(self, T, arrDist, nLanes=2):
        """Implementation of the main simulation
        T: integer denoting the maximum running time
        nLanes: amount of lanes"""
        lanes: Deque[Lane] = createLanes(nLanes) #create a list with nLanes lane objects

        nCars = 0 # current number of cars
        t = 0 #current time
        arrival0 = arrDist[0]
        arrival1 = arrDist[1]
        arrivals = [arrival0, arrival1]

        activeLane = lanes[0]
        previousDepartureTime = 0
        earliestTime = np.inf

        # Choosing which car from which lane goes first
        if arrival0[0] < arrival1[0]:
            earliestTime = arrival0.pop(0)
        else:
            earliestTime = arrival1.pop(0)
            activeLane = lanes[1]

        c0 = Car(earliestTime, activeLane) # first customer
        res: SimResults = SimResults() #object to store the simulation results
        fes: FES = FES() #future event set
        firstEvent = Event(Event.ARRIVAL, c0.arrivalTime, c0)
        activeLane.addCar(c0.arrivalTime, c0.lane)
        fes.add(firstEvent) #add the first event to the future event set
        while t < T:
            """Main loop"""
            e = fes.next() #go to next event
            t = e.time #update time
            c1 = e.car #car associated with this event
            res.registerQueueLength (t, nCars) #register lane length
            nLoops = 0 #needed to for the lane switching process to prevent an endless while loop

            #switch lanes if the active lane is empty. If all lanes are empty, wait for an arrival
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
                c1.lane.addCar(t, c1.lane)#add a car to the lane
                nCars += 1
                if c1.lane.length() == 1: #if the arrived car is the only car in the lane
                    if c1.lane == activeLane:
                        res.registerWaitingTime(t - c1.arrivalTime)
                        #schedule a department
                        dep = Event(Event.DEPARTURE, t, c1)
                        previousDepartureTime = t
                        fes.add(dep)
                arr = Event(Event.ARRIVAL, min(arrival0[0], arrival1[0]), Car(t, c1.lane))
                fes.add(arr)


            elif e.type == Event.DEPARTURE: # handle a departure event
                previousDepartureTime = t
                activeLane = c1.lane #change the active lane
                activeLane.cars.remove(c1) # remove the car
                nCars -= 1
                res.registerWaitingTime(t - c1.arrivalTime)

                if not activeLane.isEmpty(): # if there is a car waiting in the active lane
                    c2 = c1.lane.cars[-1] # longest waiting customer in the lane

                    #create and schedule the next departure
                    dep = Event(Event.DEPARTURE, previousDepartureTime + c2.arrivalTime - c1.arrivalTime, c2)
                    fes.add(dep)

            if not activeLane.isEmpty():
                #schedule the departure of the longest waiting car in the active lane
                if t - previousDepartureTime > 1:
                    dep = Event(Event.DEPARTURE, t, activeLane[-1])
                else:
                    #if the cars are less than 1 second from each other, wait until the distance is 1 second for the departure
                    dep = Event(Event.DEPARTURE, previousDepartureTime + 1, activeLane.longestWaitingCar())

                previousDepartureTime = t
                fes.add(dep)

        return(res)


dataframe = pd.read_excel('../arrivals30.xlsx', header=None)
list_of_lists = dataframe.values.tolist()
arrTimeListList = list(map(list, zip(*list_of_lists))) #list of lists of the arrival times per lane

sim = ExhaustiveSimulation()
sim.Simulate(100, arrTimeListList)


