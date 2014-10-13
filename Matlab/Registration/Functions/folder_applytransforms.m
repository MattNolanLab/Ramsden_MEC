function [  ] = folder_applytransforms( varargin )

%apply_transforms_outofcore( path_to_transforms , path_to_images );

if isempty(varargin)
  filepathMAT = pwd;
  filepathIM  = pwd;
elseif length(varargin)==3
  filepathMAT = varargin{1};
  filepathIM  = varargin{2};
  fileext = varargin{3};

else
  error('unknown input length');
end

if ispc
    slash = '\';
elseif isunix || ismac
    slash = '/';
else
    error('unsupported OS');
end

% add slash if needed
if ~strcmp(filepathMAT(end),slash)
  filepathMAT(end+1) = slash;
end

% find non-rigid reg files 
%cd(filepathMAT);
mat_files = dir([filepathMAT,'*res.mat']);
numReg = length(mat_files);

if numReg == 0 
 error('No registration files found in this dir!%s',filepathMAT);
end

noMatches    = 0;
ambigMatches = 0;

for i=1:numReg
    res_filename = mat_files(i).name;
    fprintf('registering image %d of %d\n',i,numReg);  
    % load res file
    res = load([filepathMAT,filesep,res_filename]);
    % take out of structure
    res = res.res;
    % find jpg with matching file num
    % ASSUME: this num is unique to each image (and always at the start
    % of the file name).
    %s = regexp(reg_filename, '[0-9]+_[^_]+_[0-9]+', 'match')
    s = regexp(res_filename, '[0-9]+[\w]?_[^_]+_[0-9]+', 'match');
    fileNum = s{1};
    % build up pattern match 
    pat = [fileNum,fileext];
    
    jpg_files = dir([filepathIM,pat]);
    % sanity check
    
    if length(jpg_files)~=1
        fprintf('could not match file number uniquely! (num matches = %d for pat: %s)\n',length(jpg_files),fileNum);
        
        if length(jpg_files)>1
         ambigMatches = ambigMatches+1;
        end
        if length(jpg_files)<1
         noMatches = noMatches+1;
        end
        continue;
    end
    jpg_filename = jpg_files(1).name;
    try
        im = imread([filepathIM,filesep,jpg_filename]);
    catch exception
        fprintf('Error opening image %s\n',pat);
        continue
    end
    % convert
    im = double(im);
    im = im/255;
    % transform image
    reg_im=mirt2D_transform(im, res);
    % write transformed image to disk
    if ~exist([filepathIM(1:end-1),'Reg'],'dir')
        mkdir([filepathIM(1:end-1),'Reg/']);
    end
    reg_filepathIM = [filepathIM(1:end-1),'Reg/'];
    reg_filename = [jpg_filename(1:end-4),'_reg.tif'];
    filepathIM_filename = [reg_filepathIM,filesep,reg_filename];
    imwrite(reg_im,filepathIM_filename);%,'Quality',100);
 
end

failCount = noMatches+ambigMatches;
fprintf('%d of %d transforms applied successfully\n',numReg-failCount,numReg);

if failCount>0
    fprintf('WARNING: Could not perform transform on %d images (%d no matches and %d ambig matches)\n',failCount,noMatches,ambigMatches);
end


























