from set_prob import *
# from Print_plot import *
from parameters_control import *


class MPC:
    def __init__(self, k, i, r2_c, horizon = total_time):
        self.horizon = horizon
        self.k = k
        self.state = None
        self.input = None
        self.i = i
        self.r2_c = r2_c

    def solve(self):
        r2_trace = r2_ground[self.i][:self.k+1]
        for tau in range(len(y2_prediction_list[str(self.k)][self.i])):
            r2_trace.append(y2_prediction_list[str(self.k)][self.i][tau])

        x, u, time = Solve_Prob(self.k, r2_trace, self.r2_c)
        # optimized results
        self.state = x
        self.input = u
        optimal_state_sequence.append(x[self.k+1])
        optimal_control_sequence.append(u[self.k])
        return x, r2_trace, time