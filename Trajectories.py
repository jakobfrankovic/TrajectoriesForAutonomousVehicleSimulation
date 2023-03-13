import matplotlib.pyplot as plt
import math
class Trajectories:
    def __init__(self, arrival_departure):
        """ 
        arrival_departure contains tuples of (arrival, departure)
        """
        self.arrival_departure = arrival_departure

    def get_trajectory_data(self, density, vm = 13, am = 3, x0 = -300):
        """
        here we create matrix_all that contains tables. Each table contains tuples that state the y and x coordinate (i.e. (distance to crossing, time))
        """
        table_arrival_departure = self.arrival_departure
        tf = table_arrival_departure[0][1]
        tf_previous = tf
        #contains table_xt for multiple cars
        matrix_all = [] 
        for arrival, departure in table_arrival_departure:

            #we set the arrival in real world scenario
            arrival = arrival - abs(x0)/vm

            #time begins running at the arrival into the control region
            t = arrival

            #we will use table_xt for each trajectory. Later we will append it to matrix_all that contains multiple trajectory tables
            table_xt = [] 

            #start of crossing the intersection is equal to the departure
            tf = departure
            if tf - tf_previous == 1:
                pass #tfull stays the same for the whole platoon
            else:
                tfull = tf
            
            #because the given equations in the assignment want us to start from t = 0, we need to recalibrate all other used constants too
            tfull_local = abs(tfull - arrival)
            tf_local = abs(tf - arrival)
            
            t_local = 0
            
            #distance if a vehicle stops for 0 seconds
            L = vm*(tf_local - vm/am) 

            if L >= abs(x0):
                #use of equations stated in the assignment if the vehicle has to stop
                tacc = tfull_local - vm/am
                tstop = tacc - (tf_local - vm/am - abs(x0)/vm)
                tdec = tstop - vm/am
                if departure > 28:
                    dummy = 0
                while t_local <= tf_local:
                    if t > 28:
                        dummy = 0
                    if tfull_local <= t_local and t_local <= tf_local:
                        table_xt.append(((t_local-tf_local)*vm, t))
                    elif tacc <= t_local and t_local <= tfull_local:
                        table_xt.append(((tfull_local-tf_local)*vm - vm**2/(2*am) + (am/2)*(t_local - tacc)**2, t))
                    elif tstop <= t_local and t_local <= tacc:
                        table_xt.append(((tfull_local - tf_local)*vm - vm**2/(2*am), t))
                    elif tdec <= t_local and t_local <= tstop:
                        table_xt.append(((tfull_local - tf_local)*vm - vm**2/(2*am) - (am/2)*(t_local-tstop)**2, t))
                    elif 0 <= t_local and t_local <= tdec:
                        table_xt.append((x0 + vm*t_local, t))
                    t += density
                    t_local += density  

            else:
                #use of equations stated in the assignment if the vehicle does not have to stop
                tacc = tfull_local - math.sqrt((tf_local*vm - abs(x0))/am)
                tstop = tacc
                tdec = tacc - math.sqrt((tf_local*vm - abs(x0))/am)
                while t_local <= tf_local:
                    if tfull_local <= t_local and t_local <= tf_local:
                        table_xt.append(((t_local - tf_local)*vm, t))
                    elif tacc <= t_local and t_local <= tfull_local:
                        table_xt.append(((t_local - tf_local)*vm + am/2*(t_local - tfull_local)**2, t))
                    elif tdec <= t_local and t_local <= tacc:
                        table_xt.append((x0 + vm*t_local - (am/2)*(t_local - tdec)**2, t))
                    elif 0 <= t_local and t_local <= tdec:
                        table_xt.append((x0 + vm*t_local, t))
                    t += density
                    t_local += density

            #matrix_all contains data for multiple trajectories
            matrix_all.append(table_xt)

            tf_previous = tf
        #we set trajectory data accessable by the object
        self.matrix = matrix_all

    def plot_down_to_up(self):
        """
        vehicles start at -300m
        """
        matrix = self.matrix
        for i, inner_list in enumerate(matrix):
            #Unpack the tuples into separate lists for x and y values
            y_values, x_values = zip(*inner_list)
            #Plot the data for this inner list
            x_values = [x for x in x_values if x > 0]
            y_values = y_values[len(y_values) - len(x_values): ]
            plt.plot(x_values, y_values, label=f'Car: {i+1}', color = "r")

    def plot_up_to_down(self):
        """
        vehicles start at +300m
        """
        matrix = self.matrix
        for i, inner_list in enumerate(matrix):
            #Unpack the tuples into separate lists for x and y values
            y_values, x_values = zip(*inner_list)
            #Plot the data for this inner list
            x_values = [x for x in x_values if x > 0]
            y_values = y_values[len(y_values) - len(x_values): ]
            y_values = [-y for y in y_values] 
            plt.plot(x_values, y_values, label=f'Car: {i+1}', color = "r")



with open("sampleOutput.txt", "r") as file:
    # Read the contents of the file into a list of lines
    lines = file.readlines()

# Iterate over each line and split it into three columns
result1 = []
result2 = []
for line in lines:
    column1, column2, column3 = line.split(" ")
    # Do something with the columns
    if column1 == "1":
        # Append a tuple of column2 and column3 to the result list
        result1.append((column2, column3))
    elif column1 == "0":
        result2.append((column2, column3))

result1 = [(float(x[0]), float(x[1])) for x in result1]

result2 = [(float(x[0]), float(x[1])) for x in result2]

trajectory_1 = Trajectories(result1)
trajectory_1.get_trajectory_data(density=0.1)
trajectory_1.plot_up_to_down()




#trajectory_2 = Trajectories([(24.205-10, 30.8-10), (26.802-10, 31.8-10), (30.893-10, 32.8-10), (31.893-10, 33.8-10), (32.893-10, 34.8-10), (35.179-10, 35.8-10), (36.8-10, 36.8-10)])
trajectory_2 = Trajectories(result2)
#trajectory_2 = Trajectories([(24.205, 30.8), (26.802, 31.8), (30.893, 32.8)])
trajectory_2.get_trajectory_data(density=0.1)
trajectory_2.plot_down_to_up()
plt.show()
            