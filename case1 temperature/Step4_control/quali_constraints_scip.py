
from parameters_control import *
from pyscipopt import *




def addConstr_qualitative(model, test_index, x, u, y2, y3, k, c_room2, c_room3, r2_trace_list, r3_trace_list):
    # y2 and y3 will be used if we use KKT condition (see lines 81-89), otherwise we only use r2_trace_list and r3_trace_list

    # system model constraints
    # known state
    for i in range(0, k+1):
        model.addCons(x[i] == optimal_state_sequence[test_index][i])  
    for i in range(0, k):
        model.addCons(u[i] == optimal_control_sequence[test_index][i])     
    # model [1,T]
    for i in range(k, total_time-1):
        model.addCons(x[i+1] == x[i] + 2*(0.06*(5-x[i]) + 0.08*(55-x[i])*u[i]))
    # physical constraints
    for i in range(k+1, total_time):
        model.addCons(x[i] >= 0)
        model.addCons(x[i] <= 45)
    for i in range(k, total_time-1):
        model.addCons(u[i] >= 0)
        model.addCons(u[i] <= 1)

    mu1, mu2 = {}, {}  # mu corresponds to x-y2<bound \wedge x-y2>-bound \wedge x-y3<bound \wedge x-y3>-bound
    mu1_r2_2 =  {}
    mu1_r3_2 =  {}
    vlambda, temp_result = {}, {}  # they are for kkt
    for i in range(FG_len):
        mu1[i] = model.addVar(vtype="B") 
        mu2[i] = model.addVar(vtype="B")
        vlambda[i] = model.addVar(vtype="C") 
        temp_result[i] = model.addVar(vtype="C") 
        for j in range(2):
            mu1_r2_2[i, j] = model.addVar(vtype="B") 
            mu1_r3_2[i, j] = model.addVar(vtype="B") 

    Gmu1 = {}
    for i in range(F_t[0], F_t[1]+1):
        Gmu1[i] = model.addVar(vtype="B")
    FGmu1 = model.addVar(vtype="B")
    
    for i in range(F_t[0], F_t[1]+1):
        for j in range(G_len):
            model.addCons(Gmu1[i] <= mu1[i+j])
        model.addCons(Gmu1[i] >= 1- G_len + sum(mu1[i+j] for j in range(G_len)))
    for i in range(F_t[0], F_t[1]+1):
        model.addCons(FGmu1 >= Gmu1[i])
    model.addCons(FGmu1 <= sum(Gmu1[i] for i in range(F_t[0], F_t[1]+1)))

    model.addCons(FGmu1 == 1)


    # for the predicate which is the conjunction of room 2 and 3
    for i in range(FG_len):
        for j in range(2):
            model.addCons(mu1[i] <= mu1_r2_2[i, j])
            model.addCons(mu1[i] <= mu1_r3_2[i, j])
        model.addCons(mu1[i] >= 1- 4 + sum(mu1_r2_2[i, j] + mu1_r3_2[i, j] for j in range(2)))

    q1 = {}
    for i in range(FG_len - k):
        for s in range(k+1):
            for j in range(4):
                q1[i, s, j] = model.addVar(vtype="B")

    for i in range(FG_len): 
        if i > k:
            if k == 0: 
                # open loop; also the first time step of closed loop
                # for room 2 mu1
                # for this constraint, we use "y2[i] ==  (y2_trace[i] - c_room2[i])" to replace KKT (see below)
                model.addCons(x[i] - (r2_trace_list[k][i] - c_room2[str(k)][str(i)]) - bound <= M * (1 - mu1_r2_2[i, 0]) - epsilon)
                # # we can also use the following KKT condition to solve the inner optimization problem
                # # BUT we use the explicit way as above in this case study since the predicate is very simple
                # model.addCons(x[i] - y2[i] - bound <= M * (1 - mu1_r2_2[i, 0])- epsilon)
                # # the constraints of the inner optimization problem is (y-yhat)^2 <= C^2 
                # model.addCons(1 + vlambda[i]*2*(y2[i] - r2_trace_list[k][i]) == 0)
                # model.addCons(vlambda[i] >= 0)
                # model.addCons(temp_result[i] == (y2[i] - r2_trace_list[k][i])*(y2[i] - r2_trace_list[k][i]) - (c_room2[str(k)][str(i)])*(c_room2[str(k)][str(i)]))
                # model.addCons(temp_result[i] <= 0)
                # model.addCons(vlambda[i]*temp_result[i] == 0)
                
                model.addCons(- bound - x[i] + (r2_trace_list[k][i] + c_room2[str(k)][str(i)]) <= M * (1 - mu1_r2_2[i, 1])- epsilon)

                # for room 3 mu1
                model.addCons(x[i] - (r3_trace_list[k][i] - c_room3[str(k)][str(i)]) - bound <= M * (1 - mu1_r3_2[i, 0])- epsilon)
                model.addCons(- bound - x[i] + (r3_trace_list[k][i] + c_room3[str(k)][str(i)]) <= M * (1 - mu1_r3_2[i, 1])- epsilon)

            else: 
                # closed loop; here we set M'= M, epsilon' = epsilon
                # for room 2 mu1
                for s in range(k+1):
                    model.addCons(x[i] - (r2_trace_list[s][i] - c_room2[str(s)][str(i)]) - bound <= M * (1 - mu1_r2_2[i, 0]) - epsilon + M*(1 - q1[i-k, s, 0]) - epsilon)
                    model.addCons(- x[i] + (r2_trace_list[s][i] - c_room2[str(s)][str(i)]) + bound + M * (1 - mu1_r2_2[i, 0]) <= M*q1[i-k, s, 0])
                model.addCons(sum(q1[i-k, s, 0] for s in range(k+1)) >=1)
                for s in range(k+1):
                    model.addCons(- bound - x[i] + (r2_trace_list[s][i] + c_room2[str(s)][str(i)]) <= M * (1 - mu1_r2_2[i, 1])- epsilon + M*(1 - q1[i-k, s, 1]) - epsilon)
                    model.addCons(x[i] - (r2_trace_list[s][i] + c_room2[str(s)][str(i)]) + bound <= M*q1[i-k, s, 1])
                model.addCons(sum(q1[i-k, s, 1] for s in range(k+1)) >=1)

                # for room 3 mu1
                for s in range(k+1):
                    model.addCons(x[i] - (r3_trace_list[s][i] - c_room3[str(s)][str(i)]) - bound <= M * (1 - mu1_r3_2[i, 0]) - epsilon + M*(1 - q1[i-k, s, 2]) - epsilon)
                    model.addCons(- x[i] + (r3_trace_list[s][i] - c_room3[str(s)][str(i)]) + bound + M * (1 - mu1_r3_2[i, 0]) <= + M*q1[i-k, s, 2])
                model.addCons(sum(q1[i-k, s, 2] for s in range(k+1)) >=1)
                for s in range(k+1):
                    model.addCons(- bound - x[i] + (r3_trace_list[s][i] + c_room3[str(s)][str(i)]) <= M * (1 - mu1_r3_2[i, 1])- epsilon + M*(1 - q1[i-k, s, 3]) - epsilon)
                    model.addCons(x[i] - (r3_trace_list[s][i] + c_room3[str(s)][str(i)]) + bound <= M*q1[i-k, s, 3])
                model.addCons(sum(q1[i-k, s, 3] for s in range(k+1)) >=1)

        else:
            model.addCons(x[i] - r2_trace_list[k][i] - bound <= M * (1 - mu1_r2_2[i, 0])- epsilon)
            model.addCons(-bound - x[i] + r2_trace_list[k][i] <= M * (1 - mu1_r2_2[i, 1])- epsilon)
            model.addCons(x[i] - r3_trace_list[k][i] - bound <= M * (1 - mu1_r3_2[i, 0])- epsilon)
            model.addCons(-bound - x[i] + r3_trace_list[k][i] <= M * (1 - mu1_r3_2[i, 1])- epsilon)
