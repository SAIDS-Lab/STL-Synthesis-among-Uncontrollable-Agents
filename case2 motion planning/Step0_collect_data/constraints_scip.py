from para_collectdata import *
from pyscipopt import *

def addConstr(model, x2, u2, k, optimal_state_r2, optimal_control_r2):

    # system model constraints
    # known state
    for i in range(0, k+1):
        for j in range(4):
            model.addCons(x2[i, j] == optimal_state_r2[i][j])  
    for i in range(0, k):
        for j in range(2):
            model.addCons(u2[i, j] == optimal_control_r2[i][j])  
    
    # model [1,T]
    for i in range(k, total_time-1):
        model.addCons(x2[i+1, 0] == x2[i, 0] + x2[i, 1] + 0.5*u2[i, 0])
        model.addCons(x2[i+1, 1] == x2[i, 1] + u2[i, 0])
        model.addCons(x2[i+1, 2] == x2[i, 2] + x2[i, 3] + 0.5*u2[i, 1])
        model.addCons(x2[i+1, 3] == x2[i, 3] + u2[i, 1])
        

    # physical constraints
    for i in range(k+1, total_time):
        model.addCons(x2[i, 0] >= 0)
        model.addCons(x2[i, 0] <= 10)
        model.addCons(x2[i, 1] >= -vmax)
        model.addCons(x2[i, 1] <= vmax)
        model.addCons(x2[i, 2] >= 0)
        model.addCons(x2[i, 2] <= 10)
        model.addCons(x2[i, 3] >= -vmax)
        model.addCons(x2[i, 3] <= vmax)



    G1 = model.addVar(vtype="B")
    G1_mu, G1_mu_4 = {}, {}
    for i in range(G1_len):
        G1_mu[i] = model.addVar(vtype="B")
        for j in range(4):
            G1_mu_4[i, j] = model.addVar(vtype="B")
            
    for i in range(G1_len):
        model.addCons(G1 <= G1_mu[i])
    model.addCons(G1 >= 1- G1_len + sum(G1_mu[i] for i in range(G1_len)))

    # encode for mu_x1
    for i in range(G1_len):
        for j in range(4):
            model.addCons(G1_mu[i] <= G1_mu_4[i, j])
        model.addCons(G1_mu[i] >= 1- 4 + sum(G1_mu_4[i, j] for j in range(4)))

    for i in range(G1_len): 
        if k >= G1_t[0] + i:
            model.addCons(- x2[G1_t[0] + i, 0] + mu1x[0] <= M * (1 - G1_mu_4[i, 0]))
            model.addCons(x2[G1_t[0] + i, 0] - mu1x[1] <= M * (1 - G1_mu_4[i, 1]))
            model.addCons( - x2[G1_t[0] + i, 2] + mu1y[0] <= M * (1 - G1_mu_4[i, 2]))
            model.addCons(x2[G1_t[0] + i, 2] - mu1y[1] <= M * (1 - G1_mu_4[i, 3]))
        else:
            model.addCons(- x2[G1_t[0] + i, 0] + mu1x_shrink[0] <= M * (1 - G1_mu_4[i, 0]))
            model.addCons(x2[G1_t[0] + i, 0] - mu1x_shrink[1] <= M * (1 - G1_mu_4[i, 1]))
            model.addCons( - x2[G1_t[0] + i, 2] + mu1y_shrink[0] <= M * (1 - G1_mu_4[i, 2]))
            model.addCons(x2[G1_t[0] + i, 2] - mu1y_shrink[1] <= M * (1 - G1_mu_4[i, 3]))

    G2 = model.addVar(vtype="B")
    G2_mu, G2_mu_4 = {}, {}
    for i in range(G2_len):
        G2_mu[i] = model.addVar(vtype="B")
        for j in range(4):
            G2_mu_4[i, j] = model.addVar(vtype="B")
            
    for i in range(G2_len):
        model.addCons(G2 <= G2_mu[i])
    model.addCons(G2 >= 1- G2_len + sum(G2_mu[i] for i in range(G2_len)))

    for i in range(G2_len):
        for j in range(4):
            model.addCons(G2_mu[i] <= G2_mu_4[i, j])
        model.addCons(G2_mu[i] >= 1- 4 + sum(G2_mu_4[i, j] for j in range(4)))

    for i in range(G2_len): 
        if k >= G2_t[0] + i:
            model.addCons(- x2[G2_t[0] + i, 0] + mu2x[0] <= M * (1 - G2_mu_4[i, 0]))
            model.addCons(x2[G2_t[0] + i, 0] - mu2x[1] <= M * (1 - G2_mu_4[i, 1]))
            model.addCons( - x2[G2_t[0] + i, 2] + mu2y[0] <= M * (1 - G2_mu_4[i, 2]))
            model.addCons(x2[G2_t[0] + i, 2] - mu2y[1] <= M * (1 - G2_mu_4[i, 3]))
        else:
            model.addCons(- x2[G2_t[0] + i, 0] + mu2x_shrink[0] <= M * (1 - G2_mu_4[i, 0]))
            model.addCons(x2[G2_t[0] + i, 0] - mu2x_shrink[1] <= M * (1 - G2_mu_4[i, 1]))
            model.addCons( - x2[G2_t[0] + i, 2] + mu2y_shrink[0] <= M * (1 - G2_mu_4[i, 2]))
            model.addCons(x2[G2_t[0] + i, 2] - mu2y_shrink[1] <= M * (1 - G2_mu_4[i, 3]))


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

    for i in range(FG_len):
        for j in range(4):
            model.addCons(FG_mu[i] <= FG_mu_4[i, j])
        model.addCons(FG_mu[i] >= 1- 4 + sum(FG_mu_4[i, j] for j in range(4)))

    for i in range(FG_len): 
        if k >= FG_t[0] + i:
            model.addCons(- x2[FG_t[0] + i, 0] + mu3x[0] <= M * (1 - FG_mu_4[i, 0]))
            model.addCons(x2[FG_t[0] + i, 0] - mu3x[1] <= M * (1 - FG_mu_4[i, 1]))
            model.addCons( - x2[FG_t[0] + i, 2] + mu3y[0] <= M * (1 - FG_mu_4[i, 2]))
            model.addCons(x2[FG_t[0] + i, 2] - mu3y[1] <= M * (1 - FG_mu_4[i, 3]))
        else:
            model.addCons(- x2[FG_t[0] + i, 0] + mu3x_shrink[0] <= M * (1 - FG_mu_4[i, 0]))
            model.addCons(x2[FG_t[0] + i, 0] - mu3x_shrink[1] <= M * (1 - FG_mu_4[i, 1]))
            model.addCons( - x2[FG_t[0] + i, 2] + mu3y_shrink[0] <= M * (1 - FG_mu_4[i, 2]))
            model.addCons(x2[FG_t[0] + i, 2] - mu3y_shrink[1] <= M * (1 - FG_mu_4[i, 3]))

    G_obs_r2 = model.addVar(vtype="B")
    G_obs_mu_r2 = {}
    G_obs1_mu_r2, G_obs2_mu_r2, G_obs3_mu_r2 = {}, {}, {}
    G_obs1_mu_4_r2, G_obs2_mu_4_r2, G_obs3_mu_4_r2 = {}, {}, {}
    for i in range(G_obs_len):
        G_obs_mu_r2[i] = model.addVar(vtype="B")
        G_obs1_mu_r2[i] = model.addVar(vtype="B")
        G_obs2_mu_r2[i] = model.addVar(vtype="B")
        G_obs3_mu_r2[i] = model.addVar(vtype="B")
        for j in range(4):
            G_obs1_mu_4_r2[i, j] = model.addVar(vtype="B")
            G_obs2_mu_4_r2[i, j] = model.addVar(vtype="B")
            G_obs3_mu_4_r2[i, j] = model.addVar(vtype="B")
            
    for i in range(G_obs_len):
        model.addCons(G_obs_r2 <= G_obs_mu_r2[i])
    model.addCons(G_obs_r2 >= 1- G_obs_len + sum(G_obs_mu_r2[i] for i in range(G_obs_len)))


    for i in range(G_obs_len):
        model.addCons(G_obs_mu_r2[i] <= G_obs1_mu_r2[i])
        model.addCons(G_obs_mu_r2[i] <= G_obs2_mu_r2[i])
        model.addCons(G_obs_mu_r2[i] <= G_obs3_mu_r2[i])
        model.addCons(G_obs_mu_r2[i] >= 1 - 3 + G_obs1_mu_r2[i] + G_obs2_mu_r2[i] + G_obs3_mu_r2[i])

    for i in range(G_obs_len):
        for j in range(4):
            model.addCons(G_obs1_mu_r2[i] >= G_obs1_mu_4_r2[i, j])
        model.addCons(G_obs1_mu_r2[i] <= sum(G_obs1_mu_4_r2[i, j] for j in range(4)))
        for j in range(4):
            model.addCons(G_obs2_mu_r2[i] >= G_obs2_mu_4_r2[i, j])
        model.addCons(G_obs2_mu_r2[i] <= sum(G_obs2_mu_4_r2[i, j] for j in range(4)))
        for j in range(4):
            model.addCons(G_obs3_mu_r2[i] >= G_obs3_mu_4_r2[i, j])
        model.addCons(G_obs3_mu_r2[i] <= sum(G_obs3_mu_4_r2[i, j] for j in range(4)))

    for i in range(G_obs_len): 
        model.addCons(x2[G_obs_t[0] + i, 0] - mu_obs1_x_shrink[0] <= M * (1 - G_obs1_mu_4_r2[i, 0]))
        model.addCons( - x2[G_obs_t[0] + i, 0] + mu_obs1_x_shrink[1] <= M * (1 - G_obs1_mu_4_r2[i, 1]))
        model.addCons(x2[G_obs_t[0] + i, 2] - mu_obs1_y_shrink[0] <= M * (1 - G_obs1_mu_4_r2[i, 2]))
        model.addCons( - x2[G_obs_t[0] + i, 2] + mu_obs1_y_shrink[1] <= M * (1 - G_obs1_mu_4_r2[i, 3]))

        model.addCons(x2[G_obs_t[0] + i, 0] - mu_obs2_x_shrink[0] <= M * (1 - G_obs2_mu_4_r2[i, 0]))
        model.addCons( - x2[G_obs_t[0] + i, 0] + mu_obs2_x_shrink[1] <= M * (1 - G_obs2_mu_4_r2[i, 1]))
        model.addCons(x2[G_obs_t[0] + i, 2] - mu_obs2_y_shrink[0] <= M * (1 - G_obs2_mu_4_r2[i, 2]))
        model.addCons( - x2[G_obs_t[0] + i, 2] + mu_obs2_y_shrink[1] <= M * (1 - G_obs2_mu_4_r2[i, 3]))

        model.addCons(x2[G_obs_t[0] + i, 0] - mu_obs3_x_shrink[0] <= M * (1 - G_obs3_mu_4_r2[i, 0]))
        model.addCons( - x2[G_obs_t[0] + i, 0] + mu_obs3_x_shrink[1] <= M * (1 - G_obs3_mu_4_r2[i, 1]))
        model.addCons(x2[G_obs_t[0] + i, 2] - mu_obs3_y_shrink[0] <= M * (1 - G_obs3_mu_4_r2[i, 2]))
        model.addCons( - x2[G_obs_t[0] + i, 2] + mu_obs3_y_shrink[1] <= M * (1 - G_obs3_mu_4_r2[i, 3]))


    z_phi = model.addVar(vtype="B")

    
    model.addCons(z_phi >= G1)
    model.addCons(z_phi >= G2)
    model.addCons(z_phi >= FG)
    model.addCons(z_phi >= G_obs_r2)
    model.addCons(z_phi <= 1-4+G1+G2+FG+G_obs_r2)

    model.addCons(z_phi == 1)
   
