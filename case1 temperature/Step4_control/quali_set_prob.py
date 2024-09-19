from pyscipopt import *
import time
from quali_constraints_scip import *



def Solve_Prob(k, test_index, c_room2, c_room3, r2_trace_list, r3_trace_list):
    case1 = Model("case1")

    # create variables
    x, u, y2, y3 = {}, {}, {}, {}
    for i in range(total_time):
        x[i] = case1.addVar(vtype="C", name="controllable state") 
        y2[i] = case1.addVar(vtype="C", name="uncontrollable state 2") # 2 and 3 mean the room 2 and 3
        y3[i] = case1.addVar(vtype="C", name="uncontrollable state 3") 

    for i in range(total_time-1):
        u[i] = case1.addVar(vtype="C", name="control input")      

    # add specification constraints and objective
    obj = case1.addVar(vtype="C", name="obj")
    addConstr_qualitative(case1, test_index, x, u, y2, y3, k, c_room2, c_room3, r2_trace_list, r3_trace_list)
    case1.addCons(obj == sum(u[i]*u[i] for i in range(0, total_time-1)))
    case1.setObjective(obj, "minimize")

    # case1.setParam("limits/time", 50)
    case1.data = x,u

    # optimize
    case1.hideOutput()
    time_start = time.time()
    case1.optimize()
    time_cost = time.time() - time_start
    if case1.getStatus() == "optimal":
        x,u = case1.data
        state = [case1.getVal(x[i]) for i in range(len(x))]
        input = [case1.getVal(u[i]) for i in range(len(u))]
        return state, input, time_cost, "1"
    else:
        return None, None, None, "0"

        
    
