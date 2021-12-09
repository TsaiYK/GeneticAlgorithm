function f = myfun3(x)
for i = 1:3
    xDesign(i) = x(i);
end
xDesign(4) = 0.75;
xDesign(5) = round(x(5));
[weight,~,~] = WeightCal(xDesign);
f = weight;