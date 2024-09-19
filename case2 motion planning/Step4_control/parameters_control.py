import json


with open('case2 motion planning/data_pre_control/c_close_r2.json', 'r') as json_file:
    c_close = json.load(json_file)
with open('case2 motion planning/data_pre_control/c_open_r2.json', 'r') as json_file:
    c_open = json.load(json_file)
with open('case2 motion planning/data_pre_control/r2_ground.json', 'r') as json_file:
    r2_ground = json.load(json_file)
with open('case2 motion planning/data_pre_control/r2_test_predictions.json', 'r') as json_file:
    y2_prediction_list= json.load(json_file)




total_time = 21

mu1x = [0, 2]
mu1y = [4, 6]
mu2x = [3.5, 6.5]
mu2y = [8, 10]
mu3x = [8.5, 10]
mu3y = [0, 2]
mu4x = [7, 8.5]
mu4y = [0, 2]



mu_obs1_x = [1.6, 2.6]
mu_obs1_y = [2, 3]
mu_obs2_x = [8.3, 9.3]
mu_obs2_y = [6.5, 7.5]
mu_obs3_x = [5.7, 6.7]
mu_obs3_y = [2.7, 3.7]


# we use this parameter as an engineer trick to guarantee the line between two dots will not collide the obstables
p_obs= 0.3


umax = 1
vmax = 1.5
M = 100
epsilon = 0.0001

G_track_t = [0, total_time-1]
G_track_len = G_track_t[1] - G_track_t[0] + 1

G_obs_t = [0, total_time-1]
G_obs_len = G_obs_t[1] - G_obs_t[0] + 1

G1_t = [6, 9]
G1_len = G1_t[1] - G1_t[0] + 1

G2_t = [5, 12]
G2_len = G2_t[1] - G2_t[0] + 1

FG_t = [14, 18, 0, 2]
FG_Flen = FG_t[1]- FG_t[0] + 1
FG_Glen = FG_t[3]- FG_t[2] + 1
FG_len = FG_t[1] + FG_t[3] - FG_t[0] + 1

D = 2
test_num = 1000

optimal_state_sequence = dict()
optimal_control_sequence = dict()

for i in range(test_num):
    optimal_state_sequence[i] = [[1, 0, 1, 0]]
    optimal_control_sequence[i] = []




