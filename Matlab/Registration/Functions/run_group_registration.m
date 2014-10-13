function [ ] = run_group_registration( imstackCell )


  logfilepath = '/log/';
  theTime = datestr(now,'HH:MM:SS');
  theDate = datestr(now,'dd-mmm-yyyy');


  % add var name and datetime to the logfile name to help identify later
  imstackname = inputname(1);
  if isempty(imstackname)
    imstackname = 'imstack';
  end
  metadata.logfile1 = [logfilepath,'registration_log','-',imstackname,'-',theTime,'-',theDate,'.log'];
  metadata.log   = 1;

  t0 = clock;
  fprintf('Running local registration optimization\n');
  for i=1:length(imstackCell)
    imstack = imstackCell{i};
    results{i} = run_imstack_registration(imstack,i);
  end
  jobTime = etime(clock,t0);
  fprintf('Time taken: %.2f secs\n',jobTime);

  % save results to disk
  filename_transform = ['transforms-',imstackname,'-',theTime,'-',theDate,'.mat'];
  filepath_transform = ['Example_Results/GroupRegistration/transform_results/'];
  fprintf('Saving results to disk..\n');
  tic;
  %res = results{1};
  % use functional ver of save when filename is stored in a var
  save([filepath_transform,filename_transform], 'results');
  toc

end
