from scipy import stats
from Distribution import Distribution
from Event import Event
from FES import FES
from SimResults import SimResults

class simulationFCFS:
    def __init__(self , arrDist , servDist):
        #number of servers will always be equal to 1 (one intersection)
        self.arrDist = arrDist
        self.servDist = servDist
    
    #T is the time we simulate
    def simulate(self, T):
        q = 0 # queue length
        t = 0 # current time
        #S = 0 # for surface, we used SimResults here
        res = SimResults()
        fes = FES() #scheduling events
        firstEvent = Event(Event.ARRIVAL , self.arrDist.rvs())
        fes.add(firstEvent)
        while t < T :
            # tOld = t don't need this because we have future event set
            # jump to next event
            e = fes.next()
            # update the time
            t = e.time
            # register the queue length
            res.RegisterQueueLength(t, q)

            # if event is an arrival :
            if e.type == Event.ARRIVAL :
                # increase queue length
                q += 1
                # there is an available server
                dep = Event(Event.DEPARTURE, t + self.servDist.rvs())
                fes.add(dep)
                arr = Event(Event.ARRIVAL, t + self.arrDist.rvs())
                fes.add(arr)
            # schedule next arrival
            elif e.type == Event.DEPARTURE :
                # event is departure
                q -= 1
                # decrease queue length
                if q >= self.nrServers :
                    # someone is waiting for service
                    dep = Event(Event.DEPARTURE, t + self.servDist.rvs())
                fes.add(dep)
        return res

ex = stats.expon(scale=1)
ex
arrDist = Distribution(stats.expon(scale=1/2.0)) # here we input the distribution
servDist = Distribution(stats.expon(scale=1/1.0)) # here we input the distribution
sim = simulationFCFS(arrDist, servDist, 1)
res = sim.simulate(1000000)