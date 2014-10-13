function [  ] = folder_preprocess( movingFolderPath)


fileNames = dir([movingFolderPath,filesep,'*.jpg']);
fprintf('Found %d jpgs to register\n',length(fileNames));
numFiles = length(fileNames);

for i=1:numFiles

    fprintf('registering %d of %d\n',i,numFiles);
    thisMovingImPath = [movingFolderPath,filesep,fileNames(i).name];
    im_preprocess( thisMovingImPath)

end


end
