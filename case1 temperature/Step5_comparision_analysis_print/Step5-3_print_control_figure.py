import sys
import os
module_path = os.path.abspath(os.path.join('/Users/xinyiyu/Library/CloudStorage/GoogleDrive-xyu07104@usc.edu/My Drive/7 - STL with CP/auto/STL-Synthesis-among-Uncontrollable-Agents/case1 temperature'))
if module_path not in sys.path:
    sys.path.append(module_path)
from Step4_control.parameters_control import *
import matplotlib.pyplot as plt
import numpy as np


def PrintPaperFig(mode, r1_trace_list_closed, r2_trace_list_closed, r3_trace_list_closed, r1_trace_list_open, r2_trace_list_open, r3_trace_list_open):
    fig, ax = plt.subplots(1, 4, figsize=(15, 3))
    font_size = 14

    # time_list = [0, 8, 20, 26]
    time_list = [0, 8, 16, 26]
    for i in range(4):
        k = time_list[i]
        k_known = np.arange(k+1)
        k_unknown = np.arange(k, total_time)

        if i == 0:
            r1_trace_list = r1_trace_list_open
            r2_trace_list = r2_trace_list_open
            r3_trace_list = r3_trace_list_open
            c_room2 = c_open_room2[str(k)]
            c_room3 = c_open_room3[str(k)]
        else:
            r1_trace_list = r1_trace_list_closed[str(k)]
            r2_trace_list = r2_trace_list_closed[str(k)]
            r3_trace_list = r3_trace_list_closed[str(k)]
            c_room2 = c_close_room2[str(k)]
            c_room3 = c_close_room3[str(k)]

        r2_temp_pred_upper = [r2_trace_list[k]]
        r2_temp_pred_lower = [r2_trace_list[k]]
        r3_temp_pred_upper = [r3_trace_list[k]]
        r3_temp_pred_lower = [r3_trace_list[k]]
        for tau in range(k+1, total_time):
            r2_temp_pred_upper.append(r2_trace_list[tau] + c_room2[str(tau)])
            r2_temp_pred_lower.append(r2_trace_list[tau] - c_room2[str(tau)])
            r3_temp_pred_upper.append(r3_trace_list[tau] + c_room3[str(tau)])
            r3_temp_pred_lower.append(r3_trace_list[tau] - c_room3[str(tau)])

        ax[i].plot(k_unknown, r2_temp_pred_upper, alpha=0)
        ax[i].plot(k_unknown, r2_temp_pred_lower, alpha=0)
        ax[i].fill_between(k_unknown, r2_temp_pred_lower, r2_temp_pred_upper, where=np.array(r2_temp_pred_upper) > np.array(r2_temp_pred_lower), interpolate=True, color='red', alpha=0.1)
        ax[i].plot(k_unknown, r3_temp_pred_upper, alpha=0)
        ax[i].plot(k_unknown, r3_temp_pred_lower, alpha=0)
        ax[i].fill_between(k_unknown, r3_temp_pred_lower, r3_temp_pred_upper, where=np.array(r3_temp_pred_upper) > np.array(r3_temp_pred_lower), interpolate=True, color='blue', alpha=0.1)

        ax[i].plot(k_known, r1_trace_list[:k+1], linewidth=1, color = 'black', label = "Known states of x" if i == 0 else None)
        ax[i].plot(k_known, r2_trace_list[:k+1], linewidth=1, color = 'red', label = "Known states of $Y_{r2}$" if i == 0 else None)
        ax[i].plot(k_known, r3_trace_list[:k+1], linewidth=1, color = 'blue', label = "Known states of $Y_{r3}$" if i == 0 else None)
        ax[i].plot(k_unknown, r1_trace_list[k:], linestyle=':', linewidth=1, color = 'black', label = "predicted states of x" if i == 0 else None)
        ax[i].plot(k_unknown, r2_trace_list[k:], linestyle=':', linewidth=1, color = 'red', label = "Predicted states of $Y_{r2}$" if i == 0 else None)
        ax[i].plot(k_unknown, r3_trace_list[k:], linestyle=':', linewidth=1, color = 'blue', label = "Predicted states of $Y_{r3}$" if i == 0 else None)
    for i in range(4):
        ax[i].tick_params(axis='x', labelsize=10)
        ax[i].tick_params(axis='y', labelsize=10)
        ax[i].set_ylim(13,28)

    ax[0].set_title('open-loop results', fontsize=font_size)
    ax[1].set_title('closed-loop results (k=8)', fontsize=font_size)
    ax[2].set_title('closed-loop results (k=16)', fontsize=font_size)
    ax[3].set_title('closed-loop results (k=26)', fontsize=font_size)

    
    fig.legend(fontsize = 12, loc='center right')
    fig.tight_layout(rect=[0, 0, 0.83, 1])
    # plt.show()
    plt.savefig(f"case1 temperature/fig/case1_trace_{mode}.pdf")
    





if __name__ == "__main__":
    mode = ["qualitative", "quantitative"]
    for i in range(2):
        with open(f"case1 temperature/data_controlresults/r1_trace_list_closedloop_{mode[i]}.json") as f:
            r1_trace_list_closedloop = json.load(f)
        with open(f"case1 temperature/data_controlresults/r2_trace_list_closedloop_{mode[i]}.json") as f:
            r2_trace_list_closedloop = json.load(f)
        with open(f"case1 temperature/data_controlresults/r3_trace_list_closedloop_{mode[i]}.json") as f:
            r3_trace_list_closedloop = json.load(f)
        with open(f"case1 temperature/data_controlresults/r1_trace_list_openloop_{mode[i]}.json") as f:
            r1_trace_list_openloop = json.load(f)
        with open(f"case1 temperature/data_controlresults/r2_trace_list_openloop_{mode[i]}.json") as f:
            r2_trace_list_openloop = json.load(f)
        with open(f"case1 temperature/data_controlresults/r3_trace_list_openloop_{mode[i]}.json") as f:
            r3_trace_list_openloop = json.load(f)


        index  = 7
        PrintPaperFig(mode[i], r1_trace_list_closedloop[str(index)], r2_trace_list_closedloop[str(index)], r3_trace_list_closedloop[str(index)], r1_trace_list_openloop[str(index)], r2_trace_list_openloop[str(index)], r3_trace_list_openloop[str(index)])
    