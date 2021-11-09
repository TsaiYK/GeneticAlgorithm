function [c,ceq] = nonlconFcn(x)
f = 0;
for i = 1:length(x)
    f = f+x(i)^2;
end
c = -(f-0.5^length(x));
ceq = [];