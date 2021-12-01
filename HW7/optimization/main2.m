clear
clc
close all

lb = [0.001,0.001,0.75,0.75,3];
ub = [0.1,0.1,5,5,15];
A = []; b = [];
Aeq = []; beq = [];
nonlcon = @(x) nonlconFcn2(x); % nonlinear constraint
fun = @(x) myfun2(x); % objective function
options.PopulationSize = 20;
options.tol = 1e-10;
options.SelectionPercent = 0.30;
options.Generations = 30;
options.crossover_fraction = 0.8;
options.crossover_ratio = 1.5;
options.Mutationfraction = 0.05;

[x_opt,fval_opt] = GeneticAlgorithmRick(fun,A,b,Aeq,beq,lb,ub,nonlcon,options);
% options = optimoptions('ga','PlotFcn', @gaplotbestf);
% [x_opt,fval_opt,feasible_opt] = ga(fun,5,A,b,Aeq,beq,lb,ub,nonlcon,options);
% options = optimoptions('fmincon','Algorithm','sqp','Display','iter','DiffMinChange',0.001);
% % x0 = [0.055, 0.05, 2, 2, 3];
% x0 = [0.1, 0.1, 2.0, 2.0, 3];
% [x_opt,fval_opt,feasible_opt] = fmincon(fun,x0,A,b,Aeq,beq,lb,ub,nonlcon,options);

%% Optimal solution
[weight,A_skin,A_stiff] = WeightCal(x_opt);
[stress_stiff, stress_skin] = StressCal(x_opt);
final_eigenVal = buckling_analysis(x_opt);
final_eigenVal/(60/x_opt(5))
feasible = isfeasible(x_opt,A,b,Aeq,beq,lb,ub,nonlcon,1e-10,1);

plotPanel(x_opt)



