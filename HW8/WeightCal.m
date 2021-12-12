function [weight,A_skin,A_stiff] = WeightCal(x)
% x = [t_skin,t_stiff,h_stiff,w_stiff,n_stiff]
t_stiff = x(1);
h_stiff = x(2);
w_stiff = x(3);
n_stiff = x(4);
n_lam = x(5);

% Parameters
L = 90;
w_skin = 60; % width of plate, unit: in
rho_alum = 0.0975; %density of material, lb/in^3
rho_composite = 0.05708112; %lb/in^3

% Cross-sectional Area calculation
A_skin = n_lam*0.005*w_skin;
A_stiff = n_stiff*(w_stiff*h_stiff - (w_stiff-t_stiff)*(h_stiff-t_stiff));

% weight
weight = (A_skin*L*rho_composite)+(A_stiff*L*rho_alum);
