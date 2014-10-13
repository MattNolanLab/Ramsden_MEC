function im = imageprocessing(im)
im = im;
%   imshow(im)
%% If you want to mask the image
im = maskim(im);
im = double(im);
%% If you want to smooth the iamge
%   im = vl_imsmooth(im,5);

%   im = imstack_gaussfilter(im,10,3);
%   imshow(im)

%% Median filter the image
%     imshow(im)
im = medfilt2(im,[2 2]); %4 4 for default

end
