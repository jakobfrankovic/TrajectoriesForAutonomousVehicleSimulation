from typing import *
class Event:
    ARRIVAL = 0
    DEPARTURE = 1

    def __init__(self, typ, time : int or float, car=None):  # type is a reserved word
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
