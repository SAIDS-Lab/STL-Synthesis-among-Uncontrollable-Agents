from set_prob import *
from para_collectdata import *
import random


class MPC:
    def __init__(self, k, horizon = total_time):
        self.horizon = horizon
        self.k = k
        self.state_r1 = None
        self.input_r1 = None
        self.state_r2 = None
        self.input_r2 = None

    def solve(self, optimal_state_r2, optimal_control_r2):

        flag, x2, u2 = Solve_Prob(self, self.k, optimal_state_r2, optimal_control_r2)
        # optimized results
        if flag == 1:
            dist_x_r2 = random.uniform(-random_p, random_p)
            dist_y_r2 = random.uniform(-random_p, random_p)
            optimal_state_r2.append([x2[self.k+1][0]+dist_x_r2, x2[self.k+1][1], x2[self.k+1][2]+dist_y_r2, x2[self.k+1][3]])
            optimal_control_r2.append([u2[self.k][j] for j in range(2)])
            return flag, optimal_state_r2, optimal_control_r2
        else:
            return flag, 2, 3

