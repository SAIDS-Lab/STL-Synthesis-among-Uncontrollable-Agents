from set_prob import *
from parameters_control import *



class MPC:
    def __init__(self, k, i, c_room2, c_room3, horizon = total_time):
        self.horizon = horizon
        self.k = k
        self.state = None
        self.input = None
        self.i = i
        self.c_room2 = c_room2
        self.c_room3 = c_room3

    def solve(self):
        r2_trace = r2_ground[self.i][:self.k+1]
        r3_trace = r3_ground[self.i][:self.k+1]
        for tau in range(len(y2_prediction_list[str(self.k)][self.i])):
            r2_trace.append(y2_prediction_list[str(self.k)][self.i][tau])
            r3_trace.append(y3_prediction_list[str(self.k)][self.i][tau])

        x, u, time = Solve_Prob(self.k, r2_trace, r3_trace, self.c_room2, self.c_room3)
        # optimized results
        self.state = x
        self.input = u
        optimal_state_sequence.append(x[self.k+1])
        optimal_control_sequence.append(u[self.k])
        return x, r2_trace, r3_trace, time

