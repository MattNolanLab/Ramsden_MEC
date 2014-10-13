function [ im ] = removeblackBG( im )


% connected components with area (px count) larger than minArea and 
% that contain at least 1 pixel on the image border will be set to 255.0
minArea = 10;

% (requires image toolbox)

% binarize
bwim = my_im2bw(im);
% assume largest (-ve) components are the rigid rotation border
s = regionprops(~bwim,{'Area','PixelIdxList'});

% remove all connected components with more than n pixels

componentList = find([s.Area] > minArea);
for i=1:length(componentList)
   
    idx = s(componentList(i)).PixelIdxList;
    
    % get image positions
    [idx_i,idx_j] = ind2sub(size(bwim),idx);
    % test to make sure this connected component has at least 1 pixel
    % existing on the image border
    borderTest1=any(idx_i==1);
    borderTest2=any(idx_i==(size(bwim,1)));
    borderTest3=any(idx_j==1);
    borderTest4=any(idx_j==(size(bwim,2)));
    
    % only remove the component if it has pixels connected to the border
    % (so we do not accidently remove bits of mouse brain)
    if (borderTest1 || borderTest2 || borderTest3 || borderTest4)
     im(idx) = 255.0;  
    end
end


end

