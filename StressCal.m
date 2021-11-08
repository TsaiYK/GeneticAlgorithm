function [stress_stiff,stress_skin] = StressCal(x)
% x = [t_skin,t_stiff,h_stiff,w_stiff,n_stiff]
[~,A_skin,A_stiff] = WeightCal(x);


% Forces
w_skin = 60;
w_domain = w_skin/x(5);% width of plate, unit: in
F = 40*w_domain;
F_skin = F*A_skin/(A_skin+A_stiff);
F_stiff = F*A_stiff/x(5)/(A_skin+A_stiff);

% Stresses
stress_skin = F_skin/A_skin;
stress_stiff = F_stiff/A_stiff;