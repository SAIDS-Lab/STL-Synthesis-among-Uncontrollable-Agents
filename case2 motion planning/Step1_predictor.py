import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Reshape, LSTM


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
    len_in = k + 1
    len_out = len_seq - len_in
    train_data_x = [item[:len_in] for item in data]
    train_data_y = [item[len_in:len_seq] for item in data]
    train_data_x = np.array(train_data_x).reshape(-1, len(train_data_x[0]), 2)
    train_data_y = np.array(train_data_y).reshape(-1, len(train_data_y[0]), 2)

    '''build model'''
    model = Sequential()
    model.add(LSTM(10, input_shape=(len_in, 2)))
    model.add(Dense(50))
    model.add(Dense(20))
    model.add(Dense(len_out * 2))  
    model.add(Reshape((len_out, 2)))  
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(train_data_x, train_data_y, epochs=100, batch_size=1, verbose=0, callbacks=[custom_callback])
    return model
    

   

def lstm_eval():
    '''Change the following parameters to evaluate different cases'''
    index = 1
    k = 10
    len_in = k + 1
    with open("data_original/r2_calib.json") as f:
        room_calib = json.load(f)
    model = keras.models.load_model(f'predictors/predictor_{k}.keras')


    calib_data_x = [item[:len_in] for item in room_calib]
    calib_data_y = [item[len_in:len_seq] for item in room_calib]
    calib_data_x = np.array(calib_data_x).reshape(-1, len(calib_data_x[0]), 2)
    calib_data_y = np.array(calib_data_y).reshape(-1, len(calib_data_y[0]), 2)
    
    test_output = model.predict(calib_data_x).tolist()
    original = calib_data_x[index].tolist()
    predicted = original.copy()
    predicted.extend(test_output[index])
    ground = original
    ground.extend(calib_data_y[index].tolist())

    x_coords = [point[0] for point in predicted]
    y_coords = [point[1] for point in predicted]
    plt.scatter(x_coords, y_coords, label = "predicted")
    x_coords = [point[0] for point in ground]
    y_coords = [point[1] for point in ground]
    plt.scatter(x_coords, y_coords, label = "ground")
    plt.legend()
    plt.show()


def train_lstms():
    with open("data_original/r2_train.json") as f:
        r2_train = json.load(f)
    print("Starting to train the LSTMs. \n")

    for k in range(total_time - 1):
        print("training the predictor at time step:", k)
        model = lstm_net_train(r2_train, k)
        model.save(f'predictors/predictor_{k}.keras')

    print("LSTMs have been saved in the folder called predictors. \n")

        


if __name__ == '__main__':
    # train_lstms()

    lstm_eval()

    


    


