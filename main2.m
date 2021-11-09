clear
clc
close all

lb = [0.01,0.01,2,2,3];
ub = [0.1,0.1,10,10,20];
A = []; b = [];
Aeq = []; beq = [];
nonlcon = @(x) nonlconFcn2(x); % nonlinear constraint
fun = @(x) myfun2(x); % objective function
options.PopulationSize = 1000;
options.tol = 1e-10;
options.SelectionPercent = 0.30;
options.Generations = 100;
options.crossover_fraction = 0.8;
options.crossover_ratio = 1.5;
options.Mutationfraction = 0.05;

[x_opt,fval_opt] = GeneticAlgorithmRick(fun,A,b,Aeq,beq,lb,ub,nonlcon,options);

% options = [];
% [x_opt,fval_opt,feasible_opt] = ga(fun,2,A,b,Aeq,beq,lb,ub,nonlcon,options);

%% Optimal solution
[weight,A_skin,A_stiff] = WeightCal(x_opt);
[stress_stiff, stress_skin] = StressCal(x_opt);
[sigma_cr_stiff, sigma_cr_skin] = BucklingCalcs(x_opt);
buckleOrNot = [stress_stiff>sigma_cr_stiff, ...
    stress_skin>sigma_cr_skin];
feasible = isfeasible(x_opt,A,b,Aeq,beq,lb,ub,nonlcon,options.tol,1);

