function plotPanel(x)
t_skin = x(1);
t_stiff = x(2);
h_stiff = x(3);
w_stiff = x(4);
n_stiff = x(5);
w_domain = 60/n_stiff;

figure
surf([0,60;0,60],[0,0;90,90],zeros(2,2),'FaceColor','c'); hold on
for i = 1:n_stiff+1
    p1 = [0+w_domain*(i-1),0,0];
    p2 = [0+w_domain*(i-1),0,h_stiff];
    p3 = [0+w_domain*(i-1),90,0];
    p4 = [0+w_domain*(i-1),90,h_stiff];
    X = [p1(1),p2(1);p3(1),p4(1)];
    Y = [p1(2),p2(2);p3(2),p4(2)];
    Z = [p1(3),p2(3);p3(3),p4(3)];
    surf(X,Y,Z,'FaceColor','b')
end
view([23.5,20.8470])
axis equal  
xlabel('x (in)')
ylabel('y (in)')