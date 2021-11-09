function f = myfun2(x)
x(:,5) = round(x(:,5));
[weight,~,~] = WeightCal(x);
f = weight;