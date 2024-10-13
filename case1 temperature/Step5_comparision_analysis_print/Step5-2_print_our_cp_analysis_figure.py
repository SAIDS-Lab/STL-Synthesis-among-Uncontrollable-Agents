import matplotlib.pyplot as plt
import json
import numpy as np
import sys
import os
module_path = os.path.abspath(os.path.join('please replace it with your own path/STL-Synthesis-among-Uncontrollable-Agents/case1 temperature'))
if module_path not in sys.path:
    sys.path.append(module_path)
from parameters import *
import random

random.seed(123)

font_size = 15
label_size = 12

# Plot the nonconformity list
def print_nonconformity(c_open, c_close, nonconformity_list_r_open, nonconformity_list_r_close):
    bin_width= 0.01
    fig, ax = plt.subplots(1, 2, figsize=(8, 3.5))
    nonconformity_list_r = [nonconformity_list_r_open, nonconformity_list_r_close]
    for i in range(2):
        bin_centers = np.arange(min(nonconformity_list_r[i])- bin_width / 2, max(nonconformity_list_r[i]) + bin_width / 2, bin_width)
        ax[i].hist(nonconformity_list_r[i], bins=bin_centers, rwidth=1)
        ax[i].set_ylabel("Frequency", fontsize=font_size)
        ax[i].set_xlabel("Score", fontsize=font_size)
        ax[i].tick_params(axis='x', labelsize = label_size)
        ax[i].tick_params(axis='y', labelsize = label_size)
    ax[0].set_xlim(0.2, 1.5)
    ax[1].set_xlim(0.55, 1.4)
    ax[0].set_title("$R_{OL}$ Nonconformity Scores", fontsize=font_size)
    ax[1].set_title("$R_{CL}$ Nonconformity Scores", fontsize=font_size)
    ax[0].axvline(x = c_open, label = "$C_{OL}$", color = "r")
    ax[1].axvline(x = c_close, label = "$C_{CL}$", color = "r")
    ax[0].legend(fontsize=font_size, loc='upper right')
    ax[1].legend(fontsize=font_size, loc='upper right')
    fig.tight_layout()
    fig.savefig("case1 temperature/fig/case1_nonconformity.pdf")



# Plot the test coverages.
def print_stmtresult(stmt_1_coverages, stmt_2_coverages):
    bin_width= 0.02
    fig, ax = plt.subplots(1, 2, figsize=(8, 3.5))
    stmt_coverage = [stmt_1_coverages, stmt_2_coverages]
    for i in range(2):
        bin_centers = np.arange(min(stmt_coverage[i])- bin_width / 2, max(stmt_coverage[i]) + bin_width / 2, bin_width)
        ax[i].hist(stmt_coverage[i], bins=bin_centers, rwidth=1)
        ax[i].set_ylabel("Frequency", fontsize=font_size)
        ax[i].set_xlabel("Percentage", fontsize=font_size)
        ax[i].tick_params(axis='x', labelsize = label_size)
        ax[i].tick_params(axis='y', labelsize = label_size)
        ax[i].axvline(x = 0.85, color = "r")
    ax[0].set_title("Empirical Coverage of (3)", fontsize=font_size)
    ax[1].set_title("Empirical Coverage of (15)", fontsize=font_size)
    fig.tight_layout()
    fig.savefig("case1 temperature/fig/case1_stmtresult.pdf")


if __name__ == "__main__":
    with open("case1 temperature/data_cp/c_open.json") as f:
        c_open = json.load(f)
    with open("case1 temperature/data_cp/c_close.json") as f:
        c_close = json.load(f)
    with open('case1 temperature/data_cp/r_open_nonconformity_list.json') as f:
        nonconformity_list_r_open = json.load(f)[:-1]
    with open('case1 temperature/data_cp/r_close_nonconformity_list.json') as f:
        nonconformity_list_r_close = json.load(f)[:-1]
    with open('case1 temperature/data_cp/test_result_stmt_1.json') as f:
        stmt_1_coverages = json.load(f)
    with open('case1 temperature/data_cp/test_result_stmt_2.json') as f:
        stmt_2_coverages = json.load(f)

    print_nonconformity(c_open, c_close, nonconformity_list_r_open, nonconformity_list_r_close)
    print_stmtresult(stmt_1_coverages, stmt_2_coverages)

