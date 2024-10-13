
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
        model.addCons(x[i+1] == x[i] + 2*(0.06*(5-x[i]) + 0.08*(55-x[i])*u[i]))
    # physical constraints
    for i in range(k+1, total_time):
        model.addCons(x[i] >= 0)
        model.addCons(x[i] <= 45)
    for i in range(k, total_time-1):
        model.addCons(u[i] >= 0)
        model.addCons(u[i] <= 1)

    FGmu1 = model.addVar(vtype="C")
    Gmu1 = {}
    r_mu1 = {}  # mu1 corresponds to x-y2<bound \wedge x-y2>-bound \wedge x-y3<bound \wedge x-y3>-bound
    r_mu1_r2, r_mu1_r2_temp =  {}, {}
    r_mu1_r3, r_mu1_r3_temp =  {}, {}
    
    for i in range(F_t[0], F_t[1]+1):
        Gmu1[i] = model.addVar(vtype="C")
    for i in range(FG_len):
        r_mu1[i] = model.addVar(vtype="C") 
        for j in range(2):
            r_mu1_r2[i, j] = model.addVar(vtype="C") 
            r_mu1_r3[i, j] = model.addVar(vtype="C") 
            for s in range(k+1):
                r_mu1_r2_temp[i, j, s] = model.addVar(vtype="C") 
                r_mu1_r3_temp[i, j, s] = model.addVar(vtype="C")

    p_Gmu1 = {}
    for i in range(F_t[0], F_t[1]+1):
        for j in range(G_len):
            p_Gmu1[i, j] = model.addVar(vtype="B")
    for i in range(F_t[0], F_t[1]+1):
        model.addCons(sum(p_Gmu1[i, j] for j in range(G_len)) == 1)
        for j in range(G_len):
            model.addCons(Gmu1[i] <= r_mu1[i+j])
            model.addCons(r_mu1[i+j] - (1-p_Gmu1[i, j])*M <= Gmu1[i])
            model.addCons(Gmu1[i] <= r_mu1[i+j] + (1-p_Gmu1[i, j])*M)

    p_FGmu1 = {}
    for i in range(F_t[0], F_t[1]+1):
        p_FGmu1[i] = model.addVar(vtype="B")
    for i in range(F_t[0], F_t[1]+1):
        model.addCons(FGmu1 >= Gmu1[i])
        model.addCons(Gmu1[i] - (1-p_FGmu1[i])*M <= FGmu1)
        model.addCons(FGmu1 <= Gmu1[i] + (1-p_FGmu1[i])*M)
    model.addCons(sum(p_FGmu1[i] for i in range(F_t[0], F_t[1]+1)) == 1)

    model.addCons(FGmu1 >= 0)

    # for the predicate which is the conjunction of room 2 and 3
    p_binary_mu1 = {}
    for i in range(FG_len):
        for j in range(4):
            p_binary_mu1[i, j] = model.addVar(vtype="B")
    for i in range(FG_len):
        model.addCons(sum(p_binary_mu1[i, j] for j in range(4)) == 1)
        for j in range(2):
            model.addCons(r_mu1[i] <= r_mu1_r2[i, j])
            model.addCons(r_mu1[i] <= r_mu1_r3[i, j])
            model.addCons(r_mu1_r2[i, j] - (1-p_binary_mu1[i, j])*M <= r_mu1[i])
            model.addCons(r_mu1[i] <= r_mu1_r2[i, j] + (1-p_binary_mu1[i, j])*M)
            model.addCons(r_mu1_r3[i, j] - (1-p_binary_mu1[i, j+2])*M <= r_mu1[i])
            model.addCons(r_mu1[i] <= r_mu1_r3[i, j] + (1-p_binary_mu1[i, j+2])*M)

    for i in range(FG_len): 
        if i > k:
            if k == 0: 
                # open loop; also the first time step of closed loop
                # for room 2 mu1
                # for this constraint, we use "y2[i] ==  (y2_trace[i] - c_room2[str(k)][i])" to replace KKT (see below)
                model.addCons(r_mu1_r2[i, 0] == - x[i] + r2_trace_list[k][i] - c_room2[str(k)][str(i)] + bound)
                model.addCons(r_mu1_r2[i, 1] == x[i] - r2_trace_list[k][i] - c_room2[str(k)][str(i)] + bound)
                # for room 3 mu1
                model.addCons(r_mu1_r3[i, 0] == - x[i] + r3_trace_list[k][i] - c_room3[str(k)][str(i)] + bound)
                model.addCons(r_mu1_r3[i, 1] == x[i] - r3_trace_list[k][i] - c_room3[str(k)][str(i)] + bound)
            else: 
                for s in range(k+1):
                    # for room 2 mu1
                    model.addCons(r_mu1_r2_temp[i, 0, s] == - x[i] + r2_trace_list[s][i] - c_room2[str(s)][str(i)] + bound)
                    model.addCons(r_mu1_r2_temp[i, 1, s] == x[i] - r2_trace_list[s][i] - c_room2[str(s)][str(i)] + bound)
                    # for room 3 mu1
                    model.addCons(r_mu1_r3_temp[i, 0, s] == - x[i] + r3_trace_list[s][i] - c_room3[str(s)][str(i)] + bound)
                    model.addCons(r_mu1_r3_temp[i, 1, s] == x[i] - r3_trace_list[s][i] - c_room3[str(s)][str(i)] + bound)

                p_binary_mu1_r2 = {}
                p_binary_mu1_r3 = {}
                for s in range(k+1):
                    for j in range(2):
                        p_binary_mu1_r2[s, j] = model.addVar(vtype="B")
                        p_binary_mu1_r3[s, j] = model.addVar(vtype="B")
                for j in range(2):
                    model.addCons(sum(p_binary_mu1_r2[s, j] for s in range(k+1)) == 1)
                    model.addCons(sum(p_binary_mu1_r3[s, j] for s in range(k+1)) == 1)   
                for s in range(k+1):
                    for j in range(2):
                        model.addCons(r_mu1_r2[i, j] >= r_mu1_r2_temp[i, j, s])
                        model.addCons(r_mu1_r2_temp[i, j, s] - (1-p_binary_mu1_r2[s, j])*M <= r_mu1_r2[i, j])
                        model.addCons(r_mu1_r2[i, j] <= r_mu1_r2_temp[i, j, s] + (1-p_binary_mu1_r2[s, j])*M)
                        model.addCons(r_mu1_r3[i, j] >= r_mu1_r3_temp[i, j, s])
                        model.addCons(r_mu1_r3_temp[i, j, s] - (1-p_binary_mu1_r3[s, j])*M <= r_mu1_r3[i, j])
                        model.addCons(r_mu1_r3[i, j] <= r_mu1_r3_temp[i, j, s] + (1-p_binary_mu1_r3[s, j])*M)

        else:
            model.addCons(r_mu1_r2[i, 0] == - x[i] + r2_trace_list[k][i] + bound)
            model.addCons(r_mu1_r2[i, 1] == x[i] - r2_trace_list[k][i] + bound)
            model.addCons(r_mu1_r3[i, 0] == - x[i] + r3_trace_list[k][i] + bound)
            model.addCons(r_mu1_r3[i, 1] == x[i] - r3_trace_list[k][i] + bound)

    return FGmu1
