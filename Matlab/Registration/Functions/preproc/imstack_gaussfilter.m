function [ imstack_gauss ] = imstack_gaussfilter( imstack )

% default
windowSize = 13;
stdDev     = 3;

% define filter
h = fspecial('gaussian', [windowSize windowSize] , stdDev);
% get imstack size
[r,c,d] = size(imstack);

fprintf('Applying %dx%d gaussing filter (std=%.2f) to %d images\n',windowSize,windowSize,stdDev,d);

for i=1:d
    fprintf('%d of %d\n',i,d);
    im = imstack(:,:,i);
    imgauss=imfilter(im, h,'replicate');
    imstack_gauss(:,:,i) = imgauss;   
end

end

