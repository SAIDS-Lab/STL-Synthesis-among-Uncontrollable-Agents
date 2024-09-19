
import json
from parameters import *
from Step2_conformal_prediction import *




def generate_predictions(data, len_in, model):
    data_x = [item[:len_in] for item in data]
    data_y = [item[len_in:len_seq] for item in data]
    data_x = np.array(data_x).reshape(-1, len(data_x[0]), 2)
    data_y = np.array(data_y).reshape(-1, len(data_y[0]), 2)
    return model.predict(data_x).tolist()




if __name__ == '__main__':
    print("Starting to prepare for the control, including: compute predicitons for test data; copy useful data to the file called data_pre_control. \n")
    with open("case2 motion planning/data_original/r2_test.json") as f:
        r2_test = json.load(f)
    with open("case2 motion planning/data_cp/c_open.json") as f:
        c_open = json.load(f)
    with open("case2 motion planning/data_cp/c_close.json") as f:
        c_close = json.load(f)
    with open("case2 motion planning/data_cp/r2_sigmas.json") as f:
        r2_sigmas = json.load(f)

    c_close_r2 = dict()
    c_open_r2 = dict()
    for k in range(total_time - 1):
        c_close_r2[k] = dict()
        if k == 0:
            c_open_r2[k] = dict()
        for tau in range(k + 1, total_time):
            c_close_r2[k][tau] = r2_sigmas[str(k)][str(tau)]*c_close
            if k == 0:
                c_open_r2[k][tau] = r2_sigmas[str(k)][str(tau)]*c_open

    r2_test_predictions = dict()
    for k in range(total_time - 1):
        model = keras.models.load_model(f'case2 motion planning/predictors/predictor_{k}.keras')
        len_in = k + 1
        r2_test_predictions[k] = generate_predictions(r2_test, len_in, model)

    r2_ground = r2_test

    with open('case2 motion planning/data_pre_control/r2_test_predictions.json', 'w') as f:
        json.dump(r2_test_predictions, f)
    with open('case2 motion planning/data_pre_control/r2_ground.json', 'w') as f:
        json.dump(r2_ground, f)
    with open('case2 motion planning/data_pre_control/c_close_r2.json', 'w') as f:
        json.dump(c_close_r2, f)
    with open('case2 motion planning/data_pre_control/c_open_r2.json', 'w') as f:
        json.dump(c_open_r2, f)

    print("We have finished all the preparation for the control. Let's design a controller now! \n")