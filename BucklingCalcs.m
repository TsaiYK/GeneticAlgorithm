%% Calculating Moment of Inertia for stringers 
%Constants
E = 10.4E6; %psi
sigma_y = 40E3; %psi
v = 0.3; 
rho = 0.0975; %lb/in^3
L = 90; %in
Ncr = 40; %lbf/in
c = 4; %from definition for clamped-clamped beam
kc = 7.2; 

%Variables
t_skin = 0.055;
t_stiff = 0.05;
n_stiff = 3;
h_stiff = 5;
w_stiff = 4;
w_domain = 60/n_stiff; 

%Calculations
L_rho_EJ = pi*sqrt((2*c*E)/sigma_y) %Value to compare to in order to determine Euler or Johnson
%Moment of Inertia calcs
Ixx1 = (1/12)*(w_stiff-t_stiff)*t_stiff^3 
Iyy1 = (1/12)*t_stiff*(w_stiff-t_stiff)^3 
Ixx2 = (1/12)*t_stiff*h_stiff^3
Iyy2 = (1/12)*h_stiff*t_stiff^3
A1 = (w_stiff-t_stiff)*t_stiff;
A2 = t_stiff*h_stiff;
Cx = ((w_stiff-t_stiff)/2*A1+(w_stiff-(t_stiff/2))*A2)/(A1+A2);
Cy = ((t_stiff/2)*A1+(h_stiff/2)*A2)/(A1+A2);
C1x = (w_stiff-t_stiff)/2;
C1y = t_stiff/2;
C2x = w_stiff-(t_stiff/2);
C2y = h_stiff/2;
Ixx_adj = (Ixx1+A1*(Cy-C1y)^2)+(Ixx2+A2*(Cy-C2y)^2)
Iyy_adj = (Iyy1+A1*(Cx-C1x)^2)+(Iyy2+A2*(Cx-C2x)^2)

%Additional Calcs
A_stringer = (t_stiff*h_stiff)+(t_stiff*(w_stiff-t_stiff));
rho_stringer_xx = sqrt(Ixx_adj/A_stringer);
rho_stringer_yy = sqrt(Iyy_adj/A_stringer);
rho = min([rho_stringer_xx, rho_stringer_yy]);

%Loop for 
if L/rho > L_rho_EJ 
    sigma_cr = c*(pi^2*E)/(L/rho)^2
else 
    sigma_cr = sigma_y*(1-((sigma_y*(L/rho)^2))/(4*c*pi^2*E))
    
end
