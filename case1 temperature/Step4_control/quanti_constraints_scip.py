
from parameters_control import *
from pyscipopt import *



def addConstr_quantitative(model, test_index, x, u, y2, y3, k, c_room2, c_room3, r2_trace_list, r3_trace_list):
    # y2 and y3 will be used if we use KKT condition (see lines 81-89), otherwise we only use r2_trace_list and r3_trace_list

    # system model constraints
    # known state
    for i in range(0, k+1):
        model.addCons(x[i] == optimal_state_sequence[test_index][i])  
    for i in range(0, k):
        model.addCons(u[i] == optimal_control_sequence[test_index][i])     
    # model [1,T]
    for i in range(k, total_time-1):
        # model.addCons(x[i+1] == x[i] + 4*u[i])
        model.addCons(x[i+1] == x[i] + 2*(0.06*(5-x[i]) + 0.08*(55-x[i])*u[i]))
    # physical constraints
    for i in range(k+1, total_time):
        model.addCons(x[i] >= 0)
        model.addCons(x[i] <= 45)
    for i in range(k, total_time-1):
        model.addCons(u[i] >= 0)
        model.addCons(u[i] <= 1)


    r_G = model.addVar(vtype="C")
    r_mu_or_F_mu = {}
    r_mu = {}  # mu corresponds to x-y2<bound \wedge x-y2>-bound \wedge x-y3<bound \wedge x-y3>-bound
    r_mu_r2, r_mu_r2_temp =  {}, {}
    r_mu_r3, r_mu_r3_temp =  {}, {}
    

    for i in range(GF_len):
        r_mu[i] = model.addVar(vtype="C") 
        for j in range(2):
            r_mu_r2[i, j] = model.addVar(vtype="C") 
            r_mu_r3[i, j] = model.addVar(vtype="C") 
            for s in range(k+1):
                r_mu_r2_temp[i, j, s] = model.addVar(vtype="C") 
                r_mu_r3_temp[i, j, s] = model.addVar(vtype="C")
    for i in range(G_len):
        r_mu_or_F_mu[i] = model.addVar(vtype="C") 

    model.addCons(r_G >= 1)
    p_binary_G = {}
    for i in range(1, G_len):
        p_binary_G[i] = model.addVar(vtype="B")
    model.addCons(sum(p_binary_G[i] for i in range(1, G_len)) == 1)
    for i in range(1, G_len):
        model.addCons(r_G <= r_mu_or_F_mu[i])
        model.addCons(r_mu_or_F_mu[i] - (1-p_binary_G[i])*M <= r_G)
        model.addCons(r_G <= r_mu_or_F_mu[i] + (1-p_binary_G[i])*M)


    p_binary_mu_or_F_mu = {}
    for i in range(G_len):
        for j in range(F_len):
            p_binary_mu_or_F_mu[i, j] = model.addVar(vtype="B")
    for i in range(G_len):
        # encode for mu_or_F_mu
        model.addCons(sum(p_binary_mu_or_F_mu[i, j] for j in range(F_len)) == 1)
        for j in range(F_len):
            model.addCons(r_mu_or_F_mu[i] >= r_mu[i+j])
            model.addCons(r_mu[i+j] - (1-p_binary_mu_or_F_mu[i, j])*M <= r_mu_or_F_mu[i])
            model.addCons(r_mu_or_F_mu[i] <= r_mu[i+j] + (1-p_binary_mu_or_F_mu[i, j])*M)

    
    # for the predicate which is the conjunction of room 2 and 3
    p_binary_mu = {}
    for i in range(GF_len):
        for j in range(4):
            p_binary_mu[i, j] = model.addVar(vtype="B")
    for i in range(GF_len):
        model.addCons(sum(p_binary_mu[i, j] for j in range(4)) == 1)
        for j in range(2):
            model.addCons(r_mu[i] <= r_mu_r2[i, j])
            model.addCons(r_mu[i] <= r_mu_r3[i, j])
            model.addCons(r_mu_r2[i, j] - (1-p_binary_mu[i, j])*M <= r_mu[i])
            model.addCons(r_mu[i] <= r_mu_r2[i, j] + (1-p_binary_mu[i, j])*M)
            model.addCons(r_mu_r3[i, j] - (1-p_binary_mu[i, j+2])*M <= r_mu[i])
            model.addCons(r_mu[i] <= r_mu_r3[i, j] + (1-p_binary_mu[i, j+2])*M)

    for i in range(GF_len): 
        if i > k:
            if k == 0: 
                # open loop; also the first time step of closed loop
                # for room 2
                # for this constraint, we use "y2[i] ==  (y2_trace[i] - c_room2[str(k)][i])" to replace KKT (see below)
                model.addCons(r_mu_r2[i, 0] == - x[i] + r2_trace_list[k][i] - c_room2[str(k)][str(i)] + bound)
                model.addCons(r_mu_r2[i, 1] == x[i] - r2_trace_list[k][i] - c_room2[str(k)][str(i)] + bound)
                # for room 3
                model.addCons(r_mu_r3[i, 0] == - x[i] + r3_trace_list[k][i] - c_room3[str(k)][str(i)] + bound)
                model.addCons(r_mu_r3[i, 1] == x[i] - r3_trace_list[k][i] - c_room3[str(k)][str(i)] + bound)
            else: 
                for s in range(k+1):
                    # for room 2
                    model.addCons(r_mu_r2_temp[i, 0, s] == - x[i] + r2_trace_list[s][i] - c_room2[str(s)][str(i)] + bound)
                    model.addCons(r_mu_r2_temp[i, 1, s] == x[i] - r2_trace_list[s][i] - c_room2[str(s)][str(i)] + bound)
                    # for room 3
                    model.addCons(r_mu_r3_temp[i, 0, s] == - x[i] + r3_trace_list[s][i] - c_room3[str(s)][str(i)] + bound)
                    model.addCons(r_mu_r3_temp[i, 1, s] == x[i] - r3_trace_list[s][i] - c_room3[str(s)][str(i)] + bound)

                p_binary_mu_r2 = {}
                p_binary_mu_r3 = {}
                for s in range(k+1):
                    for j in range(2):
                        p_binary_mu_r2[s, j] = model.addVar(vtype="B")
                        p_binary_mu_r3[s, j] = model.addVar(vtype="B")
                for j in range(2):
                    model.addCons(sum(p_binary_mu_r2[s, j] for s in range(k+1)) == 1)
                    model.addCons(sum(p_binary_mu_r3[s, j] for s in range(k+1)) == 1)   
                for s in range(k+1):
                    for j in range(2):
                        model.addCons(r_mu_r2[i, j] >= r_mu_r2_temp[i, j, s])
                        model.addCons(r_mu_r2_temp[i, j, s] - (1-p_binary_mu_r2[s, j])*M <= r_mu_r2[i, j])
                        model.addCons(r_mu_r2[i, j] <= r_mu_r2_temp[i, j, s] + (1-p_binary_mu_r2[s, j])*M)
                        model.addCons(r_mu_r3[i, j] >= r_mu_r3_temp[i, j, s])
                        model.addCons(r_mu_r3_temp[i, j, s] - (1-p_binary_mu_r3[s, j])*M <= r_mu_r3[i, j])
                        model.addCons(r_mu_r3[i, j] <= r_mu_r3_temp[i, j, s] + (1-p_binary_mu_r3[s, j])*M)
        else:
            model.addCons(r_mu_r2[i, 0] == - x[i] + r2_trace_list[k][i] + bound)
            model.addCons(r_mu_r2[i, 1] == x[i] - r2_trace_list[k][i] + bound)
            model.addCons(r_mu_r3[i, 0] == - x[i] + r3_trace_list[k][i] + bound)
            model.addCons(r_mu_r3[i, 1] == x[i] - r3_trace_list[k][i] + bound)

    return r_G



