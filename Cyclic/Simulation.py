from Car import *
from Lane import *
from Event import *
from CES import *
from typing import *

class Simulation:
    """Simulation object"""
    def __init__(self, arrDist):
        self.arrDist = arrDist #arrival distributions of the cars

    def Simulate(self, T, nLanes):
        """implementation of the main simulation"""
        lanes: List[Lane] = createLanes(nLanes) #create a list with nLanes lane objects
        nCars = 0 # current number of cars
        t = 0 #current time
        # res = SimResults()
        # fes = FES()
        firstEvent = Event(Event.ARRIVAL, time=self.arrDist.rvs())
        # fes.add(firstEvent)
        cycQ: cyclicQueue = cyclicQueue(lanes) #create a cyclic queue object

        while t < T:
            """Main loop"""
            # e = fes.next #go to next event
            # t = e.time #update time
            # res.registerQueueLength (t, ) #register queue length
            if cycQ.activeLane.isEmpty():
                cycQ.switch(lanes)

            if e.type == Event.ARRIVAL:
                cycQ.activeLane.addCar()

