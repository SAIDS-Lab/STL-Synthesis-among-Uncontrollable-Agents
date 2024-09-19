
from parameters_control import *
from pyscipopt import *





def addConstr(model, test_index, x1, u1, r2_trace_list, k, r2_c):

    # system model constraints
    # known state
    for i in range(0, k+1):
        for j in range(4):
            model.addCons(x1[i, j] == optimal_state_sequence[test_index][i][j])  
    for i in range(0, k):
        for j in range(2):
            model.addCons(u1[i, j] == optimal_control_sequence[test_index][i][j])  
    
    # model [1,T]
    for i in range(k, total_time-1):
        model.addCons(x1[i+1, 0] == x1[i, 0] + x1[i, 1] + 0.5*u1[i, 0])
        model.addCons(x1[i+1, 1] == x1[i, 1] + u1[i, 0])
        model.addCons(x1[i+1, 2] == x1[i, 2] + x1[i, 3] + 0.5*u1[i, 1])
        model.addCons(x1[i+1, 3] == x1[i, 3] + u1[i, 1])

    # physical constraints
    for i in range(k+1, total_time):
        model.addCons(x1[i, 0] >= 0)
        model.addCons(x1[i, 0] <= 10)
        model.addCons(x1[i, 1] >= -vmax)
        model.addCons(x1[i, 1] <= vmax)
        model.addCons(x1[i, 2] >= 0)
        model.addCons(x1[i, 2] <= 10)
        model.addCons(x1[i, 3] >= -vmax)
        model.addCons(x1[i, 3] <= vmax)

    G_track = model.addVar(vtype="B")
    G_track_mu, G_track_mu_4 = {}, {}  # mu is a mixed mu based on r1 and r2
    for i in range(G_track_len):
        G_track_mu[i] = model.addVar(vtype="B")
        for j in range (4):
            G_track_mu_4[i, j] = model.addVar(vtype="B")

    for i in range(G_track_len):
        model.addCons(G_track <= G_track_mu[i])
    model.addCons(G_track >= 1- G_track_len + sum(G_track_mu[i] for i in range(G_track_len)))

    # encode for mu
    for i in range(G_track_len):
        for j in range(4):
            model.addCons(G_track_mu[i] <= G_track_mu_4[i, j])
        model.addCons(G_track_mu[i] >= 1- 4 + sum(G_track_mu_4[i, j] for j in range(4)))

    q_track = {}
    for i in range(G_track_len - k - 1):
        for s in range(k+1):
            for j in range(4):
                q_track[i, s, j] = model.addVar(vtype="B")

    for i in range(G_track_len): 
        if G_track_t[0] + i > k:
            for s in range(k+1):
                model.addCons(-x1[G_track_t[0] + i, 0] + (r2_trace_list[s][G_track_t[0] + i][0] + r2_c[str(s)][str(i+G_track_t[0])]) - D <= M * (1 - G_track_mu_4[i, 0]) - 2 * epsilon + M*(1- q_track[i-k- 1, s, 0]))
                model.addCons(-(r2_trace_list[s][G_track_t[0] + i][0] + r2_c[str(s)][str(i+G_track_t[0])]) + x1[G_track_t[0] + i, 0] + D + M * (1 - G_track_mu_4[i, 0]) <=  +M*q_track[i-k- 1, s, 0])
                model.addCons(-(r2_trace_list[s][G_track_t[0] + i][0] - r2_c[str(s)][str(i+G_track_t[0])]) + x1[G_track_t[0] + i, 0] - D <= M * (1 - G_track_mu_4[i, 1]) -2 * epsilon + M*(1- q_track[i-k- 1, s, 1])) 
                model.addCons(-x1[G_track_t[0] + i, 0] + (r2_trace_list[s][G_track_t[0] + i][0] - r2_c[str(s)][str(i+G_track_t[0])]) + D + M * (1 - G_track_mu_4[i, 1]) <=  M*q_track[i-k- 1, s, 1])

                model.addCons(-x1[G_track_t[0] + i, 2] + (r2_trace_list[s][G_track_t[0] + i][1] + r2_c[str(s)][str(i+G_track_t[0])]) - D <= M * (1 - G_track_mu_4[i, 2]) - 2 * epsilon + M*(1- q_track[i-k- 1, s, 2]))
                model.addCons(-(r2_trace_list[s][G_track_t[0] + i][1] + r2_c[str(s)][str(i+G_track_t[0])]) + x1[G_track_t[0] + i, 2] + D + M * (1 - G_track_mu_4[i, 2]) <=  M*q_track[i-k- 1, s, 2])
                model.addCons(-(r2_trace_list[s][G_track_t[0] + i][1] - r2_c[str(s)][str(i+G_track_t[0])]) + x1[G_track_t[0] + i, 2] - D <= M * (1 - G_track_mu_4[i, 3]) -2 * epsilon + M*(1- q_track[i-k- 1, s, 3])) 
                model.addCons(-x1[G_track_t[0] + i, 2] + (r2_trace_list[s][G_track_t[0] + i][1] - r2_c[str(s)][str(i+G_track_t[0])]) + D + M * (1 - G_track_mu_4[i, 3]) <=  M*q_track[i-k- 1, s, 3])

            model.addCons(sum(q_track[i-k-1, s, 0] for s in range(k+1)) >=1)
            model.addCons(sum(q_track[i-k-1, s, 1] for s in range(k+1)) >=1)
            model.addCons(sum(q_track[i-k-1, s, 2] for s in range(k+1)) >=1)
            model.addCons(sum(q_track[i-k-1, s, 3] for s in range(k+1)) >=1)

            # model.addCons(-x1[G_track_t[0] + i, 0] + (r2_trace[G_track_t[0] + i][0] + r2_c[str(k)][str(i+G_track_t[0])]) - D <= M * (1 - G_track_mu_4[i, 0]) - epsilon)
            # model.addCons(-(r2_trace[G_track_t[0] + i][0] - r2_c[str(k)][str(i+G_track_t[0])]) + x1[G_track_t[0] + i, 0] - D <= M * (1 - G_track_mu_4[i, 1]) - epsilon)
            # model.addCons(-x1[G_track_t[0] + i, 2] + (r2_trace[G_track_t[0] + i][1] + r2_c[str(k)][str(i+G_track_t[0])]) - D <= M * (1 - G_track_mu_4[i, 2]) - epsilon)
            # model.addCons(-(r2_trace[G_track_t[0] + i][1]-r2_c[str(k)][str(i+G_track_t[0])]) + x1[G_track_t[0] + i, 2] - D <= M * (1 - G_track_mu_4[i, 3]) - epsilon)
        else:
            model.addCons(-x1[G_track_t[0] + i, 0] + r2_trace_list[k][G_track_t[0] + i][0] - D <= M * (1 - G_track_mu_4[i, 0]) - epsilon)
            model.addCons(-r2_trace_list[k][G_track_t[0] + i][0] + x1[G_track_t[0] + i, 0] - D <= M * (1 - G_track_mu_4[i, 1]) - epsilon)
            model.addCons(-x1[G_track_t[0] + i, 2] + r2_trace_list[k][G_track_t[0] + i][1] - D <= M * (1 - G_track_mu_4[i, 2]) - epsilon)
            model.addCons(-r2_trace_list[k][G_track_t[0] + i][1] + x1[G_track_t[0] + i, 2] - D <= M * (1 - G_track_mu_4[i, 3]) - epsilon)

    G_obs = model.addVar(vtype="B")
    G_obs_mu = {}
    G_obs1_mu, G_obs2_mu, G_obs3_mu = {}, {}, {}
    G_obs1_mu_4, G_obs2_mu_4, G_obs3_mu_4 = {}, {}, {}
    for i in range(G_obs_len):
        G_obs_mu[i] = model.addVar(vtype="B")
        G_obs1_mu[i] = model.addVar(vtype="B")
        G_obs2_mu[i] = model.addVar(vtype="B")
        G_obs3_mu[i] = model.addVar(vtype="B")
        for j in range(4):
            G_obs1_mu_4[i, j] = model.addVar(vtype="B")
            G_obs2_mu_4[i, j] = model.addVar(vtype="B")
            G_obs3_mu_4[i, j] = model.addVar(vtype="B")
            
    for i in range(G_obs_len):
        model.addCons(G_obs <= G_obs_mu[i])
    model.addCons(G_obs >= 1- G_obs_len + sum(G_obs_mu[i] for i in range(G_obs_len)))


    for i in range(G_obs_len):
        model.addCons(G_obs_mu[i] <= G_obs1_mu[i])
        model.addCons(G_obs_mu[i] <= G_obs2_mu[i])
        model.addCons(G_obs_mu[i] <= G_obs3_mu[i])
        model.addCons(G_obs_mu[i] >= 1 - 3 + G_obs1_mu[i] + G_obs2_mu[i] + G_obs3_mu[i])

    for i in range(G_obs_len):
        for j in range(4):
            model.addCons(G_obs1_mu[i] >= G_obs1_mu_4[i, j])
        model.addCons(G_obs1_mu[i] <= sum(G_obs1_mu_4[i, j] for j in range(4)))
        for j in range(4):
            model.addCons(G_obs2_mu[i] >= G_obs2_mu_4[i, j])
        model.addCons(G_obs2_mu[i] <= sum(G_obs2_mu_4[i, j] for j in range(4)))
        for j in range(4):
            model.addCons(G_obs3_mu[i] >= G_obs3_mu_4[i, j])
        model.addCons(G_obs3_mu[i] <= sum(G_obs3_mu_4[i, j] for j in range(4)))

    for i in range(G_obs_len): 
        model.addCons(x1[G_obs_t[0] + i, 0] - (mu_obs1_x[0] - p_obs) <= M * (1 - G_obs1_mu_4[i, 0]))
        model.addCons( - x1[G_obs_t[0] + i, 0] + (mu_obs1_x[1] + p_obs) <= M * (1 - G_obs1_mu_4[i, 1]))
        model.addCons(x1[G_obs_t[0] + i, 2] - (mu_obs1_y[0] - p_obs) <= M * (1 - G_obs1_mu_4[i, 2]))
        model.addCons( - x1[G_obs_t[0] + i, 2] + (mu_obs1_y[1] + p_obs) <= M * (1 - G_obs1_mu_4[i, 3]))

        model.addCons(x1[G_obs_t[0] + i, 0] - (mu_obs2_x[0] - p_obs) <= M * (1 - G_obs2_mu_4[i, 0]))
        model.addCons( - x1[G_obs_t[0] + i, 0] + (mu_obs2_x[1] + p_obs) <= M * (1 - G_obs2_mu_4[i, 1]))
        model.addCons(x1[G_obs_t[0] + i, 2] - (mu_obs2_y[0] - p_obs) <= M * (1 - G_obs2_mu_4[i, 2]))
        model.addCons( - x1[G_obs_t[0] + i, 2] + (mu_obs2_y[1] + p_obs) <= M * (1 - G_obs2_mu_4[i, 3]))

        model.addCons(x1[G_obs_t[0] + i, 0] - (mu_obs3_x[0] - p_obs) <= M * (1 - G_obs3_mu_4[i, 0]))
        model.addCons( - x1[G_obs_t[0] + i, 0] + (mu_obs3_x[1] + p_obs) <= M * (1 - G_obs3_mu_4[i, 1]))
        model.addCons(x1[G_obs_t[0] + i, 2] - (mu_obs3_y[0] - p_obs) <= M * (1 - G_obs3_mu_4[i, 2]))
        model.addCons( - x1[G_obs_t[0] + i, 2] + (mu_obs3_y[1] + p_obs) <= M * (1 - G_obs3_mu_4[i, 3]))

    


    



    FG = model.addVar(vtype="B")
    G_nest, FG_mu= {}, {}  # mu is mu_x1 \wedge mu_x2
    FG_mu_4 = {}
    for i in range(FG_Flen):
        G_nest[i] = model.addVar(vtype="B")    
    for i in range(FG_len):
        FG_mu[i] = model.addVar(vtype="B")
        for j in range (4):
            FG_mu_4[i, j] = model.addVar(vtype="B")

    for i in range(FG_Flen):
        model.addCons(FG >= G_nest[i])
    model.addCons(FG <= sum(G_nest[i] for i in range(FG_Flen)))

    for i in range(FG_Flen):
        for j in range(FG_Glen):
            model.addCons(G_nest[i] <= FG_mu[i+j])
        model.addCons(G_nest[i] >= 1- FG_Glen + sum(FG_mu[i+j] for j in range(FG_Glen)))

    # encode for mu_x1
    for i in range(FG_len):
        for j in range(4):
            model.addCons(FG_mu[i] <= FG_mu_4[i, j])
        model.addCons(FG_mu[i] >= 1- 4 + sum(FG_mu_4[i, j] for j in range(4)))

    for i in range(FG_len): 
        model.addCons(- x1[FG_t[0] + i, 0] + mu4x[0] <= M * (1 - FG_mu_4[i, 0]))
        model.addCons(x1[FG_t[0] + i, 0] - mu4x[1] <= M * (1 - FG_mu_4[i, 1]))
        model.addCons( - x1[FG_t[0] + i, 2] + mu4y[0] <= M * (1 - FG_mu_4[i, 2]))
        model.addCons(x1[FG_t[0] + i, 2] - mu4y[1] <= M * (1 - FG_mu_4[i, 3]))

    model.addCons(FG == 1)
    model.addCons(G_track == 1)
    model.addCons(G_obs == 1)

    return G_track_mu_4,q_track

