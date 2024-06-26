import matplotlib.pyplot as plt
import json
import numpy as np
import sys
import os
module_path = os.path.abspath(os.path.join('please replace it with your own path/STL-Synthesis-among-Uncontrollable-Agents/case2 motion planning'))
if module_path not in sys.path:
    sys.path.append(module_path)
from parameters import *
import random

random.seed(123)
bin_width= 0.01

with open("data_cp/c_open.json") as f:
    c_open = json.load(f)
with open("data_cp/c_close.json") as f:
    c_close = json.load(f)


# Calculate the percentage of test data satisfying theorem 1:
with open('data_original/r2_test.json') as f:
    r2_test = json.load(f)
with open('data_original/r2_calib.json') as f:
    r2_cal = json.load(f)
with open('data_cp/r2_sigmas.json') as f:
    r2_sigmas = json.load(f)

print("Load predictions.")
with open('data_cp/r2_test_prediction.json', 'r') as f:
    r2_test_prediction = json.load(f)
with open('data_cp/r2_calib_prediction.json', 'r') as f:
    r2_calib_prediction = json.load(f)



def compute_quantiles(delta, r2_calib, r2_calib_prediction, r2_sigmas):
    r_open_nonconformity_list = []
    for j in range(len(r2_calib)):
        r = []
        for tau in range(1, total_time):
            ground = r2_calib[j][tau]
            prediction = r2_calib_prediction[str(0)][j][tau-1]
            nonconformity = np.linalg.norm([a - b for a, b in zip(ground, prediction)]) / r2_sigmas[str(0)][str(tau)]
            r.append(nonconformity)
        r_open_nonconformity_list.append(max(r))

    p = int(np.ceil((len(r2_calib) + 1) * (1 - delta)))
    r_open_nonconformity_list.append(float("inf"))
    r_open_nonconformity_list.sort()
    c_open = r_open_nonconformity_list[p - 1]

    r_close_nonconformity_list = []
    for j in range(len(r2_calib)):
        r = []
        for k in range(total_time - 1):
            ground = r2_calib[j][k + 1]
            prediction = r2_calib_prediction[str(k)][j][0]
            nonconformity = np.linalg.norm([a - b for a, b in zip(ground, prediction)]) / r2_sigmas[str(k)][str(k+1)]
            r.append(nonconformity)
        r_close_nonconformity_list.append(max(r))

    p = int(np.ceil((len(r2_calib) + 1) * (1 - delta)))
    r_close_nonconformity_list.append(float("inf"))
    r_close_nonconformity_list.sort()
    c_close = r_close_nonconformity_list[p - 1]

    return c_open, c_close


# Let's segment test set into folds of 100 data traces.
# Test statement 1 - open loop; test statement 2 - closed loop.
stmt_1_coverages = []
stmt_2_coverages = []
stmt_1_value = 0
stmt_2_value = 0

def sample_from_test_predictions(data_set, sample_inds):
    new_data_set = dict()
    for k in data_set.keys():
        new_data_set[k] = []
        for j in range(len(sample_inds)):
            new_data_set[k].append(data_set[str(k)][sample_inds[j]])
    return new_data_set

num_trials = 1000
num_samples_each_trial = 50
bin_width= 1/num_samples_each_trial

for i in range(num_trials):
    """
    Create samples.
    """
    # First generate random indices from 500 numbers.
    delta=0.15
    sample_cal_inds = random.sample(range(0, len(r2_cal)), num_samples_each_trial)
    r2_cal_sample = [r2_cal[i] for i in sample_cal_inds]
    cal_predictions_r2_sample = sample_from_test_predictions(r2_calib_prediction, sample_cal_inds)
    sample_test_inds = random.sample(range(0, len(r2_test)), num_samples_each_trial)
    r2_test_sample = [r2_test[i] for i in sample_test_inds]
    test_predictions_r2_sample = sample_from_test_predictions(r2_test_prediction, sample_test_inds)

    """
    Compute the quantiles.
    """
    c1, c2 = compute_quantiles(delta, r2_cal_sample, cal_predictions_r2_sample, r2_sigmas)

    # for the result in the form of number
    count = 0
    correct_count = 0
    # print(test_predictions_r2_sample)
    for tau in range(len(test_predictions_r2_sample["0"][0])):
        if np.linalg.norm([a - b for a, b in zip(r2_test_sample[0][tau+1], test_predictions_r2_sample[str(0)][0][tau])]) <= c1 * r2_sigmas[str(0)][str(tau+1)]:
            correct_count += 1
        count += 1
    if count == correct_count:
        stmt_1_value += 1

    count = 0
    correct_count = 0
    for k in range(len(test_predictions_r2_sample["0"][0])):
        if np.linalg.norm([a - b for a, b in zip(r2_test_sample[0][k+1], test_predictions_r2_sample[str(k)][0][0])]) <= c2 * r2_sigmas[str(k)][str(k + 1)]:
            correct_count += 1
        count += 1
    if count == correct_count:
        stmt_2_value += 1

    # for the result in the form of plot
    correct_count_stmt_1 = 0
    for j in range(len(r2_test_sample)):
        count = 0
        correct_count = 0
        for tau in range(len(test_predictions_r2_sample["0"][0])):
            if np.linalg.norm([a - b for a, b in zip(r2_test_sample[j][tau+1], test_predictions_r2_sample[str(0)][j][tau])]) <= c1 * r2_sigmas[str(0)][str(tau+1)]:
                correct_count += 1
            count += 1
        if count == correct_count:
            correct_count_stmt_1 += 1
    stmt_1_coverages.append(correct_count_stmt_1 / num_samples_each_trial)

    correct_count_stmt_2 = 0
    for j in range(len(r2_test_sample)):
        count = 0
        correct_count = 0
        for k in range(len(test_predictions_r2_sample["0"][0])):
            if np.linalg.norm([a - b for a, b in zip(r2_test_sample[j][k+1], test_predictions_r2_sample[str(k)][j][0])]) <= c2 * r2_sigmas[str(k)][str(k + 1)]:
                correct_count += 1
            count += 1
        if count == correct_count:
            correct_count_stmt_2 += 1
    stmt_2_coverages.append(correct_count_stmt_2 / num_samples_each_trial)

with open('data_cp/test_result_stmt_1.json', 'w') as f:
    json.dump(stmt_1_coverages, f)
with open('data_cp/test_result_stmt_2.json', 'w') as f:
    json.dump(stmt_2_coverages, f)

print("the result 1 in the paper is", stmt_1_value/num_trials)
print("the result 2 in the paper is", stmt_2_value/num_trials)

