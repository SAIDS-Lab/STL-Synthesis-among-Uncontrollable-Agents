
from set_prob import *
from mpc import *

r1_trace_list, r2_trace_list, r3_trace_list, time = dict(), dict(), dict(), dict()
# i is the index of the test data
for i in range (10):
    print("the executing index of the test data is", i+1)
    r1_trace_list[i], r2_trace_list[i], r3_trace_list[i], time[i] = dict(), dict(), dict(), dict()
    mpc = MPC(0, i, c_open_room2, c_open_room3)
    r1_trace, r2_trace, r3_trace, time_cost = mpc.solve()
    r1_trace_list[i] = r1_trace
    r2_trace_list[i] = r2_trace
    r3_trace_list[i] = r3_trace
    time[i] = time_cost
    # Note that r1_trace/r2_trace/r3_trace[:k+1] are real states and the remaining is the predicted states

with open('data_controlresults/r1_trace_list_openloop.json', 'w') as f:
    json.dump(r1_trace_list, f)
with open('data_controlresults/r2_trace_list_openloop.json', 'w') as f:
    json.dump(r2_trace_list, f)
with open('data_controlresults/r3_trace_list_openloop.json', 'w') as f:
    json.dump(r3_trace_list, f)
with open('data_controlresults/time_openloop.json', 'w') as f:
    json.dump(time, f)


