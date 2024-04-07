
from parameters_control import *
from pyscipopt import *


def addConstr(model, x, u, y2, y3, y2_trace, y3_trace, k, c_room2, c_room3):
    # y2 and y3 will be used if we use KKT condition (see lines 73-81), otherwise we only use y2_trace and y3_trace

    # system model constraints
    # known state
    for i in range(0, k+1):
        model.addCons(x[i] == optimal_state_sequence[i])  
    for i in range(0, k):
        model.addCons(u[i] == optimal_control_sequence[i])     
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


    G = model.addVar(vtype="B")
    mu_or_F_mu = {}
    F_mu = {} 
    mu = {}  # mu corresponds to x-y2<bound \wedge x-y2>-bound \wedge x-y3<bound \wedge x-y3>-bound
    mu_r2, mu_r2_2 =  {}, {}
    mu_r3, mu_r3_2 =  {}, {}
    vlambda, temp_result = {}, {}
    for i in range(GF_len):
        mu[i] = model.addVar(vtype="B") 
        mu_r2[i] = model.addVar(vtype="B") 
        mu_r3[i] = model.addVar(vtype="B") 
        vlambda[i] = model.addVar(vtype="C") 
        temp_result[i] = model.addVar(vtype="C") 
        for j in range(2):
            mu_r2_2[i, j] = model.addVar(vtype="B") 
            mu_r3_2[i, j] = model.addVar(vtype="B") 
    for i in range(G_len):
        mu_or_F_mu[i] = model.addVar(vtype="B") 
        F_mu[i] = model.addVar(vtype="B") 

    model.addCons(G == 1)
    for i in range(G_len):
        model.addCons(G <= mu_or_F_mu[i])
    model.addCons(G >= 1- G_len + sum(mu_or_F_mu[i] for i in range(G_len)))
    for i in range(G_len):
        # encode for mu_or_F_mu
        model.addCons(mu_or_F_mu[i] >= mu[i])
        model.addCons(mu_or_F_mu[i] >= F_mu[i])
        model.addCons(mu_or_F_mu[i] <= mu[i] + F_mu[i])
        # encode for F_mu
        for j in range(F_len):
            model.addCons(F_mu[i] >= mu[i+j])
        model.addCons(F_mu[i] <= 1- F_len + sum(mu[i+j] for j in range(F_len)))

    # for the predicate which is the conjunction of room 2 and 3
    for i in range(GF_len):
        for j in range(2):
            model.addCons(mu[i] <= mu_r2_2[i, j])
            model.addCons(mu[i] <= mu_r3_2[i, j])
        model.addCons(mu[i] >= 1- 4 + sum(mu_r2_2[i, j] + mu_r3_2[i, j] for j in range(2)))

    for i in range(GF_len): 
        if i > k:
            # for room 2
            # for this constraint, we use "y2[i+G_t[0]] ==  (y2_trace[i+G_t[0]] - C_1*room2_sigma[i+G_t[0]])" to replace KKT (see below)
            model.addCons(x[i+G_t[0]] - (y2_trace[i+G_t[0]] - c_room2[str(k)][str(i+G_t[0])]) - bound <= M * (1 - mu_r2_2[i, 0]) - epsilon)
            # we can also use the following KKT condition to solve the inner optimization problem
            # BUT we use the explicit way as above in this case study since the predicate is very simple
            # model.addCons(x[i+G_t[0]] - y2[i+G_t[0]] - bound <= M * (1 - mu_r2_2[i, 0])- epsilon)
            # the constraints of the inner optimization problem is (y-yhat)^2 <= C^2 
            # model.addCons(1 + vlambda[i]*2*(y2[i+G_t[0]] - y2_trace[i+G_t[0]]) == 0)
            # model.addCons(vlambda[i] >= 0)
            # model.addCons(temp_result[i] == (y2[i+G_t[0]] - y2_trace[i+G_t[0]])*(y2[i+G_t[0]] - y2_trace[i+G_t[0]]) - (c_room2[str(k)][str(i+G_t[0])])*(c_room2[str(k)][str(i+G_t[0])]))
            # model.addCons(temp_result[i] <= 0)
            # model.addCons(vlambda[i]*temp_result[i] == 0)
            
            model.addCons(- bound - x[i+G_t[0]] + (y2_trace[i+G_t[0]] + c_room2[str(k)][str(i+G_t[0])]) <= M * (1 - mu_r2_2[i, 1])- epsilon)

            # for room 3
            model.addCons(x[i+G_t[0]] - (y3_trace[i+G_t[0]] - c_room3[str(k)][str(i+G_t[0])]) - bound <= M * (1 - mu_r3_2[i, 0])- epsilon)
            model.addCons(- bound - x[i+G_t[0]] + (y3_trace[i+G_t[0]] + c_room3[str(k)][str(i+G_t[0])]) <= M * (1 - mu_r3_2[i, 1])- epsilon)
        else:
            model.addCons(x[i+G_t[0]] - y2_trace[i+G_t[0]] - bound <= M * (1 - mu_r2_2[i, 0])- epsilon)
            model.addCons(-bound - x[i+G_t[0]] + y2_trace[i+G_t[0]] <= M * (1 - mu_r2_2[i, 1])- epsilon)
            model.addCons(x[i+G_t[0]] - y3_trace[i+G_t[0]] - bound <= M * (1 - mu_r3_2[i, 0])- epsilon)
            model.addCons(-bound - x[i+G_t[0]] + y3_trace[i+G_t[0]] <= M * (1 - mu_r3_2[i, 1])- epsilon)



