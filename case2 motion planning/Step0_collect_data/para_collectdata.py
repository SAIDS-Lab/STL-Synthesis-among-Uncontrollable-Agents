total_time = 21
random_p = 0.15

mu1x = [0, 2]
mu1y = [4, 6]
mu2x = [3.5, 6.5]
mu2y = [8, 10]
mu3x = [8.5, 10]
mu3y = [0, 2]

mu1x_shrink = [mu1x[0]+random_p, mu1x[1]-random_p]
mu1y_shrink = [mu1y[0]+random_p, mu1y[1]-random_p]
mu2x_shrink = [mu2x[0]+random_p, mu2x[1]-random_p]
mu2y_shrink = [mu2y[0]+random_p, mu2y[1]-random_p]
mu3x_shrink = [mu3x[0]+random_p, mu3x[1]-random_p]
mu3y_shrink = [mu3y[0]+random_p, mu3y[1]-random_p]


mu_obs1_x = [1.6, 2.6]
mu_obs1_y = [2, 3]
mu_obs2_x = [8.3, 9.3]
mu_obs2_y = [6.5, 7.5]
mu_obs3_x = [5.7, 6.7]
mu_obs3_y = [2.7, 3.7]

mu_obs1_x_shrink = [mu_obs1_x[0]-random_p, mu_obs1_x[1]+random_p]
mu_obs1_y_shrink = [mu_obs1_y[0]-random_p, mu_obs1_y[1]+random_p]
mu_obs2_x_shrink = [mu_obs2_x[0]-random_p, mu_obs2_x[1]+random_p]
mu_obs2_y_shrink = [mu_obs2_y[0]-random_p, mu_obs2_y[1]+random_p]
mu_obs3_x_shrink = [mu_obs3_x[0]-random_p, mu_obs3_x[1]+random_p]
mu_obs3_y_shrink = [mu_obs3_y[0]-random_p, mu_obs3_y[1]+random_p]

umax = 1
vmax = 1.5
M = 10000

G_track_t = [0, total_time-1]
G_track_len = G_track_t[1] - G_track_t[0] + 1

G_obs_t = [0, total_time-1]
G_obs_len = G_obs_t[1] - G_obs_t[0] + 1

G1_t = [4, 6]
G1_len = G1_t[1] - G1_t[0] + 1

G2_t = [9, 13]
G2_len = G2_t[1] - G2_t[0] + 1

FG_t = [16, 18, 0, 2]
FG_Flen = FG_t[1]- FG_t[0] + 1
FG_Glen = FG_t[3]- FG_t[2] + 1
FG_len = FG_t[1] + FG_t[3] - FG_t[0] + 1


D = 1.5
D_shrink = D-random_p*6





