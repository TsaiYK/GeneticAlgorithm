function [weight,A_skin,A_stiff] = WeightCal(x,L)
% x = [t_skin,t_stiff,h_stiff,w_stiff,n_stiff]
t_skin = x(1);
t_stiff = x(2);
h_stiff = x(3);
w_stiff = x(4);
n_stiff = x(5);

% Parameters
w_skin = 60; % width of plate, unit: in

% Area calculation
A_skin = t_skin*w_skin*n_stiff;
A_stiff = w_stiff*h_stiff - (w_stiff-t_stiff)*(h_stiff-t_stiff);

% weight
weight = (A_skin+A_stiff)*L;

