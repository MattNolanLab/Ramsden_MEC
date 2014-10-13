
movingFolderPath = 'Example_Results/Images/ML3/Segmented/';
movingFolder='SegmentedThreshBlurTransforms/'

%If using filtered
%movingFolder='SegmentedThreshFilterTransforms/'

folder_applytransforms([movingFolderPath,movingFolder],[movingFolderPath, 'SegmentedExp/'],'*.tif');

folder_applytransforms([movingFolderPath,movingFolder],[movingFolderPath, 'SegmentedOrig/'],'*.jpg');