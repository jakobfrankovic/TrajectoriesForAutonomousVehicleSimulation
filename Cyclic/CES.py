class cyclicQueue:
    """Implementation of the cyclic exhaustive service method of handling the queue"""

    def __init__(self, lanes : list):
        self.lanes = lanes #list with the queue objects
        self.activeLane = lanes[0] #start with the first lane being the active one

    def switch(self, lanes):
        """Function that switches lanes in a cyclic way"""
        activeLaneIndex = self.lanes.index(self.activeLane) #get the index of the active queue in queues

        #switch queues if the active queue is empty
        try:
            self.activeLane = self.lanes[activeLaneIndex + 1]
        #if the active queue is the last in the list of queues, switch back to the very first one
        except:
            self.activeLane = self.lanes[0]

