"""
In this file, we compare the LCP-based CP algorithm with our methods for open loop results.
"""

import json
import sys
import os
module_path = os.path.abspath(os.path.join('/Users/xinyiyu/Library/CloudStorage/GoogleDrive-xyu07104@usc.edu/My Drive/7 - STL with CP/auto/STL-Synthesis-among-Uncontrollable-Agents/case1 temperature'))
if module_path not in sys.path:
    sys.path.append(module_path)
from parameters import *
from Step4_control.parameters_control import *
import casadi as ca
import numpy as np
import time
import matplotlib.pyplot as plt


def extract_nonconformity_scores(j, room2_calib, room2_calib_prediction, room3_calib, room3_calib_prediction):
    r_2, r_3 = [], []
    for tau in range(1, total_time):
        ground2, ground3 = room2_calib[j][buffer + tau], room3_calib[j][buffer + tau]
        prediction2, prediction3 = room2_calib_prediction[str(0)][j][tau - 1], room3_calib_prediction[str(0)][j][
            tau - 1]
        r_2.append(abs(ground2 - prediction2))
        r_3.append(abs(ground3 - prediction3))
    r_2.extend(r_3)
    return r_2


def organize_nonconformity_scores(room2_calib, room2_calib_prediction, room3_calib, room3_calib_prediction, optimization_size):
    """
    In this function, we organize the nonconformity scores and split the data in half to implement the LCP algorithm.
    """
    nonconformity_scores_opt = []
    for j in range(optimization_size):
        nonconformity_scores_opt.append(extract_nonconformity_scores(j, room2_calib, room2_calib_prediction, room3_calib, room3_calib_prediction))
    nonconformity_scores_cp = []
    for j in range(optimization_size, len(room2_calib)):
        nonconformity_scores_cp.append(extract_nonconformity_scores(j, room2_calib, room2_calib_prediction, room3_calib, room3_calib_prediction))
    print("Size of n1 (calibration data size for solving the optimization):", len(nonconformity_scores_opt))
    print("Size of n2 (calibrationd data size for CP):", len(nonconformity_scores_cp))
    return nonconformity_scores_opt, nonconformity_scores_cp


def compute_alphas_lcp(nonconformity_scores_opt):
    """
    In this function we solve the LCP for the alphas.
    """
    T = len(nonconformity_scores_opt[0])
    n1 = len(nonconformity_scores_opt)
    # Model initialization.
    opti = ca.Opti()
    # Variable definitions.
    q = opti.variable()
    alphas = [opti.variable() for _ in range(T)]
    Rs = [opti.variable() for _ in range(n1)]
    u_plus = [opti.variable() for _ in range(n1)]
    u_minus = [opti.variable() for _ in range(n1)]
    e_plus = [opti.variable() for _ in range(n1)]
    e_minus = [opti.variable() for _ in range(n1)]
    v = [opti.variable() for _ in range(n1)]
    # Objective function.
    opti.minimize(q)
    # Constraints.
    constraints = []
    for i in range(n1):
        for t in range(T):
            constraints.append(Rs[i] >= alphas[t] * nonconformity_scores_opt[i][t]) # Constraint 8b.
        constraints.append((1 - delta) - u_plus[i] + v[i] == 0) # Constraint 17a.
        constraints.append(delta - u_minus[i] - v[i] == 0) # Constraint 17b.
        constraints.append(u_plus[i] * e_plus[i] == 0) # Constraint 17d.
        constraints.append(u_minus[i] * e_minus[i] == 0) # Constraint 17e.
        constraints.append(e_plus[i] >= 0) # Constraint 17f.
        constraints.append(e_minus[i] >= 0) # Constraint 17g.
        constraints.append(e_plus[i] + q - e_minus[i] - Rs[i] == 0) # Constraint 17h.
        constraints.append(u_plus[i] >= 0) # Constraint 17i.
        constraints.append(u_minus[i] >= 0) # Constraint 17j.
    constraints.append(sum(v) == 0) # Constraint 17c.
    constraints.append(sum(alphas) == 1) # Constraint 6c.
    for t in range(T):
        constraints.append(alphas[t] >= 0) # Constraint 6d.
    # Add constraints.
    for constraint in constraints:
        opti.subject_to(constraint)
    # Solve.
    opti.solver('ipopt', {'print_time': False, 'ipopt.print_level': 0})
    sol = opti.solve()
    # Organize solutions.
    return [sol.value(alphas[t]) for t in range(T)]


def perform_cp(alphas_opt, nonconformity_scores_cp):
    normalized = []
    for i in range(len(nonconformity_scores_cp)):
        inidividal_scores = [alphas_opt[t] * nonconformity_scores_cp[i][t] for t in range(len(alphas_opt))]
        normalized.append(max(inidividal_scores))
    p = int(np.ceil((len(normalized) + 1) * (1 - delta)))
    normalized.append(float("inf"))
    normalized.sort()
    c_open = normalized[p - 1]
    return c_open


def compute_sigmas(data, data_predictions):
    sigmas_open = dict()
    sigmas_open[0] = dict()
    for tau in range(1, total_time):
        residuals = []
        for j in range(len(data)):
            ground = data[j][tau + buffer]
            predicted = data_predictions[str(0)][j][tau - 1]
            residuals.append(abs(ground - predicted))
        sigmas_open[0][tau] = max(residuals)
    return sigmas_open


def compute_quantiles_ours(delta, room2_calib, room2_calib_prediction, room3_calib, room3_calib_prediction, room2_sigmas, room3_sigmas):
    r_open_nonconformity_list = []
    for j in range(len(room2_calib)):
        r = []
        for tau in range(1, total_time):
            ground2, ground3 = room2_calib[j][buffer + tau], room3_calib[j][buffer + tau]
            prediction2, prediction3 = room2_calib_prediction[str(0)][j][tau-1], room3_calib_prediction[str(0)][j][tau-1]
            nonconformity_room2 = abs(ground2 - prediction2) / room2_sigmas[0][tau]
            nonconformity_room3 = abs(ground3 - prediction3) / room3_sigmas[0][tau]
            r.append(nonconformity_room2)
            r.append(nonconformity_room3)
        r_open_nonconformity_list.append(max(r))
    p = int(np.ceil((len(room2_calib) + 1) * (1 - delta)))
    r_open_nonconformity_list.append(float("inf"))
    r_open_nonconformity_list.sort()
    c_open = r_open_nonconformity_list[p - 1]
    return c_open


def compare():
    # Load data from files.
    with open("case1 temperature/data_original/room2_train.json") as f:
        room2_train = json.load(f)
    with open("case1 temperature/data_original/room3_train.json") as f:
        room3_train = json.load(f)
    with open("case1 temperature/data_original/room2_calib.json") as f:
        room2_calib = json.load(f)
    with open("case1 temperature/data_original/room3_calib.json") as f:
        room3_calib = json.load(f)
    with open("case1 temperature/data_cp/room2_train_prediction.json") as f:
        room2_train_prediction = json.load(f)
    with open("case1 temperature/data_cp/room3_train_prediction.json") as f:
        room3_train_prediction = json.load(f)
    with open("case1 temperature/data_cp/room2_calib_prediction.json") as f:
        room2_calib_prediction = json.load(f)
    with open("case1 temperature/data_cp/room3_calib_prediction.json") as f:
        room3_calib_prediction = json.load(f)

        # Proceed with The LCP Algorithm.
    print("Conducting LCP Method:")
    print("Start timer for LCP.")
    start = time.time()
    print("Organizing nonconformity scores.")
    nonconformity_scores_opt, nonconformity_scores_cp = organize_nonconformity_scores(room2_calib, room2_calib_prediction, room3_calib, room3_calib_prediction, lcp_optimization_size)
    print("Starting to compute alphas via solving the LCP.")
    alphas_opt = compute_alphas_lcp(nonconformity_scores_opt)
    print("Starting to perform conformal prediction.")
    lcp_c_open = perform_cp(alphas_opt, nonconformity_scores_cp)
    print("C computed with the LCP method:", lcp_c_open)
    print("C has been obtained.")
    print("End timer.")
    print("Time elapsed:", time.time() - start, "seconds for LCP.\n")

    # Proceed with our algorithm.
    print("Conducting our method:")
    print("Start timer for our method.")
    start = time.time()
    room2_sigmas = compute_sigmas(room2_train, room2_train_prediction)
    room3_sigmas = compute_sigmas(room3_train, room3_train_prediction)
    print("room2_sigmas", room2_sigmas)
    print("room3_sigmas", room3_sigmas)
    our_c_open = compute_quantiles_ours(delta, room2_calib, room2_calib_prediction, room3_calib, room3_calib_prediction, room2_sigmas, room3_sigmas)
    print("Our computed C:", our_c_open)
    print("End timer.")
    print("Time elapsed:", time.time() - start, "seconds for Our method.")


    # Compare the prediction regions.
    print("Compute prediction regions for LCP, Room 2.")
    regions_lcp_room_2 = []
    for t in range(total_time - 1):
        regions_lcp_room_2.append(lcp_c_open / alphas_opt[t])
    print("Compute prediction regions for LCP, Room 3.")
    regions_lcp_room_3 = []
    for t in range(total_time - 1, len(alphas_opt)):
        regions_lcp_room_3.append(lcp_c_open / alphas_opt[t])
    
    print("Compute prediction regions for Our Method, Room 2.")
    regions_our_room_2 = []
    for t in range(1, total_time):
        regions_our_room_2.append(our_c_open * room2_sigmas[0][t])
    print("Compute prediction regions for Our Method, Room 3.")
    regions_our_room_3 = []
    for t in range(1, total_time):
        regions_our_room_3.append(our_c_open * room3_sigmas[0][t])


    with open('case1 temperature/data_comparison/room2_regions_lcp.json', 'w') as f:
        json.dump(regions_lcp_room_2, f)
    with open('case1 temperature/data_comparison/room3_regions_lcp.json', 'w') as f:
        json.dump(regions_lcp_room_3, f)
    with open('case1 temperature/data_comparison/room2_regions_ours.json', 'w') as f:
        json.dump(regions_our_room_2, f)
    with open('case1 temperature/data_comparison/room3_regions_ours.json', 'w') as f:
        json.dump(regions_our_room_3, f)



def PrintPaperFigComp(r2_trace_list_open, r3_trace_list_open):
    fig, ax = plt.subplots(1, 2, figsize=(8, 3))
    font_size = 14
    r2_trace_list = r2_trace_list_open
    r3_trace_list = r3_trace_list_open

    with open('case1 temperature/data_comparison/room2_regions_ours.json') as f:
        room2_regions_ours = json.load(f)
    with open('case1 temperature/data_comparison/room3_regions_ours.json') as f:
        room3_regions_ours = json.load(f)
    with open('case1 temperature/data_comparison/room2_regions_lcp.json') as f:
        room2_regions_lcp = json.load(f)
    with open('case1 temperature/data_comparison/room3_regions_lcp.json') as f:
        room3_regions_lcp = json.load(f)

    r2_pred_upper = [[r2_trace_list[0]], [r2_trace_list[0]]]
    r2_pred_lower = [[r2_trace_list[0]], [r2_trace_list[0]]]
    r3_pred_upper = [[r3_trace_list[0]], [r3_trace_list[0]]]
    r3_pred_lower = [[r3_trace_list[0]], [r3_trace_list[0]]]
    for tau in range(1, total_time):
        r2_pred_upper[0].append(r2_trace_list[tau] + room2_regions_ours[tau-1])
        r2_pred_lower[0].append(r2_trace_list[tau] - room2_regions_ours[tau-1])
        r3_pred_upper[0].append(r3_trace_list[tau] + room3_regions_ours[tau-1])
        r3_pred_lower[0].append(r3_trace_list[tau] - room3_regions_ours[tau-1])
        r2_pred_upper[1].append(r2_trace_list[tau] + room2_regions_lcp[tau-1])
        r2_pred_lower[1].append(r2_trace_list[tau] - room2_regions_lcp[tau-1])
        r3_pred_upper[1].append(r3_trace_list[tau] + room3_regions_lcp[tau-1])
        r3_pred_lower[1].append(r3_trace_list[tau] - room3_regions_lcp[tau-1])
        
    for i in range(2):
        ax[i].plot(np.arange(total_time), r2_pred_upper[i], alpha=0)
        ax[i].plot(np.arange(total_time), r2_pred_lower[i], alpha=0)
        ax[i].plot(np.arange(total_time), r3_pred_upper[i], alpha=0)
        ax[i].plot(np.arange(total_time), r3_pred_lower[i], alpha=0)
        ax[i].fill_between(np.arange(total_time), r2_pred_upper[i], r2_pred_lower[i], where=np.array(r2_pred_upper[i]) > np.array(r2_pred_lower[i]), interpolate=True, alpha=0.1, color = "red", label = "Predicted region of $Y_1$" if i == 0 else None)
        ax[i].fill_between(np.arange(total_time), r3_pred_upper[i], r3_pred_lower[i], where=np.array(r3_pred_upper[i]) > np.array(r3_pred_lower[i]), interpolate=True, alpha=0.1, color = "blue", label = "Predicted region of $Y_2$" if i == 0 else None)
        ax[i].plot(np.arange(total_time), r2_trace_list, linestyle=':', linewidth=1, color = "red")
        ax[i].plot(np.arange(total_time), r3_trace_list, linestyle=':', linewidth=1, color = "blue")

    for i in range(2):
        ax[i].tick_params(axis='x', labelsize=10)
        ax[i].tick_params(axis='y', labelsize=10)
        ax[i].set_ylim(13,28)

    ax[0].legend(fontsize = 12, loc='lower right')
    ax[0].set_title('Our result', fontsize=font_size-3)
    ax[1].set_title('Result from [Cleaveland et al.(2024)]', fontsize=font_size-3)
    plt.savefig("case1 temperature/fig/case1_comp.pdf")

if __name__ == '__main__':
    compare()

    with open("case1 temperature/data_controlresults/r2_trace_list_openloop.json") as f:
        r2_trace_list_openloop = json.load(f)
    with open("case1 temperature/data_controlresults/r3_trace_list_openloop.json") as f:
        r3_trace_list_openloop = json.load(f)

    PrintPaperFigComp(r2_trace_list_openloop[str(0)], r3_trace_list_openloop[str(0)])