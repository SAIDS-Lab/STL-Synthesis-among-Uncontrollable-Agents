from pyscipopt import *
import time

from parameters_control import *
from constraints_scip import *
import matplotlib.pyplot as plt


def Solve_Prob(k, test_index, r2_trace, r2_c):
    Robot = Model("case2")

    # create variables
    x1, u1 = {}, {}
    for i in range(total_time):
        for j in range(4):
            x1[i, j] = Robot.addVar(lb=-10, ub=10, vtype="C", name="controllable state") 

    for i in range(total_time-1):
        for j in range(2):
            u1[i, j] = Robot.addVar(lb=-umax, ub=umax, vtype="C") 
    # add specification constraints
    G_track_mu_4, q = addConstr(Robot, test_index, x1, u1, r2_trace, k, r2_c)
    # set objective
    obj = Robot.addVar(vtype="C", name="obj")
    Robot.addCons(obj == sum(0.03*sum(x1[i, j]*x1[i, j] for j in [1,3])  + 0.97*sum(u1[i, j]*u1[i, j] for j in range(2)) for i in range(0, total_time-1)))
    Robot.setObjective(obj, "minimize")
    Robot.data = x1, u1,G_track_mu_4, q

    # optimize
    Robot.hideOutput()
    time_start = time.time()
    Robot.optimize()
    # print("Time cost:", time.time() - time_start)
    comp_time = time.time() - time_start
    if Robot.getStatus() == "optimal":
        x1, u1, G_track_mu_4, q = Robot.data
        state = [[Robot.getVal(x1[i, j]) for j in range(4)] for i in range (total_time)]
        input = [[Robot.getVal(u1[i, j]) for j in range(2)] for i in range (total_time-1)]
        return state, input, comp_time, "1"
    else:
        return None, None, None, "0"
    
    




