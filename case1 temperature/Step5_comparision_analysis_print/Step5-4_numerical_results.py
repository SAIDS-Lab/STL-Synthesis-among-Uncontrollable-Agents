import sys
import os
module_path = os.path.abspath(os.path.join('please replace it with your own path/STL-Synthesis-among-Uncontrollable-Agents/case1 temperature'))
if module_path not in sys.path:
    sys.path.append(module_path)
from Step4_control.parameters_control import *
import numpy as np
import json

with open(f"case1 temperature/data_pre_control/room2_ground.json") as f:
    r2_trace_list = json.load(f)
with open(f"case1 temperature/data_pre_control/room3_ground.json") as f:
    r3_trace_list = json.load(f)

def comp_robust_openloop(r1_trace_list, r2_trace_list, r3_trace_list):
    each_robustness = []
    for key, value in r1_trace_list.items():
        if value:
            mu1 = [min(bound-r1_trace_list[key][i] + r2_trace_list[int(key)][i], bound + r1_trace_list[key][i] - r2_trace_list[int(key)][i], bound-r1_trace_list[key][i] + r3_trace_list[int(key)][i], bound + r1_trace_list[key][i] - r3_trace_list[int(key)][i]) for i in range(len(r1_trace_list[key]))]
            Gmu1 = [min(mu1[i+j] for j in range(G_len)) for i in range(F_len)]
            FGmu1 = max(Gmu1)
            each_robustness.append(FGmu1)
            
    return each_robustness

def comp_robust_closedloop(r1_trace_list, r2_trace_list, r3_trace_list):
    each_robustness = []
    for key, value in r1_trace_list.items():
        if len(value) >= 32:
            mu1 = [min(bound-r1_trace_list[key][str(31)][i] + r2_trace_list[int(key)][i], bound + r1_trace_list[key][str(31)][i] - r2_trace_list[int(key)][i], bound-r1_trace_list[key][str(31)][i] + r3_trace_list[int(key)][i], bound + r1_trace_list[key][str(31)][i] - r3_trace_list[int(key)][i]) for i in range(len(r1_trace_list[key][str(31)]))]
            Gmu1 = [min(mu1[i+j] for j in range(G_len)) for i in range(F_len)]
            FGmu1 = max(Gmu1)
            each_robustness.append(FGmu1)
            
    return each_robustness



def analysis(mode):

    with open(f"case1 temperature/data_controlresults/r1_trace_list_openloop_{mode}.json") as f:
        r1_trace_list_openloop = json.load(f)
    with open(f"case1 temperature/data_controlresults/r1_trace_list_closedloop_{mode}.json") as f:
        r1_trace_list_closedloop = json.load(f)
    with open(f"case1 temperature/data_controlresults/time_openloop_{mode}.json") as f:
        time_openloop = json.load(f)
    with open(f"case1 temperature/data_controlresults/time_closedloop_{mode}.json") as f:
        time_closedloop = json.load(f)

    # open loop
    num_feasibility_openloop = sum(1 for value in time_openloop.values() if value)
    average_time_openloop = sum(value for value in time_openloop.values() if value) / num_feasibility_openloop
    each_robustness = comp_robust_openloop(r1_trace_list_openloop, r2_trace_list, r3_trace_list)
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
        if len(inner_dict) >= 32:
            each_time_sum.append(sum(inner_dict.values()))
    average_time_closedloop = np.mean(each_time_sum)
    each_robustness = comp_robust_closedloop(r1_trace_list_closedloop, r2_trace_list, r3_trace_list)
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
    analysis("qualitative")
    print("\n")
   

    print("Quantitative analysis:")
    analysis("quantitative")
    