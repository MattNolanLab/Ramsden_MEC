function [ adjusted_imstack ] = imstack_imadjust( imstack )


[r,c,d] = size(imstack);

fprintf('Applying imadjust filter to %d images\n',d);

for i=1:d
    fprintf('%d of %d\n',i,d);
    im = imstack(:,:,i);
    adjusted_im=imadjust(im);
    adjusted_imstack(:,:,i) = adjusted_im;   
end

end


