function [stress_skin,stress_stiff] = StressCal(x,L)
% x = [t_skin,t_stiff,h_stiff,w_stiff,n_stiff]
[~,A_skin,A_stiff] = WeightCal(x,L);

% Forces
w_skin = 60; % width of plate, unit: in
F = 40*w_skin;
F_skin = F*A_skin/(A_skin+A_stiff);
F_stiff = F*A_stiff/(A_skin+A_stiff);

% Stresses
stress_skin = F_skin/A_skin;
stress_stiff = F_stiff/A_stiff;