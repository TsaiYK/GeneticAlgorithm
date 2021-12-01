function [xBest,fvalBest] = GeneticAlgorithmRick(fun,A,b,Aeq,beq,lb,ub,nonlcon,options)
generation = 1;
while generation<options.Generations
    if generation ~= 1
        options.parentPops = mutantKids{generation-1};
        options.parentFval = fvalKids{generation-1};
        options.paraentFeasible = feasibleKids{generation-1};
    end
    [mutantKids{generation}, fvalKids{generation}, feasibleKids{generation},...
        x_sort{generation}, fval_sort{generation}, feasible_sort{generation}] = ...
        GeneticAlgorithmRickFunc(fun,A,b,Aeq,beq,lb,ub,nonlcon,options,generation);

%     if mod(generation,10)==1
%         clf
%         figure(1)
%         plot(x_sort{generation}(:,1),x_sort{generation}(:,2),'k.'); hold on
%         plot(mutantKids{generation}(:,1),mutantKids{generation}(:,2),'b*');
%         axis([lb(1),ub(1),lb(2),ub(2)]);
%         pause(1);
%     end
    if isempty(fvalKids{generation}(find(feasibleKids{generation})==1))
        mean_fval = NaN;
        min_fval = NaN;
    else
        fvalKids{generation}(find(feasibleKids{generation})==1)
        mean_fval = mean(fvalKids{generation}(find(feasibleKids{generation})==1));
        min_fval = min(fvalKids{generation}(find(feasibleKids{generation})==1));
    end
    figure(1)
%     plot(generation,mean_fval,'k.','MarkerSize',10); hold on
    plot(generation,min_fval,'b*'); hold on
    xlabel('Generations'); ylabel('Objective Function')
    legend('Best');
    xlim([0,options.Generations]);
        
    generation = generation+1;

end

fvalFinal = fvalKids{end};
xFinal = mutantKids{end};
feasibleFinal = feasibleKids{end};

[fvalBest,index_best] = min(fvalFinal(feasibleFinal));
xFinalFeasible = xFinal(feasibleFinal,:);
xBest = xFinalFeasible(index_best,:);


function [mutantKids, fvalKids, feasibleKids, x_sort, fval_sort, feasible_sort] = ...
    GeneticAlgorithmRickFunc(fun,A,b,Aeq,beq,lb,ub,nonlcon,options,generation)
% clear
% clc
% % lb = [-1,-1,-1,-1,-1]; ub = [1,1,1,1,1];
% lb = [-1,-1]; ub = [1,1];
% A = []; b = [];
% Aeq = []; beq = [];
% nonlcon = [];
% fun = @(x) myfun2(x);
% options.PopulationSize = 100;
% options.tol = 1e-3;
% options.SelectionPercent = 0.10;
% options.Generations = 10;
% generation = 1;

% genetic algorithm written by Ying-Kuan (Rick) Tsai
numPopulation = options.PopulationSize;
tol = options.tol;

%% Initialize population
if generation == 1
    n = length(lb);
    xm = (lb+ub)/2;
    delta_x = ub-lb;
    x = rand(numPopulation,n);
    x = x.*repmat(delta_x,numPopulation,1)+...
        repmat(lb,numPopulation,1);
else
    x = options.parentPops;
end

%% Evaluate obj and constraints functions
for i = 1:numPopulation
    fval(i) = fun(x(i,:));
end

%% Mark the infeasible
feasible = isfeasible(x,A,b,Aeq,beq,lb,ub,nonlcon,tol,numPopulation);

%% Selection
topPercent = options.SelectionPercent;
selection_num = round(numPopulation*topPercent);
xFeasible = x(feasible,:);
fvalFeasible = fval(feasible);
feasibleFeasible = feasible(feasible);

[fval_sort,sort_index] = sort(fvalFeasible);
x_sort = xFeasible(sort_index,:);
feasible_sort = feasibleFeasible(sort_index);

num_x_selected = 0;
x_selected = []; fval_selected = [];
k = 1;
while num_x_selected < selection_num
    if k<=size(x_sort,1)
        x_selected = [x_selected;x_sort(k,:)];
        fval_selected = [fval_selected;fval_sort(k)];
    else
        break
    end
    k = k+1;
    num_x_selected = size(x_selected,1);
end

% x_selected = x_sort(1:selection_num,:);
% fval_selected = fval_sort(1:selection_num);

%% Crossover
poolSize=size(x_selected,1);
if mod(poolSize,2)
    parents=[x_selected;x_selected(1,:)];
else
    parents = x_selected;
end
xoverKids = zeros(numPopulation,length(lb));
crossover_fraction = options.crossover_fraction;
crossover_ratio = options.crossover_ratio;
k = 1;
for ind = 1:2:size(parents,1)    % Popsize should be even number
    for j = 1:round(1/topPercent)
    % Create crossover children
        [child1, child2] = crsintermediate( parents(ind,:),...
            parents(ind+1,:), crossover_fraction, crossover_ratio);

        % Save feasible crossover children
        xoverKids(k,:)     = child1;
        xoverKids(k+1,:)   = child2;
        k = k+2;
    end
end

%% Mutation
% Determine the mutation method
mutationopt{1} = 0.1; % scale
mutationopt{2} = 0.5; % shrink

% Mutation fraction
Mutationfraction = options.Mutationfraction;

% All of the individual would be modified, but only 'mutationFraction' of design
% variables for an individual would be changed.
mutantKids = zeros(size(xoverKids));
feasibleKids = false(size(xoverKids,1),1);
fvalKids = zeros(1,selection_num);
for ind = 1:size(xoverKids,1)
    % Mutate child
    mutantKid = mutationgaussian( xoverKids(ind,:), lb, ub, options,...
        generation, Mutationfraction, mutationopt);
    
    % Save kid to pool
    mutantKids(ind,:) = mutantKid;
    % Check feasiblity
    feasibleKids(ind) = isfeasible(mutantKid,A,b,Aeq,beq,lb,ub,nonlcon,tol,1);
    fvalKids(ind) = fun(mutantKids(ind,:));
end

end

end
