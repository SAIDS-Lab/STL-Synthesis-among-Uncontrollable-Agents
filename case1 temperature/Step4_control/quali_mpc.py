from quali_set_prob import *
from parameters_control import *



class MPC:
    def __init__(self, k, test_index, c_room2, c_room3, horizon = total_time):
        self.horizon = horizon
        self.k = k
        self.state = None
        self.input = None
        self.test_index = test_index
        self.c_room2 = c_room2
        self.c_room3 = c_room3

    def solve(self, test_index, r2_trace_list, r3_trace_list):
        r2_trace = r2_ground[self.test_index][:self.k+1]
        r3_trace = r3_ground[self.test_index][:self.k+1]
        for tau in range(len(y2_prediction_list[str(self.k)][self.test_index])):
            r2_trace.append(y2_prediction_list[str(self.k)][self.test_index][tau])
            r3_trace.append(y3_prediction_list[str(self.k)][self.test_index][tau])
        
        r2_trace_list[self.k] = r2_trace
        r3_trace_list[self.k] = r3_trace
            
        x, u, time, status = Solve_Prob(self.k, test_index, self.c_room2, self.c_room3, r2_trace_list, r3_trace_list)

        # optimized results
        if status == "1":  # feasible
            self.state = x
            self.input = u
            optimal_state_sequence[test_index].append(x[self.k+1])
            optimal_control_sequence[test_index].append(u[self.k])
            return x, r2_trace, r3_trace, time, status
        else:
            return None, None, None, None, status

   