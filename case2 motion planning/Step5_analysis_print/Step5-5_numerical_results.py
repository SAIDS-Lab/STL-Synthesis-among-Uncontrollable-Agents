import sys
import os
module_path = os.path.abspath(os.path.join('please replace it with your own path/STL-Synthesis-among-Uncontrollable-Agents/case2 motion planning'))
if module_path not in sys.path:
    sys.path.append(module_path)
from Step4_control.parameters_control import *
import numpy as np
import json

with open(f"case2 motion planning/data_pre_control/r2_ground.json") as f:
    r2_trace_list = json.load(f)


def comp_robust_openloop(r1_trace_list, r2_trace_list):
    each_robustness = []
    for key, value in r1_trace_list.items():
        if value:
            G_mu1 = min(min(r2_trace_list[int(key)][i][0], 2 - r2_trace_list[int(key)][i][0], r2_trace_list[int(key)][i][1]-4, 6-r2_trace_list[int(key)][i][1]) for i in range(4,7))
            G_mu2 = min(min(r2_trace_list[int(key)][i][0]-3.5, 6.5 - r2_trace_list[int(key)][i][0], r2_trace_list[int(key)][i][1]-8, 10-r2_trace_list[int(key)][i][1]) for i in range(9,13))
            FG = max(min(r2_trace_list[int(key)][i+j][0]-8.5, 10 - r2_trace_list[int(key)][i+j][0], r2_trace_list[int(key)][i+j][1], 2-r2_trace_list[int(key)][i+j][1], r1_trace_list[key][i+j][0]-7, 8.5 - r1_trace_list[key][i+j][0], r1_trace_list[key][i+j][2], 2-r1_trace_list[key][i+j][2]) for j in range(3) for i in range(16,19))
            G_close = min(D - min(r2_trace_list[int(key)][i][0] - r1_trace_list[key][i][0], r1_trace_list[key][i][0] - r2_trace_list[int(key)][i][0], r2_trace_list[int(key)][i][1] - r1_trace_list[key][i][2], r1_trace_list[key][i][2] - r2_trace_list[int(key)][i][1]) for i in range(21))
            G_obs1 = min(min(max(1.6-r1_trace_list[key][i][0], r1_trace_list[key][i][0]-2.6, 2- r1_trace_list[key][i][2], r1_trace_list[key][i][2]-3), max(8.3-r1_trace_list[key][i][0], r1_trace_list[key][i][0]-9.3, 6.5- r1_trace_list[key][i][2], r1_trace_list[key][i][2]-7.5), max(5.7-r1_trace_list[key][i][0], r1_trace_list[key][i][0]-6.7, 2.7- r1_trace_list[key][i][2], r1_trace_list[key][i][2]-3.7)) for i in range(21))
            G_obs2 = min(min(max(1.6-r2_trace_list[int(key)][i][0], r2_trace_list[int(key)][i][0]-2.6, 2- r2_trace_list[int(key)][i][1], r2_trace_list[int(key)][i][1]-3), max(8.3-r2_trace_list[int(key)][i][0], r2_trace_list[int(key)][i][0]-9.3, 6.5- r2_trace_list[int(key)][i][1], r2_trace_list[int(key)][i][1]-7.5), max(5.7-r2_trace_list[int(key)][i][0], r2_trace_list[int(key)][i][0]-6.7, 2.7- r2_trace_list[int(key)][i][1], r2_trace_list[int(key)][i][1]-3.7)) for i in range(21))
            each_robustness.append(min(G_mu1, G_mu2, FG, G_close, G_obs1, G_obs2))
    return each_robustness

def comp_robust_closedloop(r1_trace_list, r2_trace_list):
    each_robustness = []
    for key, value in r1_trace_list.items():
        if len(value) >= 20:
            G_mu1 = min(min(r2_trace_list[int(key)][i][0], 2 - r2_trace_list[int(key)][i][0], r2_trace_list[int(key)][i][1]-4, 6-r2_trace_list[int(key)][i][1]) for i in range(4,7))
            G_mu2 = min(min(r2_trace_list[int(key)][i][0]-3.5, 6.5 - r2_trace_list[int(key)][i][0], r2_trace_list[int(key)][i][1]-8, 10-r2_trace_list[int(key)][i][1]) for i in range(9,13))
            FG = max(min(r2_trace_list[int(key)][i+j][0]-8.5, 10 - r2_trace_list[int(key)][i+j][0], r2_trace_list[int(key)][i+j][1], 2-r2_trace_list[int(key)][i+j][1], r1_trace_list[key][str(19)][i+j][0]-7, 8.5 - r1_trace_list[key][str(19)][i+j][0], r1_trace_list[key][str(19)][i+j][2], 2-r1_trace_list[key][str(19)][i+j][2]) for j in range(3) for i in range(16,19))
            G_close = min(D - min(r2_trace_list[int(key)][i][0] - r1_trace_list[key][str(19)][i][0], r1_trace_list[key][str(19)][i][0] - r2_trace_list[int(key)][i][0], r2_trace_list[int(key)][i][1] - r1_trace_list[key][str(19)][i][2], r1_trace_list[key][str(19)][i][2] - r2_trace_list[int(key)][i][1]) for i in range(21))
            G_obs1 = min(min(max(1.6-r1_trace_list[key][str(19)][i][0], r1_trace_list[key][str(19)][i][0]-2.6, 2- r1_trace_list[key][str(19)][i][2], r1_trace_list[key][str(19)][i][2]-3), max(8.3-r1_trace_list[key][str(19)][i][0], r1_trace_list[key][str(19)][i][0]-9.3, 6.5- r1_trace_list[key][str(19)][i][2], r1_trace_list[key][str(19)][i][2]-7.5), max(5.7-r1_trace_list[key][str(19)][i][0], r1_trace_list[key][str(19)][i][0]-6.7, 2.7- r1_trace_list[key][str(19)][i][2], r1_trace_list[key][str(19)][i][2]-3.7)) for i in range(21))
            G_obs2 = min(min(max(1.6-r2_trace_list[int(key)][i][0], r2_trace_list[int(key)][i][0]-2.6, 2- r2_trace_list[int(key)][i][1], r2_trace_list[int(key)][i][1]-3), max(8.3-r2_trace_list[int(key)][i][0], r2_trace_list[int(key)][i][0]-9.3, 6.5- r2_trace_list[int(key)][i][1], r2_trace_list[int(key)][i][1]-7.5), max(5.7-r2_trace_list[int(key)][i][0], r2_trace_list[int(key)][i][0]-6.7, 2.7- r2_trace_list[int(key)][i][1], r2_trace_list[int(key)][i][1]-3.7)) for i in range(21))
            each_robustness.append(min(G_mu1, G_mu2, FG, G_close, G_obs1, G_obs2))
    return each_robustness


def analysis():

    with open(f"case2 motion planning/data_controlresults/r1_trace_list_openloop.json") as f:
        r1_trace_list_openloop = json.load(f)
    with open(f"case2 motion planning/data_controlresults/r1_trace_list_closedloop.json") as f:
        r1_trace_list_closedloop = json.load(f)
    with open(f"case2 motion planning/data_controlresults/time_openloop.json") as f:
        time_openloop = json.load(f)
    with open(f"case2 motion planning/data_controlresults/time_closedloop.json") as f:
        time_closedloop = json.load(f)

    # open loop
    num_feasibility_openloop = sum(1 for value in time_openloop.values() if value)
    average_time_openloop = sum(value for value in time_openloop.values() if value) / num_feasibility_openloop
    each_robustness = comp_robust_openloop(r1_trace_list_openloop, r2_trace_list)
    average_robustness_openloop = np.mean(each_robustness)
    num_task_sat_openloop = len([i for i in each_robustness if i >= 0]) 
    print("Here is the result of open loop analysis:")
    print("number of feasible cases: ", num_feasibility_openloop)
    print("average computation time: ", average_time_openloop)
    print("average robustness: ", average_robustness_openloop)
    print("number of satisfying the task: ", num_task_sat_openloop)
    print("\n")

    # closed loop
    num_initial_feasibility_closedloop = len([1 for value in time_closedloop.values() if len(value) >= 1])
    num_recursive_feasibility_closedloop = len([1 for value in time_closedloop.values() if len(value) >= 32])
    each_time_sum = []
    for inner_dict in time_closedloop.values():
        if len(inner_dict) >= 20:
            each_time_sum.append(sum(inner_dict.values()))
    average_time_closedloop = np.mean(each_time_sum)
    each_robustness = comp_robust_closedloop(r1_trace_list_closedloop, r2_trace_list)
    average_robustness_closedloop = np.mean(each_robustness)
    num_task_sat_closedloop = len([i for i in each_robustness if i >= 0])

    print("Here is the result of closed loop analysis:")
    print("number of initial feasible cases: ", num_initial_feasibility_closedloop)
    print("number of recursive feasible cases: ", num_recursive_feasibility_closedloop)
    print("average total computation time: ", average_time_closedloop)
    print("average robustness: ", average_robustness_closedloop)
    print("number of satisfying the task: ", num_task_sat_closedloop)
    print("\n")


if __name__ == "__main__":
    print("Qualitative analysis:")
    analysis()

    