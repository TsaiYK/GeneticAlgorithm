%% DVs
t_skin = 0.055;
t_stiff = 0.05;
h_stiff = 5;
w_stiff = 4;
n_stiff = 3;

x = [t_skin, t_stiff, h_stiff, w_stiff, n_stiff];

%% Outputs
[weight,A_skin,A_stiff] = WeightCal(x)
[stress_stiff, stress_skin] = StressCal(x)
[sigma_cr_stiff, sigma_cr_skin] = BucklingCalcs(x)