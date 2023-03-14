import pandas as pd
import numpy as np
from scipy import stats
import math
import functools
import random
from collections import deque

class Input:
    def __init__(self, data):
        self.data = data

    def get_coefficients(self):
        """
        Here we get coefficients alpha and mu for each column in the dataset. 
        We have 2 lanes, that is why we are going to have only 2 coefficents of alpha and mu.
        """
        df = pd.read_excel(self.data)
        array1 = np.array([df.columns[0]] + [arrival for arrival in df.iloc[:, 0]])
        array2 = np.array([df.columns[1]] + [arrival for arrival in df.iloc[:, 1]])

        #differences between two consecutive values
        diff_1 = np.diff(array1)
        diff_2 = np.diff(array2)

        #how many differences are equal to B = 1
        count1_B = np.count_nonzero(np.abs(diff_1 - 1) == 0)
        count2_B = np.count_nonzero(np.abs(diff_2 - 1) == 0)

        #probability of x <= B
        all1 = len(diff_1)
        all2 = len(diff_2)
        p_1 = count1_B / all1
        p_2 = count2_B / all2

        #coefficients alpha
        alpha1 = 1 - p_1
        alpha2 = 1 - p_2
        self.alpha1 = alpha1
        self.alpha2 = alpha2 

        #after integrating we solved E[A] = estimation, to get mu coeffficient
        mean1 = np.mean(diff_1)
        mean2 = np.mean(diff_2)
        mu1 = alpha1/(mean1 - 1)
        mu2 = alpha2/(mean2 - 1)
        self.mu1 = mu1
        self.mu2 = mu2
    
    #We return the coefficients we were able to get
    def mu(self):
        return [self.mu1, self.mu2]
    def alpha(self):
        return [self.alpha1, self.alpha2]
    
class Generate:
    """
    Used to generate variables given distribution in the assignment
    """
    def __init__(self, alpha, mu, lane_number):
        self.alpha = alpha[lane_number - 1]
        self.mu = mu[lane_number - 1]

    @staticmethod
    def inverse_transform_sampling(alpha, mu, dummy_par = None): #we use dummy_par only for map function to make it very very fast
        """
        We use inverse transform method to generate interarrival times
        """
        u = random.uniform(0, 1)
        if 0.4 <= u < 1:
            return (1/mu) * np.log(alpha/(1 - u)) + 1
        elif 0 < u < 0.4:
            return 1
        
    def generate_number(self, size):
        """
        We generate a number from distribution in assignment.

        lane_number ... in which lane do we want to generate (in our cas 1 or 2, we use differen mu and alpha according to the lane)
        size ... size of the sample
        """
        #we will create a partial function only because it is necessary that the function has only
        #   one parameter to use map. 
        alpha = self.alpha
        mu = self.mu
        partial_function = functools.partial(self.inverse_transform_sampling, alpha, mu)
        map_object = map(partial_function, np.zeros(size))
        self.arrivals = np.cumsum(list(map_object))
        return self.arrivals
    
    def non_homogenious_arrivals(self, maxLambda = 1):
        def lambdat(t, alpha, mu):
            array = []
            for x in t:
                array.append(1 - alpha*math.exp(-mu*(x-1)))
            return array
        maxLambda = mu[0] + 1
        allArrivals = self.arrivals
        udist = stats.uniform(0, 1)
        u = udist.rvs(len(allArrivals))
        accept = u * maxLambda < lambdat(allArrivals, alpha[0], mu[0])
        acceptedArrivals = allArrivals[accept]
        return acceptedArrivals
    

if __name__ == "__main__":
    input = Input("arrivals30.xlsx")
    input.get_coefficients()

    #we get lists of the coefficients 
    alpha = input.alpha()
    mu = input.mu()

    #we get interarrival times
    generator = Generate(alpha, mu, 1)
    array = generator.generate_number(100)

    #we checked the mean to see if it is correct
    #mean = np.mean(array)

    arrival_times = np.cumsum(array)

    #arrival_times = arrival_times.flatten()

    #from scipy import stats
    def lambdat(t, alpha, mu):
        array = []
        for x in t:
            array.append(1 - alpha*math.exp(-mu*(x-1)))
        return array

    maxLambda = mu[0] + 1
    allArrivals = arrival_times
    udist = stats.uniform(0, 1)
    u = udist.rvs(len(allArrivals))
    accept = u * maxLambda < lambdat(allArrivals, alpha[0], mu[0])
    acceptedArrivals = allArrivals[accept]

    import matplotlib.pyplot as plt
    T = 100000
    arr1 = [x for x in allArrivals if x < T]
    ys1 = [x for x in range(0, len(arr1))]
    ys1.append(len(arr1)) # point at t=100
    xs1 = [0] + arr1 # t = 100

    arr2 = [x for x in acceptedArrivals if x < T]
    ys2 = [x for x in range(0, len(arr2))]
    ys2.append(len(arr2)) # point at t=100
    xs2 = [0] + arr2 # t = 100

    plt.figure()
    plt.step(xs1, ys1, "b", where="post")
    plt.step(xs2, ys2, "r", where="post")
    #plt.figure()
    #plt.step(xs2, ys2, "b", where="post")
    plt.show()

