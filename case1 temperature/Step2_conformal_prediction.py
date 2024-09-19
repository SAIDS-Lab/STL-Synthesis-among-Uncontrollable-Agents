import numpy as np
from tensorflow import keras
import matplotlib.pyplot as plt
import json
from parameters import *


def generate_predictions(data, len_in, model):
    data_x = [item[:len_in] for item in data]
    data_y = [item[len_in:len_seq] for item in data]
    data_x = np.array(data_x).reshape(-1, len(data_x[0]), 1)
    data_y = np.array(data_y).reshape(-1, len(data_y[0]), 1)
    return model.predict(data_x).tolist()


def compute_sigmas(data, data_predictions):
    sigmas = dict()
    for k in range(total_time - 1):
        sigmas[k] = dict()
        for tau in range(k + 1, total_time):
            residuals = []
            for j in range(len(data)):
                ground = data[j][tau+buffer]
                predicted = data_predictions[str(k)][j][tau-k-1]
                residuals.append(abs(ground - predicted))
            sigmas[k][tau] = max(residuals)
    return sigmas

def compute_quantiles(delta, room2_calib, room2_calib_prediction, room3_calib, room3_calib_prediction, room2_sigmas, room3_sigmas):
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
    print("c_open:", c_open, end="\n")

    r_close_nonconformity_list = []
    for j in range(len(room2_calib)):
        r = []
        for k in range(total_time - 1):
            for tau in range(k + 1, total_time):
                ground2, ground3 = room2_calib[j][buffer + tau], room3_calib[j][buffer + tau]
                prediction2, prediction3 = room2_calib_prediction[str(k)][j][tau-k-1], room3_calib_prediction[str(k)][j][tau-k-1]
                nonconformity_room2 = abs(ground2 - prediction2) / room2_sigmas[k][tau]
                nonconformity_room3 = abs(ground3 - prediction3) / room3_sigmas[k][tau]
                r.append(nonconformity_room2)
                r.append(nonconformity_room3)
        r_close_nonconformity_list.append(max(r))

    p = int(np.ceil((len(room2_calib) + 1) * (1 - delta)))
    r_close_nonconformity_list.append(float("inf"))
    r_close_nonconformity_list.sort()
    c_close = r_close_nonconformity_list[p - 1]
    print("c_close:", c_close)

    with open('case1 temperature/data_cp/r_open_nonconformity_list.json', 'w') as f:
        json.dump(r_open_nonconformity_list, f)
    with open('case1 temperature/data_cp/r_close_nonconformity_list.json', 'w') as f:
        json.dump(r_close_nonconformity_list, f)

    return c_open, c_close


def obtain_predicitons():
    with open("case1 temperature/data_original/room2_train.json") as f:
        room2_train = json.load(f)
    with open("case1 temperature/data_original/room3_train.json") as f:
        room3_train = json.load(f)
    with open("case1 temperature/data_original/room2_calib.json") as f:
        room2_calib = json.load(f)
    with open("case1 temperature/data_original/room3_calib.json") as f:
        room3_calib = json.load(f)

    print("Starting to compute predictions. \n")

    room2_calib_predictions, room2_train_predictions, room3_calib_predictions, room3_train_predictions = dict(), dict(), dict(), dict()
    for k in range(total_time - 1):
        model2 = keras.models.load_model(f'case1 temperature/predictors/predictor2_{k}.keras')
        model3 = keras.models.load_model(f'case1 temperature/predictors/predictor3_{k}.keras')
        len_in = k + buffer + 1
        room2_calib_predictions[k] = generate_predictions(room2_calib, len_in, model2)
        room2_train_predictions[k] = generate_predictions(room2_train, len_in, model2)
        room3_calib_predictions[k] = generate_predictions(room3_calib, len_in, model3)
        room3_train_predictions[k] = generate_predictions(room3_train, len_in, model3)

    with open('case1 temperature/data_cp/room2_calib_prediction.json', 'w') as f:
        json.dump(room2_calib_predictions , f)
    with open('case1 temperature/data_cp/room2_train_prediction.json', 'w') as f:
        json.dump(room2_train_predictions, f)
    with open('case1 temperature/data_cp/room3_calib_prediction.json', 'w') as f:
        json.dump(room3_calib_predictions, f)
    with open('case1 temperature/data_cp/room3_train_prediction.json', 'w') as f:
        json.dump(room3_train_predictions, f)

    print("Computing predictions completed, and all the predictions have been saved. \n")


def obtain_sigmas_and_c():
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

    print("Starting to compute Sigmas and C. \n")

    room2_sigmas = compute_sigmas(room2_train, room2_train_prediction)
    room3_sigmas = compute_sigmas(room3_train, room3_train_prediction)
    with open('case1 temperature/data_cp/room2_sigmas.json', 'w') as f:
        json.dump(room2_sigmas, f)
    with open('case1 temperature/data_cp/room3_sigmas.json', 'w') as f:
        json.dump(room3_sigmas, f)

    c_open, c_close = compute_quantiles(delta, room2_calib, room2_calib_prediction, room3_calib, room3_calib_prediction, room2_sigmas, room3_sigmas)

    with open('case1 temperature/data_cp/c_open.json', 'w') as f:
        json.dump(c_open, f)
    with open('case1 temperature/data_cp/c_close.json', 'w') as f:
        json.dump(c_close, f)

    print("Sigmas, c_open, c_close have all been obtained and saved. \n")


if __name__ == '__main__':
    obtain_predicitons()
    obtain_sigmas_and_c()
    