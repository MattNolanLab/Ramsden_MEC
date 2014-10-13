function [  ] = folder_reg( movingFolderPath , medImPath,movingFolder )


fileNames = dir(fullfile(movingFolderPath,movingFolder,filesep,'*.jpg'));
fprintf('Found %d jpgs to register\n',length(fileNames));
numFiles = length(fileNames);

for i=1:numFiles

    fprintf('registering %d of %d\n',i,numFiles);
    thisMovingImPath = fullfile(movingFolderPath,movingFolder,filesep,fileNames(i).name); %(3:end)
    diary([movingFolderPath,'Segmented/Log',filesep,fileNames(i).name,'log.txt'])
    fprintf(thisMovingImPath );
    im_reg( thisMovingImPath , medImPath );
    diary off

end


end
