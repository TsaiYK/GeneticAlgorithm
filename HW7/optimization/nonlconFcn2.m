function [c,ceq] = nonlconFcn2(x)
x(5) = round(x(5));
% % [weight,A_skin,A_stiff] = WeightCal(x);
% [stress_stiff, stress_skin] = StressCal(x);
% [sigma_cr_stiff, sigma_cr_skin] = BucklingCalcs(x);
% % buckleOrNot = [stress_stiff>sigma_cr_stiff, ...
% %     stress_skin>sigma_cr_skin];
% % c = buckleOrNot;
% c(1) = stress_stiff-sigma_cr_stiff;
% c(2) = stress_skin-sigma_cr_skin;
% c(3) = stress_stiff-sigma_y;
% c(4) = stress_skin-sigma_y;
eigenVal = buckling_analysis(x);
c(1) = -(eigenVal/(60/x(5))-40);
ceq = [];