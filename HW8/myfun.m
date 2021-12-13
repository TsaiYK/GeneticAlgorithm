function f = myfun(x)
for i = 1:3
    xDesign(i) = x(i);
end
xDesign(4) = round(x(4));
xDesign(5) = round(x(5));
[weight,~,~] = WeightCal(xDesign);
f = weight;