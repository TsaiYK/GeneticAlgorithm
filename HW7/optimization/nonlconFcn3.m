function [c,ceq] = nonlconFcn3(x)
for i = 1:3
    xDesign(i) = x(i);
end
xDesign(4) = 0.75;
xDesign(5) = round(x(4));
eigenVal = buckling_analysis(xDesign);
c(1) = -(eigenVal/(60/xDesign(5))-40);
ceq = [];
