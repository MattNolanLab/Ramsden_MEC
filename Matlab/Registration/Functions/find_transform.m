function [ res ] = find_transform( a , main , optim )



a(a==0)=nan;    % set zeros to nans, the black color here corresponds to the border
                % around the actual images. We exclude this border by
                % setting it to NaNs.

res=mirt2Dgroup_sequence(a, main, optim);  % find the transformation (all to the mean)
%b=mirt2Dgroup_transform(a, res);          % apply the transformation

% see the result
% for i=1:size(b,3), imshow(b(:,:,i)); drawnow; pause(0.1); end;

end
