clear
clc
close all

%% Call out python code and run FEA
system('cd C:\Users\yktsai0121\Desktop\AERO604_abaqus\HW7_script\ForMatlab');
system('abaqus cae noGUI=buckling_sim.py');

%% Read the data
filename_eigenVal = 'PostData_HW7_buckling_eigenVal.txt';
fileID = fopen(filename_eigenVal,'r');
eigenVal = fscanf(fileID,'%f');

