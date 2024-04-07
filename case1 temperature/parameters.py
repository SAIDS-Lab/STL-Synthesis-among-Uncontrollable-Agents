"""
Authors: Xinyi Yu, Yiqi Zhao

In this file, we set all the parameters we will use in this project

"""


# Define Hyperparameters Here:
delta = 0.15 # The expected miscoverage rate.
# num_traces = 1500 # Number of traces sampled for each room.
train_num = 500 # Number of training traces for each room.
calib_num = 500 # Number of calibration traces for each room.
test_num = 1000 # Number of test traces for each room.
num_traces = train_num + calib_num + test_num




# fixed parameters in class Room
temp_env = -5           # environmental temperature
tem_env_radius = 3      # the uncertainty radius of the environmental temperature
starting_radius = 2.8   # uncertainty radius of temperature adjustment upon arrival
in_room_radius = 1.5    # uncertainty radius of temperature adjustment after entering the room
temp_r_radius = 0.03    # the uncertainty radius of different ACs

# adjustable parameters in class Room
temp_comf = 22          # comfortable temperature 
temp_r = 0.3            # the parameter in Newton's law of cooling that determines the speed of the temperature changing
sampling_time = 2       # units: 2 mins
period_time = 30        # units: 30 mins
samples_per_period = int(period_time/sampling_time)   # units: steps
num_period = 2          # in total, it is 30 steps (60 mins)
total_time = num_period*samples_per_period + 1 + 2
buffer = 6
len_seq = total_time + buffer


inp_dim = 1
out_dim = 1
mid_dim = 10
mid_layers = 1
mod_dir = '.'





