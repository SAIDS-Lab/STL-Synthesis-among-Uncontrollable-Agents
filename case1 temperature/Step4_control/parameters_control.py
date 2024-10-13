import json



with open('case1 temperature/data_pre_control/c_close_room2.json', 'r') as json_file:
    c_close_room2 = json.load(json_file)
with open('case1 temperature/data_pre_control/c_close_room3.json', 'r') as json_file:
    c_close_room3 = json.load(json_file)
with open('case1 temperature/data_pre_control/c_open_room2.json', 'r') as json_file:
    c_open_room2 = json.load(json_file)
with open('case1 temperature/data_pre_control/c_open_room3.json', 'r') as json_file:
    c_open_room3 = json.load(json_file)


with open('case1 temperature/data_pre_control/room2_ground.json', 'r') as json_file:
    r2_ground = json.load(json_file)
with open('case1 temperature/data_pre_control/room3_ground.json', 'r') as json_file:
    r3_ground = json.load(json_file)

with open('case1 temperature/data_pre_control/room2_test_predictions.json', 'r') as json_file:
    y2_prediction_list= json.load(json_file)
with open('case1 temperature/data_pre_control/room3_test_predictions.json', 'r') as json_file:
    y3_prediction_list= json.load(json_file)


test_num = 1000

optimal_state_sequence = dict()
optimal_control_sequence = dict()

for i in range(test_num):
    optimal_state_sequence[i] = [15]
    optimal_control_sequence[i] = []



total_time = 33
umax = 1
M = 1000


F_t = [0, 2]
G_t = [0, 30]
F_len = F_t[1] - F_t[0] + 1
G_len = G_t[1] - G_t[0] + 1
FG_len = G_t[1] + F_t[1] + 1


bound = 5
epsilon = 0.01




# Here is the list of the test data that ｜y_{tau, i} - \hat{Y}_{tau|s, i}｜ <= C, forall tau,s,i \in \{1,...,T\} \times \{0, ..., tau-1\} \times \{1,...,N\} doesn't hold.
list = []
for i in range(test_num):
    count = 0
    correct_count = 0
    for k in range(len(y2_prediction_list["0"][0])):
        for tau in range(k + 1, len(y2_prediction_list["0"][0])+1):
            if abs(r2_ground[i][tau] - y2_prediction_list[str(k)][i][tau-k-1]) <= c_close_room2[str(k)][str(tau)] and abs(r3_ground[i][tau] - y3_prediction_list[str(k)][i][tau-k-1]) <= c_close_room3[str(k)][str(tau)]:
                correct_count += 1
            count += 1
    if count != correct_count:
        list.append(i)

# print(list)