import sys
import os
module_path = os.path.abspath(os.path.join('/Users/xinyiyu/Library/CloudStorage/GoogleDrive-xyu07104@usc.edu/My Drive/7 - STL with CP/auto/STL-Synthesis-among-Uncontrollable-Agents/case2 motion planning'))
if module_path not in sys.path:
    sys.path.append(module_path)
import json
import numpy as np
import matplotlib.pyplot as plt
from parameters import *
from Step4_control.parameters_control import *
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle, Circle

with open("case2 motion planning/data_controlresults/r1_trace_list_closedloop.json") as f:
    r1_trace_list_closedloop = json.load(f)
with open("case2 motion planning/data_controlresults/r2_trace_list_closedloop.json") as f:
    r2_trace_list_closedloop = json.load(f)

index = 0
r1_trace_list = r1_trace_list_closedloop[str(index)]
r2_trace_list = r2_trace_list_closedloop[str(index)]

def update(frame):
    ax.clear()
    k = time_list[frame]
    path1 = np.array([[r1_trace_list[str(k)][tau][0], r1_trace_list[str(k)][tau][2]] for tau in range(total_time)])
    path2 = np.array([[r2_trace_list[str(k)][tau][0], r2_trace_list[str(k)][tau][1]] for tau in range(total_time)])

    ax.scatter(path1[:, 0], path1[:, 1], color='red', s=10)
    ax.scatter(path2[:, 0], path2[:, 1], color='blue', s=20)
    ax.scatter(path1[0, 0], path1[0, 1], color='red', s=20, marker='s')
    ax.scatter(path2[0, 0], path2[0, 1], color='blue', s=20, marker='s')
    
    a1 = Rectangle((mu1x[0], mu1y[0]), mu1x[1] - mu1x[0], mu1y[1] - mu1y[0], facecolor ="blue", alpha=0.1)
    a2 = Rectangle((mu2x[0], mu2y[0]), mu2x[1] - mu2x[0], mu2y[1] - mu2y[0], facecolor ="blue", alpha=0.1)
    a3 = Rectangle((mu3x[0], mu3y[0]), mu3x[1] - mu3x[0], mu3y[1] - mu3y[0], facecolor ="blue", alpha=0.1)
    a4 = Rectangle((mu4x[0], mu4y[0]), mu4x[1] - mu4x[0], mu4y[1] - mu4y[0], facecolor ="red", alpha=0.1)
    a5 = Rectangle((mu_obs1_x[0], mu_obs1_y[0]), mu_obs1_x[1] - mu_obs1_x[0], mu_obs1_y[1] - mu_obs1_y[0], facecolor ="grey", alpha=0.3, hatch='///////')
    a6 = Rectangle((mu_obs2_x[0], mu_obs2_y[0]), mu_obs2_x[1] - mu_obs2_x[0], mu_obs2_y[1] - mu_obs2_y[0], facecolor ="grey", alpha=0.3, hatch='///////')
    a7 = Rectangle((mu_obs3_x[0], mu_obs3_y[0]), mu_obs3_x[1] - mu_obs3_x[0], mu_obs3_y[1] - mu_obs3_y[0], facecolor ="grey", alpha=0.3, hatch='///////')
    ax.add_patch(a1)
    ax.add_patch(a2)
    ax.add_patch(a3)
    ax.add_patch(a4)
    ax.add_patch(a5)
    ax.add_patch(a6)
    ax.add_patch(a7)
        
    circle_list = []
    for tau in range(k+1, total_time):
        circle_list.append(Circle((path2[tau, 0], path2[tau, 1]), c_close[str(k)][str(tau)], fill=False, color='blue', linestyle='dashed', alpha = 0.5))
    for circle in circle_list:
        ax.add_patch(circle)

    ax.plot(path1[:k+1, 0], path1[:k+1, 1], linewidth=1, color='red')
    ax.plot(path1[k:, 0], path1[k:, 1], linestyle=':', linewidth=1, color='red')
    ax.plot(path2[:k+1, 0], path2[:k+1, 1], linewidth=1, color='blue')
    ax.plot(path2[k:, 0], path2[k:, 1], linestyle=':', linewidth=1, color='blue')
    ax.set_ylim(0, 10)
    ax.set_xlim(0, 10)
    ax.set_title(f'closed-loop results (k={k})', fontsize=font_size)

fig, ax = plt.subplots(figsize=(7, 6))
font_size = 14
time_list = list(range(total_time-1))

ani = FuncAnimation(fig, update, frames=len(time_list), repeat=True)

ani.save('case2 motion planning/fig/case2.mp4', fps=2, extra_args=['-vcodec', 'libx264'])