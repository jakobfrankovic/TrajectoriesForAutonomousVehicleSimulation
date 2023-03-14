from typing import * #to add type hints
from Car import *
from collections import deque

class Lane:
    """Lane/queue object"""
    def __init__(self):
        self.cars: deque = deque() #list of cars on the lane, initialized as empty

    def isEmpty(self) -> bool:
        """Returns whether a lane is empty or not"""
        return len(self.cars) == 0

    def addCar(self, arrTime: int | float) -> None:
        """Function to add a car to a lane
        arrTime: float denoting the arrival time of the car
        laneNr: integer specifying what lane the car is added to"""
        assert type(arrTime) == int or float #test whether the given arrival time is an integer or float
        assert arrTime > 0 #check that the arrival time is positive
        car: Car = Car(arrTime) #declare a new car instance
        self.cars.append(car)

    def reverse(self):
        """Return the cars in the lane based on descending wait time"""
        return self.cars.reverse()

    def nextCar(self):
        """Return the next car in the lane"""
        return

def createLanes(nLanes):
    """Function that adds nLanes Lane objects to a list and returns it"""
    assert type(nLanes) == int
    lanes = [] #empty list with all the lanes
    for i in range(nLanes):
        lanes.append(Lane())
    return lanes







# lanes = Lanes(3)
# print(lanes.placeholder())

# lane = Lane()
# lane.addCar(5.14)
# print(lane.cars)