
medimage  = 'ML3_median_image_resize_0.2_filter.jpg'
movingFolder = 'SegmentedThresh_blur_Registered/'

% If filtered - change
%medimage  = 'ML3_median_image_resize_0.2_filter.jpg'
%movingFolder = 'SegmentedThresh_blur_Registered/'

medpath = ['Example_Results/Images/Median/',medimage];
regpath =['Example_Results/Images/ML3/Segmented/',movingFolder];
folder_crosscorr( medpath ,regpath );
