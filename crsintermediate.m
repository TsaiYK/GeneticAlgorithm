function [child1, child2] = crsintermediate(parent1, parent2, fraction, ratio)
% CRSINTERMEDIATE crossover operator (Inspired by Matlab's crossover operator)
%
% Description: (For real coding) Intermediate crossover. 
%       child = parent1 + rand * Ratio * ( parent2 - parent1)
%
% Parameters: 
%   fraction : crossover fraction of variables of an individual
%   options = ratio
%
% This function could be improved quite a bit for better results

nvars = length(parent1);
crsFlag = rand(1, nvars) < fraction;

randNum = rand(1,nvars);     % uniformly distribution

child1 = parent1 + crsFlag .* randNum .* ratio .* (parent2 - parent1);
child2 = parent2 - crsFlag .* randNum .* ratio .* (parent2 - parent1);