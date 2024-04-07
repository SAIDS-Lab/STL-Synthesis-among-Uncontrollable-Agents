
system_path = '/Users/xinyiyu/Library/CloudStorage/GoogleDrive-xyu07104@usc.edu/My Drive/7 - STL with CP/codes/new codes/case2 motion planning' 
import sys
sys.path.append(system_path)

from para_collectdata import *
from set_prob import *
from mpc import *
from parameters import *
import json


data_r2 = []  
count = 0
while count <= num_traces:
    print("Collecting data:", count)

    optimal_state_r2 = [[0.5, 0, 1, 0]]
    optimal_control_r2 = []

    flag = 1
    for k in range(total_time-1):
        if flag == 1:
            mpc = MPC(k)
            # print("--------------Time step:", k, "-----------------")
            flag, optimal_state_r2, optimal_control_r2 = mpc.solve(optimal_state_r2, optimal_control_r2)
        
    if flag == 1:
        count = count+1
        final_trace_r2 = []
        for i in range(total_time):
            final_trace_r2.append([optimal_state_r2[i][0], optimal_state_r2[i][2]])
        data_r2.append(final_trace_r2)
    else:
        print("it is infeasible in this case and we skip it.")


r2_train, r2_calib, r2_test = data_r2[:train_num], data_r2[train_num:train_num + calib_num], data_r2[train_num + calib_num:]


with open('data_original/r2_train.json', 'w') as f:
    json.dump(r2_train, f)
with open('data_original/r2_calib.json', 'w') as f:
    json.dump(r2_calib, f)
with open('data_original/r2_test.json', 'w') as f:
    json.dump(r2_test, f)



