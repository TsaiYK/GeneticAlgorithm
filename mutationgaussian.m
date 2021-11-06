function mutantKid = mutationgaussian(kid,lb,ub,options,generation,fraction,mutationopt)
%MUTATIONGAUSSIAN Gaussian mutation operator (Inspired by MATLAB gaussianmuatation)

% 2. Calc the "scale" and "shrink" parameter.
if min(size(kid))~=1
    error('Kid must be vector')
end
nvars = length(kid);
scale =  mutationopt{1};
shrink =  mutationopt{2};
scale = scale - shrink * scale * generation / options.Generations;

scale = scale * (ub - lb);
mutantKid=kid;
for i = 1:nvars
    if(rand() < fraction)
        mutantKid(i) = kid(i) + scale(i) * randn();
    end
end
end