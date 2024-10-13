import sys
import os
module_path = os.path.abspath(os.path.join('please replace it with your own path/STL-Synthesis-among-Uncontrollable-Agents/case2 motion planning'))
if module_path not in sys.path:
    sys.path.append(module_path)
from parameters import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle
from Step4_control.parameters_control import *


def PrintPaperFig(r1_trace_list_closed, r2_trace_list_closed, r1_trace_list_open, r2_trace_list_open):
    fig, ax = plt.subplots(1, 4, figsize=(15, 3.3))
    font_size = 14
    time_list = [0, 8, 14, 18]

    for i in range(4):
        k = time_list[i]
        path1 = []
        path2 = []
        for tau in range(total_time):
            if i == 0:
                path1.append([r1_trace_list_open[tau][0], r1_trace_list_open[tau][2]])
                path2.append([r2_trace_list_open[tau][0], r2_trace_list_open[tau][1]])
                c = c_open[str(k)]
            else:
                path1.append([r1_trace_list_closed[str(k)][tau][0], r1_trace_list_closed[str(k)][tau][2]])
                path2.append([r2_trace_list_closed[str(k)][tau][0], r2_trace_list_closed[str(k)][tau][1]])
                c = c_close[str(k)]
        path1 = np.array(path1)
        path2 = np.array(path2)

        ax[i].scatter(path1[ :, 0], path1[:, 1], color='red', s=10)
        ax[i].scatter(path2[ :, 0], path2[:, 1], color='blue', s=20)
        ax[i].scatter(path1[0, 0], path1[0, 1], color='red', s=20, marker = 's')
        ax[i].scatter(path2[0, 0], path2[0, 1], color='blue', s=20, marker = 's')
        
        a1 = Rectangle((mu1x[0], mu1y[0]), mu1x[1] - mu1x[0], mu1y[1] - mu1y[0], facecolor ="blue", alpha=0.1)
        a2 = Rectangle((mu2x[0], mu2y[0]), mu2x[1] - mu2x[0], mu2y[1] - mu2y[0], facecolor ="blue", alpha=0.1)
        a3 = Rectangle((mu3x[0], mu3y[0]), mu3x[1] - mu3x[0], mu3y[1] - mu3y[0], facecolor ="blue", alpha=0.1)
        a4 = Rectangle((mu4x[0], mu4y[0]), mu4x[1] - mu4x[0], mu4y[1] - mu4y[0], facecolor ="red", alpha=0.1)
        a5 = Rectangle((mu_obs1_x[0], mu_obs1_y[0]), mu_obs1_x[1] - mu_obs1_x[0], mu_obs1_y[1] - mu_obs1_y[0], facecolor ="grey", alpha=0.3, hatch='///////')
        a6 = Rectangle((mu_obs2_x[0], mu_obs2_y[0]), mu_obs2_x[1] - mu_obs2_x[0], mu_obs2_y[1] - mu_obs2_y[0], facecolor ="grey", alpha=0.3, hatch='///////')
        a7 = Rectangle((mu_obs3_x[0], mu_obs3_y[0]), mu_obs3_x[1] - mu_obs3_x[0], mu_obs3_y[1] - mu_obs3_y[0], facecolor ="grey", alpha=0.3, hatch='///////')
        ax[i].add_patch(a1)
        ax[i].add_patch(a2)
        ax[i].add_patch(a3)
        ax[i].add_patch(a4)
        ax[i].add_patch(a5)
        ax[i].add_patch(a6)
        ax[i].add_patch(a7)
        

        circle_list = []
        for tau in range(k+1, total_time):
            circle_list.append(Circle((path2[tau, 0], path2[tau, 1]), c[str(tau)], fill=False, color='blue', linestyle='dashed', alpha = 0.5))
            
        for circle in circle_list:
            ax[i].add_patch(circle)

        ax[i].plot(path1[ : k+1, 0], path1[:k+1, 1], linewidth=1, color = 'red', label = "Known states of $x$" if i == 0 else None)
        ax[i].plot(path1[ k:, 0], path1[k:, 1], linestyle=':', linewidth=1, color = 'red', label = "Predicted states of $x$" if i == 0 else None)
        ax[i].plot(path2[ : k+1, 0], path2[:k+1, 1], linewidth=1, color = 'blue', label = "Known states of $Y$" if i == 0 else None)
        ax[i].plot(path2[ k:, 0], path2[k:, 1], linestyle=':', linewidth=1, color = 'blue', label = "Predicted states of $Y$" if i == 0 else None)
    for i in range(4):
        ax[i].tick_params(axis='x', labelsize=10)
        ax[i].tick_params(axis='y', labelsize=10)
        ax[i].set_ylim(0,10)
        ax[i].set_xlim(0,10)

    ax[0].set_title('open-loop results', fontsize=font_size)
    ax[1].set_title('closed-loop results (k=6)', fontsize=font_size)
    ax[2].set_title('closed-loop results (k=12)', fontsize=font_size)
    ax[3].set_title('closed-loop results (k=18)', fontsize=font_size)

    
    fig.legend(fontsize = 12, loc='center right')
    fig.tight_layout(rect=[0, 0, 0.84, 1])
    plt.savefig("case2 motion planning/fig/case2_trace.pdf")




if __name__ == "__main__":
    with open("case2 motion planning/data_controlresults/r1_trace_list_closedloop.json") as f:
        r1_trace_list_closedloop = json.load(f)
    with open("case2 motion planning/data_controlresults/r2_trace_list_closedloop.json") as f:
        r2_trace_list_closedloop = json.load(f)
    with open("case2 motion planning/data_controlresults/r1_trace_list_openloop.json") as f:
        r1_trace_list_openloop = json.load(f)
    with open("case2 motion planning/data_controlresults/r2_trace_list_openloop.json") as f:
        r2_trace_list_openloop = json.load(f)

    index  = 0
    PrintPaperFig(r1_trace_list_closedloop[str(index)], r2_trace_list_closedloop[str(index)], r1_trace_list_openloop[str(index)], r2_trace_list_openloop[str(index)])
    