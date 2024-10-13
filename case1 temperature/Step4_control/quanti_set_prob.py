from pyscipopt import *
import time
from quanti_constraints_scip import *



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
    r = addConstr_quantitative(case1, test_index, x, u, y2, y3, k, c_room2, c_room3, r2_trace_list, r3_trace_list)
    # these are used to make the result more smooth
    # for i in range(7):
    #     case1.addCons((x[i+1]-x[i])**2 <= 2)
    # for i in range(7, total_time-1):
    #     case1.addCons((x[i+1]-x[i])**2 <= 0.4)
    case1.addCons(obj == r)
    case1.setObjective(obj, "maximize")


    case1.setParam("limits/time", 50)
    case1.data = x, u

    # optimize
    case1.hideOutput()
    time_start = time.time()
    case1.optimize()
    time_cost = time.time() - time_start
    if case1.getStatus() == "optimal":
        x, u = case1.data
        state = [case1.getVal(x[i]) for i in range(len(x))]
        input = [case1.getVal(u[i]) for i in range(len(u))]
        return state, input, time_cost, "1"
    else:
        return None, None, None, "0"

        
    



def check_Prob(k, test_index, c_room2, c_room3, r2_trace_list, r3_trace_list, last_x, last_u):
    case1_check = Model("case1_check")

    # create variables
    x, u, y2, y3 = {}, {}, {}, {}
    for i in range(total_time):
        x[i] = case1_check.addVar(vtype="C", name="controllable state") 
        y2[i] = case1_check.addVar(vtype="C", name="uncontrollable state 2") # 2 and 3 mean the room 2 and 3
        y3[i] = case1_check.addVar(vtype="C", name="uncontrollable state 3") 
    for i in range(total_time-1):
        u[i] = case1_check.addVar(vtype="C", name="control input")      

    # add specification constraints and objective
    obj = case1_check.addVar(vtype="C", name="obj")
    r= addConstr_quantitative(case1_check, test_index, x, u, y2, y3, k, c_room2, c_room3, r2_trace_list, r3_trace_list)

    # try the solution from the last time step
    for i in range(0, k+1):
        case1_check.addCons(x[i] == last_x[i])  
    for i in range(0, k):
        case1_check.addCons(u[i] == last_u[i])   
    # case1_check.addCons(obj == r_G)
    # case1_check.setObjective(obj, "maximize")
        
    case1_check.setParam("limits/time", 50)
    case1_check.data = x, u

    # optimize
    case1_check.hideOutput()
    time_start = time.time()
    case1_check.optimize()
    time_cost = time.time() - time_start
    if case1_check.getStatus() == "optimal":
        x, u = case1_check.data
        state = [case1_check.getVal(x[i]) for i in range(len(x))]
        input = [case1_check.getVal(u[i]) for i in range(len(u))]
        return state, input, time_cost, "1"
    else:
        return None, None, None, "0"

