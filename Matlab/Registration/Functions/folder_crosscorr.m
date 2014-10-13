function [  ] = folder_crosscorr( medpath , regpath )


fileNames = dir([regpath,filesep,'*.jpg']);
fprintf('Found %d jpgs to register\n',length(fileNames));
logfilepath = [regpath,'CrosscorrelationsLog.txt'];
numFiles = length(fileNames);

% open file
fid = fopen(logfilepath,'a+');
if fid==-1
    error('Error opening file');
end

for i=1:numFiles

    fprintf('registering %d of %d, %s\n',i,numFiles,fileNames(i).name);
    thisregpath = [regpath,filesep,fileNames(i).name];
    im_crosscorr( medpath , thisregpath , fid );

end

% close file
fclose(fid);

end
