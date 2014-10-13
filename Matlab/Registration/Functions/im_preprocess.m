function [  ] = im_preprocess( movingImPath)

% load movingIm from filepath
try
    movingIm = imread(movingImPath);
    movingIm = double(movingIm);
    movingIm = movingIm/255;

    % Run preprocessing
    movingIm_preproc = imstack_preproc( movingIm );
    movingImPath_blur = [strrep(movingImPath(1:end-4),'SegmentedThresh/','SegmentedThreshBlur/'),'_blur.jpg'];
    imwrite(movingIm_preproc,movingImPath_blur,'Quality',100);

catch exception
    fprintf('Error opening image %s\n',movingImPath);
end


end
