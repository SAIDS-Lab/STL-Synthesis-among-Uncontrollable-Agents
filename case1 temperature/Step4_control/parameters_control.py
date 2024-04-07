import json



with open('data_pre_control/c_close_room2.json', 'r') as json_file:
    c_close_room2 = json.load(json_file)
with open('data_pre_control/c_close_room3.json', 'r') as json_file:
    c_close_room3 = json.load(json_file)
with open('data_pre_control/c_open_room2.json', 'r') as json_file:
    c_open_room2 = json.load(json_file)
with open('data_pre_control/c_open_room3.json', 'r') as json_file:
    c_open_room3 = json.load(json_file)


with open('data_pre_control/room2_ground.json', 'r') as json_file:
    r2_ground = json.load(json_file)
with open('data_pre_control/room3_ground.json', 'r') as json_file:
    r3_ground = json.load(json_file)

with open('data_pre_control/room2_test_predictions.json', 'r') as json_file:
    y2_prediction_list= json.load(json_file)
with open('data_pre_control/room3_test_predictions.json', 'r') as json_file:
    y3_prediction_list= json.load(json_file)


optimal_state_sequence = [15]
optimal_control_sequence = []

total_time = 33
umax = 1
M = 10000

G_t = [1, total_time-1 - 2]
F_t = [0,2]
G_len = G_t[1] - G_t[0] + 1
GF_len = G_t[1] + F_t[1] - G_t[0] + 1
F_len = F_t[1] - F_t[0] + 1
bound = 10
epsilon = 0.0001