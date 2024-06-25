import numpy as np
from tensorflow import keras
import matplotlib.pyplot as plt
import json
from parameters import *


def generate_predictions(data, len_in, model):
    data_x = [item[:len_in] for item in data]
    data_y = [item[len_in:len_seq] for item in data]
    data_x = np.array(data_x).reshape(-1, len(data_x[0]), 2)
    data_y = np.array(data_y).reshape(-1, len(data_y[0]), 2)
    return model.predict(data_x).tolist()


def compute_sigmas(data, data_predictions):
    sigmas = dict()
    for k in range(total_time - 1):
        sigmas[k] = dict()
        for tau in range(k + 1, total_time):
            residuals = []
            for j in range(len(data)):
                ground = data[j][tau]
                predicted = data_predictions[str(k)][j][tau-k-1]
                diff = [a - b for a, b in zip(ground, predicted)]
                norm = np.linalg.norm(diff)   # 2-norm
                residuals.append(norm)
            sigmas[k][tau] = max(residuals)
    return sigmas

def compute_quantiles(delta, calib, calib_prediction, sigmas):
    r_open_nonconformity_list = []
    for j in range(len(calib)):
        r = []
        for tau in range(1, total_time):
            ground = calib[j][tau]
            predicted = calib_prediction[str(0)][j][tau-1]
            nonconformity = np.linalg.norm([a - b for a, b in zip(ground, predicted)]) / sigmas[0][tau]
            r.append(nonconformity)
        r_open_nonconformity_list.append(max(r))

    p = int(np.ceil((len(calib) + 1) * (1 - delta)))
    r_open_nonconformity_list.append(float("inf"))
    r_open_nonconformity_list.sort()
    c_open = r_open_nonconformity_list[p - 1]
    print("c_open:", c_open, end="\n")

    r_close_nonconformity_list = []
    for j in range(len(calib)):
        r = []
        for k in range(total_time - 1):
            ground = calib[j][k + 1]
            predicted = calib_prediction[str(k)][j][0]
            nonconformity = np.linalg.norm([a - b for a, b in zip(ground, predicted)]) / sigmas[k][k+1]
            r.append(nonconformity)

        r_close_nonconformity_list.append(max(r))

    p = int(np.ceil((len(calib) + 1) * (1 - delta)))
    r_close_nonconformity_list.append(float("inf"))
    r_close_nonconformity_list.sort()
    c_close = r_close_nonconformity_list[p - 1]
    print("c_close:", c_close, "\n")

    with open('data_cp/r_open_nonconformity_list.json', 'w') as f:
        json.dump(r_open_nonconformity_list, f)
    with open('data_cp/r_close_nonconformity_list.json', 'w') as f:
        json.dump(r_close_nonconformity_list, f)

    return c_open, c_close




def obtain_predicitons():
    with open("data_original/r2_train.json") as f:
        r2_train = json.load(f)
    with open("data_original/r2_calib.json") as f:
        r2_calib = json.load(f)
    with open("data_original/r2_test.json") as f:
        r2_test = json.load(f)

    print("Starting to compute predictions. \n")

    r2_calib_predictions, r2_train_predictions, r2_test_prediction = dict(), dict(), dict()
    for k in range(total_time - 1):
        model = keras.models.load_model(f'predictors/predictor_{k}.keras')
        len_in = k + 1
        r2_calib_predictions[k] = generate_predictions(r2_calib, len_in, model)
        r2_train_predictions[k] = generate_predictions(r2_train, len_in, model)
        r2_test_prediction[k] = generate_predictions(r2_test, len_in, model)

    with open('data_cp/r2_calib_prediction.json', 'w') as f:
        json.dump(r2_calib_predictions , f)
    with open('data_cp/r2_train_prediction.json', 'w') as f:
        json.dump(r2_train_predictions, f)
    with open('data_cp/r2_test_prediction.json', 'w') as f:
        json.dump(r2_test_prediction, f)
    print("Computing predictions completed, and all the predictions have been saved. \n")


def obtain_sigmas_and_c():
    with open("data_original/r2_train.json") as f:
        r2_train = json.load(f)
    with open("data_original/r2_calib.json") as f:
        r2_calib = json.load(f)
    with open("data_cp/r2_train_prediction.json") as f:
        r2_train_prediction = json.load(f) 
    with open("data_cp/r2_calib_prediction.json") as f:
        r2_calib_prediction = json.load(f) 

    print("Starting to compute Sigmas and C. \n")

    r2_sigmas = compute_sigmas(r2_train, r2_train_prediction)
    with open('data_cp/r2_sigmas.json', 'w') as f:
        json.dump(r2_sigmas, f)


    c_open, c_close = compute_quantiles(delta, r2_calib, r2_calib_prediction, r2_sigmas)

    with open('data_cp/c_open.json', 'w') as f:
        json.dump(c_open, f)
    with open('data_cp/c_close.json', 'w') as f:
        json.dump(c_close, f)

    print("Sigmas, c_open, c_close have all been obtained and saved. \n")


if __name__ == '__main__':
    obtain_predicitons()
    obtain_sigmas_and_c()
    