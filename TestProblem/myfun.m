function f = myfun(x)
f = 0;
for i = 1:length(x)
    f = f+x(i)^2;
end