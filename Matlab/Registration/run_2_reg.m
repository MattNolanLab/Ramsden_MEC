addpath(genpath('Matlab/'))

movingFolderPath = 'Example_Results/Images/';
movingFolder ='Segmented/SegmentedThreshBlur'
medImPath = [movingFolderPath,'Median/ML3_median_image_resize_0.2_filter.jpg'];

% Possible improvement: median filter applied to both median and moving images
% medImPath = [movingFolderPath,'Median/ML3_median_image_resize_0.2_bc_med5_bc.jpg'];
movingFolder ='Segmented/SegmentedThreshFilter'

folder_reg([ movingFolderPath,'ML3/'] , medImPath )
