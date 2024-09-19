import json
from parameters import *
from Step2_conformal_prediction import *


def generate_predictions(data, len_in, model):
    data_x = [item[:len_in] for item in data]
    data_y = [item[len_in:len_seq] for item in data]
    data_x = np.array(data_x).reshape(-1, len(data_x[0]), 1)
    data_y = np.array(data_y).reshape(-1, len(data_y[0]), 1)
    return model.predict(data_x).tolist()


if __name__ == '__main__':
    print("Starting to prepare for the control, including: compute predicitons for test data; copy useful data to the file called data_pre_control. \n")
    with open("case1 temperature/data_original/room2_test.json") as f:
        room2_test = json.load(f)
    with open("case1 temperature/data_original/room3_test.json") as f:
        room3_test = json.load(f)
    with open("case1 temperature/data_cp/c_open.json") as f:
        c_open = json.load(f)
    with open("case1 temperature/data_cp/c_close.json") as f:
        c_close = json.load(f)
    with open("case1 temperature/data_cp/room2_sigmas.json") as f:
        room2_sigmas = json.load(f)
    with open("case1 temperature/data_cp/room3_sigmas.json") as f:
        room3_sigmas = json.load(f)

    c_close_room2 = dict()
    c_close_room3 = dict()
    c_open_room2 = dict()
    c_open_room3 = dict()
    for k in range(total_time - 1):
        c_close_room2[k] = dict()
        c_close_room3[k] = dict()
        if k == 0:
            c_open_room2[k] = dict()
            c_open_room3[k] = dict()
        for tau in range(k + 1, total_time):
            c_close_room2[k][tau] = room2_sigmas[str(k)][str(tau)]*c_close
            c_close_room3[k][tau] = room3_sigmas[str(k)][str(tau)]*c_close
            if k == 0:
                c_open_room2[k][tau] = room2_sigmas[str(k)][str(tau)]*c_open
                c_open_room3[k][tau] = room3_sigmas[str(k)][str(tau)]*c_open



    room2_test_predictions, room3_test_predictions = dict(), dict()
    for k in range(total_time - 1):
        model2 = keras.models.load_model(f'case1 temperature/predictors/predictor2_{k}.keras')
        model3 = keras.models.load_model(f'case1 temperature/predictors/predictor3_{k}.keras')
        len_in = k + buffer + 1
        room2_test_predictions[k] = generate_predictions(room2_test, len_in, model2)
        room3_test_predictions[k] = generate_predictions(room3_test, len_in, model3)


    room2_ground = [room2_test[i][buffer:] for i in range(len(room2_test))]
    room3_ground = [room3_test[i][buffer:] for i in range(len(room3_test))]

    with open('case1 temperature/data_pre_control/room2_test_predictions.json', 'w') as f:
        json.dump(room2_test_predictions, f)
    with open('case1 temperature/data_pre_control/room3_test_predictions.json', 'w') as f:
        json.dump(room3_test_predictions, f)
    with open('case1 temperature/data_pre_control/room2_ground.json', 'w') as f:
        json.dump(room2_ground, f)
    with open('case1 temperature/data_pre_control/room3_ground.json', 'w') as f:
        json.dump(room3_ground, f)
    with open('case1 temperature/data_pre_control/c_close_room2.json', 'w') as f:
        json.dump(c_close_room2, f)
    with open('case1 temperature/data_pre_control/c_close_room3.json', 'w') as f:
        json.dump(c_close_room3, f)
    with open('case1 temperature/data_pre_control/c_open_room2.json', 'w') as f:
        json.dump(c_open_room2, f)
    with open('case1 temperature/data_pre_control/c_open_room3.json', 'w') as f:
        json.dump(c_open_room3, f)

    print("We have finished all the preparation for the control. Let's design a controller now! \n")