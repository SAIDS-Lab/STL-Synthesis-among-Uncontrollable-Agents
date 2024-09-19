from set_prob import *
from mpc import *






r1_trace_list, r2_trace_list, time = dict(), dict(), dict()
infeasible_time_list = []
# i is the index of the test data
for i in range (test_num):
    print("the executing index of the test data is", i+1)
    r1_trace_list[i], r2_trace_list[i], time[i] = dict(), dict(), dict()
    # k is the index of the time instant
    for k in range(total_time-1):
        mpc = MPC(k, i, c_close)
        r1_trace, r2_trace, time_cost, status = mpc.solve(i, r2_trace_list[i])
        if status != "1":
            print("The problem is infeasible at time", k)
            infeasible_time_list.append([i, k])
            break
        r1_trace_list[i][k] = r1_trace
        r2_trace_list[i][k] = r2_trace
        time[i][k] = time_cost
        # Note that r1_trace/r2_trace[:k+1] are real states and the remaining is the predicted states

with open('case2 motion planning/data_controlresults/r1_trace_list_closedloop.json', 'w') as f:
    json.dump(r1_trace_list, f)
with open('case2 motion planning/data_controlresults/r2_trace_list_closedloop.json', 'w') as f:
    json.dump(r2_trace_list, f)
with open('case2 motion planning/data_controlresults/time_closedloop.json', 'w') as f:
    json.dump(time, f)
with open(f'case2 motion planning/data_controlresults/infeasible_time_list.json', 'w') as f:
    json.dump(infeasible_time_list, f)


