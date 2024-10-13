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
bin_width= 0.01

with open("case1 temperature/data_cp/c_open.json") as f:
    c_open = json.load(f)
with open("case1 temperature/data_cp/c_close.json") as f:
    c_close = json.load(f)


# Calculate the percentage of test data satisfying theorem 1:
with open('case1 temperature/data_original/room2_test.json') as f:
    room2_test = json.load(f)
with open('case1 temperature/data_original/room3_test.json') as f:
    room3_test = json.load(f)
with open('case1 temperature/data_original/room2_calib.json') as f:
    room2_cal = json.load(f)
with open('case1 temperature/data_original/room3_calib.json') as f:
    room3_cal = json.load(f)
with open('case1 temperature/data_cp/room2_sigmas.json') as f:
    room2_sigmas = json.load(f)
with open('case1 temperature/data_cp/room3_sigmas.json') as f:
    room3_sigmas = json.load(f)

print("Load predictions.")
with open('case1 temperature/data_pre_control/room2_test_predictions.json', 'r') as f:
    room2_test_prediction = json.load(f)
with open('case1 temperature/data_pre_control/room3_test_predictions.json', 'r') as f:
    room3_test_prediction = json.load(f)
with open('case1 temperature/data_cp/room2_calib_prediction.json', 'r') as f:
    room2_calib_prediction = json.load(f)
with open('case1 temperature/data_cp/room3_calib_prediction.json', 'r') as f:
    room3_calib_prediction = json.load(f)


def compute_quantiles(delta, room2_calib, room2_calib_prediction, room3_calib, room3_calib_prediction, room2_sigmas, room3_sigmas):
    r_open_nonconformity_list = []
    for j in range(len(room2_calib)):
        r = []
        for tau in range(1, total_time):
            ground2, ground3 = room2_calib[j][buffer + tau], room3_calib[j][buffer + tau]
            prediction2, prediction3 = room2_calib_prediction[str(0)][j][tau-1], room3_calib_prediction[str(0)][j][tau-1]
            nonconformity_room2 = abs(ground2 - prediction2) / room2_sigmas["0"][str(tau)]
            nonconformity_room3 = abs(ground3 - prediction3) / room3_sigmas["0"][str(tau)]
            r.append(nonconformity_room2)
            r.append(nonconformity_room3)
        r_open_nonconformity_list.append(max(r))

    p = int(np.ceil((len(room2_calib) + 1) * (1 - delta)))
    r_open_nonconformity_list.append(float("inf"))
    r_open_nonconformity_list.sort()
    # print(r_open_nonconformity_list)
    c_open = r_open_nonconformity_list[p - 1]


    r_close_nonconformity_list = []
    for j in range(len(room2_calib)):
        r = []
        for k in range(total_time - 1):
            for tau in range(k + 1, total_time):
                ground2, ground3 = room2_calib[j][buffer + tau], room3_calib[j][buffer + tau]
                prediction2, prediction3 = room2_calib_prediction[str(k)][j][tau-k-1], room3_calib_prediction[str(k)][j][tau-k-1]
                nonconformity_room2 = abs(ground2 - prediction2) / room2_sigmas[str(k)][str(tau)]
                nonconformity_room3 = abs(ground3 - prediction3) / room3_sigmas[str(k)][str(tau)]
                r.append(nonconformity_room2)
                r.append(nonconformity_room3)
        r_close_nonconformity_list.append(max(r))

    p = int(np.ceil((len(room2_calib) + 1) * (1 - delta)))
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
num_samples_each_trial = 150
bin_width= 1/num_samples_each_trial

for i in range(num_trials):
    """
    Create samples.
    """
    # First generate random indices from 500 numbers.
    delta=0.15
    sample_cal_inds = random.sample(range(0, len(room2_cal)), num_samples_each_trial)
    room2_cal_sample = [room2_cal[i] for i in sample_cal_inds]
    room3_cal_sample = [room3_cal[i] for i in sample_cal_inds]
    cal_predictions_room_2_sample = sample_from_test_predictions(room2_calib_prediction, sample_cal_inds)
    cal_predictions_room_3_sample = sample_from_test_predictions(room3_calib_prediction, sample_cal_inds)
    sample_test_inds = random.sample(range(0, len(room2_test)), num_samples_each_trial)
    room2_test_sample = [room2_test[i] for i in sample_test_inds]
    room3_test_sample = [room3_test[i] for i in sample_test_inds]
    test_predictions_room_2_sample = sample_from_test_predictions(room2_test_prediction, sample_test_inds)
    test_predictions_room_3_sample = sample_from_test_predictions(room3_test_prediction, sample_test_inds)

    """
    Compute the quantiles.
    """
    c1, c2 = compute_quantiles(delta, room2_cal_sample, cal_predictions_room_2_sample, room3_cal_sample, cal_predictions_room_3_sample, room2_sigmas, room3_sigmas)

    # for the result in the form of number
    count = 0
    correct_count = 0
    for tau in range(len(test_predictions_room_2_sample["0"][0])):
        if abs(room2_test_sample[0][buffer+tau+1] - test_predictions_room_2_sample[str(0)][0][tau]) <= c1 * room2_sigmas[str(0)][str(tau+1)]:
            correct_count += 1
        count += 1
    if count == correct_count:
        stmt_1_value += 1

    count = 0
    correct_count = 0
    for k in range(len(test_predictions_room_2_sample["0"][0])):
        for tau in range(k + 1, len(test_predictions_room_2_sample["0"][0])):
            if abs(room2_test_sample[0][buffer + tau] - test_predictions_room_2_sample[str(k)][0][tau-k-1]) <= c2 * room2_sigmas[str(k)][str(tau)] and abs(room3_test_sample[0][buffer + tau] - test_predictions_room_3_sample[str(k)][0][tau-k-1]) <= c2 * room3_sigmas[str(k)][str(tau)]:
                correct_count += 1
            count += 1
    if count == correct_count:
        stmt_2_value += 1

    # for the result in the form of plot
    correct_count_stmt_1 = 0
    for j in range(len(room2_test_sample)):
        count = 0
        correct_count = 0
        for tau in range(len(test_predictions_room_2_sample["0"][0])):
            if abs(room2_test_sample[j][buffer+tau+1] - test_predictions_room_2_sample[str(0)][j][tau]) <= c1 * room2_sigmas[str(0)][str(tau+1)] and abs(room3_test_sample[j][buffer+tau+1] - test_predictions_room_3_sample[str(0)][j][tau]) <= c1 * room3_sigmas[str(0)][str(tau+1)]:
                correct_count += 1
            count += 1
        if count == correct_count:
            correct_count_stmt_1 += 1
    stmt_1_coverages.append(correct_count_stmt_1 / num_samples_each_trial)

    correct_count_stmt_2 = 0
    for j in range(len(room2_test_sample)):
        count = 0
        correct_count = 0
        for k in range(len(test_predictions_room_2_sample["0"][0])):
            for tau in range(k + 1, len(test_predictions_room_2_sample["0"][0])):
                if abs(room2_test_sample[j][buffer + tau] - test_predictions_room_2_sample[str(k)][j][tau-k-1]) <= c2 * room2_sigmas[str(k)][str(tau)] and abs(room3_test_sample[j][buffer + tau] - test_predictions_room_3_sample[str(k)][j][tau-k-1]) <= c2 * room3_sigmas[str(k)][str(tau)]:
                    correct_count += 1
                count += 1
        if count == correct_count:
            correct_count_stmt_2 += 1
    stmt_2_coverages.append(correct_count_stmt_2 / num_samples_each_trial)

with open('case1 temperature/data_cp/test_result_stmt_1.json', 'w') as f:
    json.dump(stmt_1_coverages, f)
with open('case1 temperature/data_cp/test_result_stmt_2.json', 'w') as f:
    json.dump(stmt_2_coverages, f)

print("the result 1 in the paper is", stmt_1_value/num_trials)
print("the result 2 in the paper is", stmt_2_value/num_trials)

