function [res] = run_imstack_registration(imstack , stackInd)



% default
main.group=2;           % Groupwise mode option: 0 - all frames are registered  to the first frame
                        %                        1 - every next frame is registered to the previous sequentially
                        %                        2 - every next frame is registred to the average of the previously registered frames
                        %                            (accumulated memory)

main.okno=33;           % mesh window size (default=33)

%['ssd','sad','rc','cc','cd2','ms','mi']
main.similarity='mi';   % similarity measure
%main.MIbins=32; % number of mutual information bins (default=64)

main.subdivide = 2;     % number of hierarchical levels
main.lambda = 0.03;     % regularization weight, 0 for none (default = 0.03)
main.alpha  = 0.03;     % similarity measure parameter
main.single=0;          % don't show the mesh at each iteration

% log memory usage
theTime = datestr(now,'HH:MM:SS');
theDate = datestr(now,'dd-mmm-yyyy');
filename_mem_log = ['mem-',theTime,'-',theDate,'.log'];
filepath_mem_log = ['/transform_results/'];
main.memLogFile = [filepath_mem_log,filename_mem_log];

%mem = memUsage('caller');
%memLogger(mem , [filepath_mem_log,filename_mem_log]);

% Optimization parameters
optim.maxsteps = 500;      % maximum number of iterations (for a given frame being registered to the mean image default=500)
optim.fundif = 1e-5;     % tolerance (for a given frame)
optim.gamma = 1;         % initial optimization step size
optim.anneal=0.8;        % annealing rate

optim.imfundif=1e-6;    % Tolerance of the mean image (change of the mean image)
optim.maxcycle=40;       % default=40



[ res ] = find_transform( imstack , main , optim );



filepath = 'Example_results/GroupRegistration/transform_results/';
filename = 'res_imstack';
the_date = datestr(now,'dd_mm_yy_HH:MM:SS');
filename = [filepath,filename,'_',num2str(stackInd),'_',the_date];
save(filename,'res');


end
