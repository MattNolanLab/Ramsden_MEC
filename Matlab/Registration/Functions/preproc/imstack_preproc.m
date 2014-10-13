function [ imstack ] = imstack_preproc( imstack )

% apply gaussian blur
gaussIter = 3;

for i=1:gaussIter
 [ imstack ] = imstack_gaussfilter( imstack );
end
% apply contrast adjust
[ imstack ] = imstack_imadjust( imstack );

end

