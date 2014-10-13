function [  ] = im_reg_test( movingImPath , medImPath )


% load movingIm from filepath
movingIm = imread(movingImPath);
movingIm = double(movingIm);
movingIm = movingIm/255;

% load the median image from filepath
medIm  = imread(medImPath);
medIm  = double(medIm);
medIm  = medIm/255;

% do pre-processing?
% movingIm_preproc = imstack_preproc( movingIm );
movingIm_preproc = movingIm;
medIm_preproc    = medIm;
% medIm_preproc   = imstack_preproc( medIm );

%%%%%%%%%%%%%%%%%%
% setup registration params
main.similarity='MI';   % similarity measure, e.g. SSD, CC, SAD, RC, CD2, MS, MI
main.MIbins=32;         % number of bins for the Mutual Information similarity measure
main.subdivide=3;       % use 3 hierarchical levels
main.okno=10;           % mesh window size, the smaller it is the more complex deformations are possible
main.lambda = 0.10;     % transformation regularization weight, 0 for none (default = 0.01)
main.single=1;          % show mesh transformation at every iteration

main.writeLog   = 0;
main.memLogFile = [];

% Optimization settings
optim.maxsteps = 40;    % maximum number of iterations at each hierarchical level (default = 40)
optim.fundif = 1e-5;    % tolerance (stopping criterion)
optim.gamma = 1;        % initial optimization step size 
optim.anneal=0.8;       % annealing rate on the optimization step    
%%%%%%%%%%%%%%%%%%


% perform the registration
[res, newim]=mirt2D_register(medIm_preproc,movingIm_preproc, main, optim);

% create filename for registered image and transform
movingImPath_reg = [strrep(movingImPath(1:end-4),'ThreshBlur/','ThreshBlurReg/'),'_reg.jpg'];
transformPath = [strrep(movingImPath(1:end-4),'ThreshBlur/','ThreshBlurTransforms/'),'_res.mat'];

% save the jpeg
imwrite(newim,movingImPath_reg,'Quality',100);
% save the transform 
save(transformPath,'res');

end

