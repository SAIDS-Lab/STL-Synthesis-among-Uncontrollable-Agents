from pyscipopt import *
import time
from constraints_scip import *
import matplotlib.pyplot as plt


def Solve_Prob(k, r2_trace, r3_trace, c_room2, c_room3):
    case1 = Model("case1")

    # create variables
    x, u, y2, y3 = {}, {}, {}, {}
    for i in range(total_time):
        x[i] = case1.addVar(vtype="C", name="controllable state") 
        y2[i] = case1.addVar(vtype="C", name="uncontrollable state 2") # 2 and 3 mean the room 2 and 3
        y3[i] = case1.addVar(vtype="C", name="uncontrollable state 3") 

    for i in range(total_time-1):
        u[i] = case1.addVar(vtype="C", name="control input")      

    # add specification constraints
    addConstr(case1, x, u, y2, y3, r2_trace, r3_trace, k, c_room2, c_room3)
    # set objective
    obj = case1.addVar(vtype="C", name="obj")
    case1.addCons(obj == sum((x[i]-r2_trace[i])*(x[i]-r2_trace[i]) + (x[i]-r3_trace[i])*(x[i]-r3_trace[i]) for i in range(0, total_time-1)))
    case1.setObjective(obj, "minimize")
    case1.data = x,u

    # optimize
    case1.hideOutput()
    time_start = time.time()
    case1.optimize()
    time_cost = time.time() - time_start
    if case1.getStatus() == "optimal":
        x,u = case1.data
        state = [case1.getVal(x[i]) for i in range (len(x))]
        input = [case1.getVal(u[i]) for i in range (len(u))]
        return state, input, time_cost
    else:
        plt.plot(r2_trace, label = "Temperature Trace 2")
        plt.plot(r3_trace, label = "Temperature Trace 3") 
        plt.legend() 
        plt.show()
        raise Exception("Unfortunately, we did not find a solution, and the predicted temperature is shown in the figure.")
        
    




