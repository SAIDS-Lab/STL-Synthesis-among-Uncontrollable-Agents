"""
In this file, we implement a class encoding a set of room temperatures from a distribution

Sources Used:
https://en.wikipedia.org/wiki/Newton%27s_law_of_cooling
"""

import random
import math
import matplotlib.pyplot as plt
from parameters import *
import json

# Set a seed.
random.seed(12)


class Room:
    """
    In this class, we implement an object encoding a set of random temperature traces from a given distribution following Newton's law of cooling

    T(t) = temp_final + (temp_initial - temp_final)e^(-rt)
    """

    def __init__(self, temp_final, r):
        """
        Constructor
        :param temp_final: The desired temperature of the room.
        :param r: The coefficient of heat transfer.
        """
        self.temp_final, self.r = temp_final, r
    
    def generate_temperatures(self, num_traces):
        """
        Generate temperature traces.
        :return: The generated traces.
        """
        return [self.__generate_one_trace() for _ in range(num_traces)]

    def __generate_one_trace(self):
        """
        Generate one trace.
        :return: The generated trace
        """
        temp_period_final = round(random.uniform(self.temp_final - starting_radius, self.temp_final + starting_radius), 2)
        temp_period_initial = round(random.uniform(temp_env - tem_env_radius, temp_env + tem_env_radius), 2)
        disturbed_r = round(random.uniform(self.r - temp_r_radius, self.r + temp_r_radius), 2)
        trace = []
        period = 0
        while period <= num_period:
            if period == 0:
                for t in range(0, samples_per_period+buffer):
                    temp = round(temp_period_final + (temp_period_initial - temp_period_final) * math.exp(-disturbed_r * t), 2)
                    trace.append(temp) 
            if period == 1:
                for t in range(0, samples_per_period):
                    temp = round(temp_period_final + (temp_period_initial - temp_period_final) * math.exp(-disturbed_r * t), 2)
                    trace.append(temp) 
            if period == num_period:
                for t in range(0, total_time%samples_per_period):
                    temp = round(temp_period_final + (temp_period_initial - temp_period_final) * math.exp(-disturbed_r * t), 2)
                    trace.append(temp) 
            period = period + 1
            temp_period_initial = temp
            temp_period_final = round(random.uniform(temp - in_room_radius, temp + in_room_radius), 2)
        return trace



def test_class():
    """
    Test the class implemented.
    """
    room = Room(temp_comf, temp_r)
    temperatures = room.generate_temperatures(10)

    for i in range(len(temperatures)):
        plt.plot([i for i in range(len(temperatures[i]))], temperatures[i], label = f"Temperature Trace {i}")
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.title("Testing Class Room")
    plt.show()
    

def collect_data():
    print("Collecting and preparing Data. \n")

    room2 = Room(temp_comf, temp_r)
    room2_temperatures = room2.generate_temperatures(num_traces)
    room3 = Room(temp_comf, temp_r)
    room3_temperatures = room3.generate_temperatures(num_traces)

    room2_train, room2_calib, room2_test = room2_temperatures[:train_num], room2_temperatures[train_num:train_num + calib_num], room2_temperatures[train_num + calib_num:]
    room3_train, room3_calib, room3_test = room3_temperatures[:train_num], room3_temperatures[train_num:train_num + calib_num], room3_temperatures[train_num + calib_num:]
    
    with open('case1 temperature/data_original/room2_train.json', 'w') as f:
        json.dump(room2_train, f)
    with open('case1 temperature/data_original/room2_calib.json', 'w') as f:
        json.dump(room2_calib, f)
    with open('case1 temperature/data_original/room2_test.json', 'w') as f:
        json.dump(room2_test, f)
    with open('case1 temperature/data_original/room3_train.json', 'w') as f:
        json.dump(room3_train, f)
    with open('case1 temperature/data_original/room3_calib.json', 'w') as f:
        json.dump(room3_calib, f)
    with open('case1 temperature/data_original/room3_test.json', 'w') as f:
        json.dump(room3_test, f)
    

    print("Thank you! We have prepared all the data and divided them into training, calibration, test data respectively. They are saved in the file called data. \n")


if __name__ == "__main__":
    # test_class()
    collect_data()
    