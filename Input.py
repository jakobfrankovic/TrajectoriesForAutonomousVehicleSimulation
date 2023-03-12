import pandas as pd
import numpy as np
import scipy.stats
import math
import functools
import random


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
    def __init__(self, alpha, mu):
        self.alpha = alpha
        self.mu = mu

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
        
    def generate_number(self, lane_number, size):
        """
        We generate a number from distribution in assignment.

        lane_number ... in which lane do we want to generate (in our cas 1 or 2)
        size ... size of the sample
        """
        alpha = self.alpha[lane_number - 1]
        mu = self.mu[lane_number - 1]
        #we will create a partial function only because it is necessary that the function has only
        #   one parameter to use map. 
        partial_function = functools.partial(self.inverse_transform_sampling, alpha, mu)
        map_object = map(partial_function, np.zeros(size))
        return list(map_object)



input = Input("arrivals30.xlsx")
input.get_coefficients()
generator = Generate(alpha = input.alpha(), mu = input.mu())
array = generator.generate_number(1, 100000)
mean = np.mean(array)
mean

