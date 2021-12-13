function eigenvalue_final = buckling_analysis(xDesign)

%% Define the filename for eigenvalue info
filename_eigenVal = 'PostData_HW8_buckling_eigenVal.txt';
% Delete if the previous one exists
if exist(filename_eigenVal, 'file')==2
    delete(filename_eigenVal);
end


% Delete if the previous one exists
if exist('DesignVariables.txt', 'file')==2
    delete('DesignVariables.txt');
end
fileDV = fopen('DesignVariables.txt','w');

% Call out python code and run FEA
fprintf(fileDV,'%.4f\n',xDesign);
system('cd C:\Users\yktsai0121\Desktop\AERO604_abaqus\HW8_script');
disp('Starting FEA analysis in Abaqus...')
tic
system('abaqus cae noGUI=hw8_composite_buckling_analysis.py');
disp('Done!')
toc


% Read the data
fileID = fopen(filename_eigenVal,'r');
eigenVal = fscanf(fileID,'%f');

design_weight = WeightCal(xDesign);

w_domain = 60/xDesign(4);
buckling = min(eigenVal)/w_domain;
if buckling <= 40
    buckles = 1; %yes
    design_weight = design_weight*1000000;
    
else
    buckles = 0; %no
end
min_eigenVal = min(eigenVal);
fclose(fileID);

fclose(fileDV);

%% Outputs

[min_weight, min_index] = min(design_weight);
t_stiff_final = xDesign(min_index,1);
h_stiff_final = xDesign(min_index,2);
w_stiff_final = xDesign(min_index,3);
n_stiff_final = xDesign(min_index,4);
n_lam_final = xDesign(min_index,5);
eigenvalue_final = min_eigenVal(min_index);

fprintf('Lowest weight: %.4f\n',min_weight,' in')
fprintf('T_stiff: %.4f\n',t_stiff_final,' in')
fprintf('H_stiff: %.4f\n',h_stiff_final,' in')
fprintf('W_stiff: %.4f\n',w_stiff_final,' in')
fprintf('N_stiff: %.4f\n',n_stiff_final)
fprintf('N_lam: %.4f\n',n_lam_final,' in')
fprintf('Eigenvalue: %.4f\n',eigenvalue_final)
