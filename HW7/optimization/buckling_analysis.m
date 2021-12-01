function final_eigenVal = buckling_analysis(xDesign)

%% Define the filename for eigenvalue info
filename_eigenVal = 'PostData_HW7_buckling_eigenVal.txt';
% Delete if the previous one exists
if exist(filename_eigenVal, 'file')==2
    delete(filename_eigenVal);
end

%% Define design variables
% Delete if the previous one exists
if exist('DesignVariables.txt', 'file')==2
    delete('DesignVariables.txt');
end
fileDV = fopen('DesignVariables.txt','w');
% xDesign = [0.001, 0.001, 0.75, 0.75, 15];
fprintf(fileDV,'%.4f\n',xDesign);
fclose(fileDV);

%% Call out python code and run FEA
system('cd C:\Users\yktsai0121\Desktop\AERO604_abaqus\HW7_script\ForMatlab');
disp('Starting FEA analysis in Abaqus...')
tic
system('abaqus cae noGUI=buckling_sim_new2.py');
disp('Done!')
toc

%% Read the data
fileID = fopen(filename_eigenVal,'r');
eigenVal = fscanf(fileID,'%f');
final_eigenVal = min(eigenVal);
fclose(fileID);

fprintf('Design variables:\n')
fprintf('t_skin: %.4f in\n',xDesign(1))
fprintf('t_stiff: %.4f in\n',xDesign(2))
fprintf('h_stiff: %.4f in\n',xDesign(3))
fprintf('w_stiff: %.4f in\n',xDesign(4))
fprintf('n_stiff: %d\n',xDesign(5))
fprintf('Eigenvalue for buckling: %.4f\n',final_eigenVal)
fprintf('critical buckling load: %.4f\n',final_eigenVal/(60/xDesign(5)))


