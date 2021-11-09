function feasible = isfeasible(x,A,b,Aeq,beq,lb,ub,nonlcon,tol,numPopulation)

% make sure inputs are column vectors
lb=lb(:); ub=ub(:);

% Combine linear inqualities and bounds
if ~isempty(ub) || ~isempty(lb)
    A = [A;eye(size(ub,1));-eye(size(lb,1))];
    b = [b;ub;-lb];
end

% initialize feasibility vector
feasible = true(numPopulation,1);
% Check feasibility of each site
for i=1:numPopulation
    % X is a comun vector of the ith row vector in Xin
    X = x(i,:)';

    % Initialize
    feasibleIneq = true;
    feasibleEq = true;
    feasibleNonlIneq = true;
    feasibleNonlEq = true;

    % Linear Inequality constraints
    if ~isempty(A)
        feasibleIneq = max(A*X-b) <= tol;
    end

    % Linear Equality constraints
    % Including "feasibleIneq" since it is no need to try if linear
    % inequality is violated. The same as the rest of the conditions below
    if (feasibleIneq && ~isempty(Aeq)) 
        feasibleEq   = all(abs(Aeq*X-beq) <= tol);
    end
    
    % Nonlinear constraints
    if (feasibleIneq && feasibleEq && ~isempty(nonlcon) && isa(nonlcon,'function_handle'))
        [c,ceq] = nonlcon(X);
        if ~isempty(c)
            % Inequality constraints
            feasibleNonlIneq = all(all(c <= tol));
        end
        if ~isempty(ceq)
            % Equality constraints
            feasibleNonlEq = all(all(abs(ceq) <= tol));
        end
    end
    
    % feasible is met if all of the constraints are not violated
    feasible(i) = feasibleIneq && feasibleEq && feasibleNonlIneq && feasibleNonlEq;
end