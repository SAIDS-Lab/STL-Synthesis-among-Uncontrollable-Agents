
from quali_set_prob import *
from quali_mpc import *


# Note that due to the nonconvexity, the solver not being able to find a solution doesn't mean that the problem is infeasible.
# This function is used to check if the solution from the last time step is feasible when the solver cannot find a solution at the current time step.
# Note that if it reports that "Sorry, we still cannot find a solution at time k", it still doesn't mean that the problem is infeasible, since we only apply x and u from the last time instant. I am too lazy to extract and then apply all the variables that used in the optimization problem from last time instant. 
# in the folder "Step4_control", we separately wrote the qualitative and quantitative versions of the control problem. Actually, they can be easily combined. (too lazy to work on it)

r1_trace_list, r2_trace_list, r3_trace_list, time = dict(), dict(), dict(), dict()
infeasible_time_list = []
# i is the index of the test data
for i in range(test_num):
    print("the executing index of the test data is", i+1)
    r1_trace_list[i], r2_trace_list[i], r3_trace_list[i], time[i] = dict(), dict(), dict(), dict()
    # k is the index of the time instant
    for k in range(total_time-1):
        mpc = MPC(k, i, c_close_room2, c_close_room3)
        r1_trace, r2_trace, r3_trace, time_cost, status, u = mpc.solve(i, r2_trace_list[i], r3_trace_list[i])
        if status != "1":
            if k != 0:
                print("The solver cannot find a solution at time", k, ". Let's try the solution from the last time instant.")
                r1_trace, r2_trace, r3_trace, time_cost, status, u = mpc.check(i, r2_trace_list[i], r3_trace_list[i], last_x, last_u)
                if status == "1":
                    print("Actually, the problem is feasible at time", k)
        else:
            last_x = r1_trace
            last_u = u
        
        if status != "1":
            print("Sorry, we cannot find a solution at time", k)
            print("：- (")
            infeasible_time_list.append([i, k])
            break
        r1_trace_list[i][k] = r1_trace
        r2_trace_list[i][k] = r2_trace
        r3_trace_list[i][k] = r3_trace
        time[i][k] = time_cost
        # Note that r1_trace/r2_trace/r3_trace[:k+1] are real states and the remaining is the predicted states

with open(f'case1 temperature/data_controlresults/r1_trace_list_closedloop_qualitative.json', 'w') as f:
    json.dump(r1_trace_list, f)
with open(f'case1 temperature/data_controlresults/r2_trace_list_closedloop_qualitative.json', 'w') as f:
    json.dump(r2_trace_list, f)
with open(f'case1 temperature/data_controlresults/r3_trace_list_closedloop_qualitative.json', 'w') as f:
    json.dump(r3_trace_list, f)
with open(f'case1 temperature/data_controlresults/time_closedloop_qualitative.json', 'w') as f:
    json.dump(time, f)
with open(f'case1 temperature/data_controlresults/infeasible_time_list_closedloop_qualitative.json', 'w') as f:
    json.dump(infeasible_time_list, f)
