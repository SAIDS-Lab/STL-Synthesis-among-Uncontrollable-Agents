from pyscipopt import *
from para_collectdata import *
from constraints_scip import *


def Solve_Prob(model, k, optimal_state_r2, optimal_control_r2):
    Robot = Model("case1_collect_data")

    # create variables
    x2, u2 = {}, {}
    for i in range(total_time):
        for j in range(4):
            x2[i, j] = Robot.addVar(lb=-10, ub=10, vtype="C", name="uncontrollable state") 

    for i in range(total_time-1):
        for j in range(2):
            u2[i, j] = Robot.addVar(lb=-umax, ub=umax, vtype="C") 

    

    # add specification constraints
    addConstr(Robot, x2, u2, k, optimal_state_r2, optimal_control_r2)

    # set objective
    obj = Robot.addVar(vtype="C", name="obj")
    Robot.addCons(obj == sum(0.55*sum(x2[i, j]*x2[i, j] for j in [1,3])  + 0.45*sum(u2[i, j]*u2[i, j] for j in range(2)) for i in range(0, total_time-1)))
    Robot.setObjective(obj, "minimize")
    Robot.data = x2, u2

    # optimize
    Robot.hideOutput()
    Robot.optimize()
    # print("Time cost:", time.time() - time_start)
    if Robot.getStatus() == "optimal":
        x2, u2 = Robot.data
        state_r2 = [[Robot.getVal(x2[i, j]) for j in range(4)] for i in range (total_time)]
        input_r2 = [[Robot.getVal(u2[i, j]) for j in range(2)] for i in range (total_time-1)]
        return 1, state_r2, input_r2
    else:
        print("Unfortunately, we did not find a solution.")
        return 0, 2, 3
    
    




