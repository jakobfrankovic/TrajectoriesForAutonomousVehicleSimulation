class Event :
    ARRIVAL = 0
    DEPARTURE = 1
    # constant for arrival type
    # constant for departure type
    def __init__ ( self, typ, time):
        self.type = typ
        self.time = time
    # type is a reserved word
    def __lt__ ( self , other ):
        # compare to other events
        return  self.time < other.time