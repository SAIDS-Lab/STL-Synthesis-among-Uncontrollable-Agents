import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

import matplotlib.pyplot as plt
import json
from parameters import *

tf.random.set_seed(12)

class CustomCallback(keras.callbacks.Callback):
    def __init__(self, display_interval):
        self.display_interval = display_interval

    def on_epoch_end(self, epoch, logs=None):
        if epoch % self.display_interval == 0:
            print(f'Epoch {epoch}: {logs}')

display_interval = 100  # Display information every 100 epochs
custom_callback = CustomCallback(display_interval)


def lstm_net_train(data, k):
    '''split the data'''
    len_in = k + buffer + 1
    train_data_x = [item[:len_in] for item in data]
    train_data_y = [item[len_in:len_seq] for item in data]
    train_data_x = np.array(train_data_x).reshape(-1, len(train_data_x[0]), 1)
    train_data_y = np.array(train_data_y).reshape(-1, len(train_data_y[0]), 1)

    '''build model'''
    model = Sequential()
    model.add(LSTM(10, input_shape=(len_in, 1)))
    model.add(Dense(50))
    model.add(Dense(20))
    model.add(Dense(len_seq - len_in))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(train_data_x, train_data_y, epochs=1000, batch_size=1, verbose=0, callbacks=[custom_callback])
    return model
    

   

def lstm_eval():
    '''Change the following parameters to evaluate different cases'''
    index = 1
    k = 0
    len_in = k + buffer + 1
    with open("data_original/room3_calib.json") as f:
        room_calib = json.load(f)
    model = keras.models.load_model(f'predictors/predictor3_{k}.keras')

    calib_data_x = [item[:len_in] for item in room_calib]
    calib_data_y = [item[len_in:len_seq] for item in room_calib]
    calib_data_x = np.array(calib_data_x).reshape(-1, len(calib_data_x[0]), 1)
    calib_data_y = np.array(calib_data_y).reshape(-1, len(calib_data_y[0]), 1)
    
    test_output = model.predict(calib_data_x).tolist()

    original = [value[0] for value in calib_data_x[index]]
    print(original)
    predicted = original.copy()
    print(test_output[index])
    predicted.extend(test_output[index])
    ground = original
    ground.extend([value[0] for value in calib_data_y[index]])

    plt.scatter([t for t in range(len(predicted))], predicted, label = "predicted")
    plt.scatter([t for t in range(len(ground))], ground, label = "ground")
    plt.legend()
    plt.show()


def train_lstms():
    with open("data_original/room2_train.json") as f:
        room2_train = json.load(f)
    with open("data_original/room3_train.json") as f:
        room3_train = json.load(f)

    print("Starting to train the LSTMs. \n")

    for k in range(total_time - 1):
        print("training the predictor at time step:", k)
        model = lstm_net_train(room2_train, k)
        model.save(f'predictors/predictor2_{k}.keras')
        model = lstm_net_train(room3_train, k)
        model.save(f'predictors/predictor3_{k}.keras')

    print("LSTMs have been saved in the folder called predictors. \n")

        


if __name__ == '__main__':
    # train_lstms()

    lstm_eval()

    


    


