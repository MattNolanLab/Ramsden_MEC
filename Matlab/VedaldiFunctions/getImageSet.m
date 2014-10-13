function names = getImageSet(path,slice_ml)
% GETIMAGESET  Scan a directory for images
%   NAMES = GETIMAGESET(PATH) scans PATH for JPG, PNG, JPEG, GIF,
%   BMP, and TIFF files and returns their path into NAMES.

% Author: Andrea Vedaldi

content = dir(path);
names = {content.name} ;
ok = regexpi(names, [slice_ml,'.*\.(jpg|png|jpeg|gif|bmp|tiff|tif)$'], 'start') ; % for slice, need underscore in label
names = names(~cellfun(@isempty,ok));

for i = 1:length(names)
  names{i} = fullfile(path,names{i}) ;
end
