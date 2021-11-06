clear
clc
close all
% lb = [-1,-1,-1,-1,-1]; ub = [1,1,1,1,1];
lb = [-1,-1]; ub = [1,1];
% A = []; b = [];
A = [-5/3, -1; -0.3, -1]; b = [-0.5;-0.3];
Aeq = []; beq = [];
% nonlcon = [];
nonlcon = @(x) nonlconFcn(x);
fun = @(x) myfun(x);
% fun = @(x) peaks(x(1),x(2));
options.PopulationSize = 100;
options.tol = 1e-3;
options.SelectionPercent = 0.30;
options.Generations = 100;
options.crossover_fraction = 0.8;
options.crossover_ratio = 1.5;
options.Mutationfraction = 0.05;
generation = 1;

[x_opt,fval_opt] = GeneticAlgorithmRick(fun,A,b,Aeq,beq,lb,ub,nonlcon,options);

% options = [];
% [x_opt,fval_opt,feasible_opt] = ga(fun,2,A,b,Aeq,beq,lb,ub,nonlcon,options);

figure(gcf);
axis([lb(1),ub(1),lb(2),ub(2)]);

%%
figure;
plot(x_opt(1),x_opt(2),'k*'); hold on
axis([lb(1),ub(1),lb(2),ub(2)]);

x1 = linspace(lb(1),ub(1),30);
x2 = linspace(lb(2),ub(2),30);
[X1,X2] = meshgrid(x1,x2);
X1 = X1'; X2 = X2';

for i = 1:length(x1)
    for j = 1:length(x2)
        x = [x1(i),x2(j)];
        f(i,j) = fun(x);
    end
end

y_constr(1,:) = -5/3*x1+0.5;
y_constr(2,:) = -0.3*(x1-1);
t = 0:0.01:2*pi;

% figure
contour(X1,X2,f); hold on
axis([lb(1),ub(1),lb(2),ub(2)]);
plot(x1,y_constr(1,:),'b-')
plot(0.5*cos(t),0.5*sin(t),'b-')
plot(x1,y_constr(2,:),'b-')


