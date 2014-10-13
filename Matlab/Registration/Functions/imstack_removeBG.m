function [ imstack ] = imstack_removeRotBG( imstack )

fprintf('Attempting to remove rigid rotation border..\n');

[r,c,d] = size(imstack);

numIm = d;

for i=1:numIm
    fprintf('%d of %d\n',i,numIm);
    im = imstack(:,:,i);
    im = removeblackBG(im);
    imstack(:,:,i) = im;
    
end


end

