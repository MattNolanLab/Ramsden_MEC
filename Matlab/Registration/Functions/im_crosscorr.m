function [  ] =  im_crosscorr(varargin)
% median first, then registered image

medpath     = varargin{1};
regpath     = varargin{2};
fid = varargin{3};


% first read median image = either true median or mask
try
    maskmed = imread(medpath);
    maskreg = imread(regpath);
    % now read in registered image - make sure type matches median

    % Now crop both images, making sure that reg is smaller
    maskmedcrop = maskmed(100:800,300:1000);
    maskregcrop = maskreg(200:650,600:1000);
%     imshow(maskregcrop)
    C = normxcorr2(maskregcrop,maskmedcrop);

    [max_cc,imax] = max(abs(C(:)));
    [ypeak,xpeak] = ind2sub(size(C),imax(1));
    corr_offset = [(ypeak-size(maskregcrop,1)),(xpeak-size(maskregcrop,2))];
    fprintf(fid,'%s\t%i\t%i\n',regpath,corr_offset(1),corr_offset(2));

catch exception
    %fprintf('Error opening image %s\n',regpath);
    fprintf(fid,'%s\t%s\n',exception.message,regpath);
end
end
