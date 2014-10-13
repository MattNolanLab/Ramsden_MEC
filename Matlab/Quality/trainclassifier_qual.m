% Input: folder containing all images for SVM to possibly use
% Need a file containing file labels  - import this to give label_vector
commonpath = 'ABAclassification/';
imagepath = 'MECImages/';

cache_poshistograms =[imagepath,'/cache/']; % change this depending on whether you want full arrays or sub arrays
qualgroups = {'/Training/Quality/AllPoor/','/Training/Quality/NotPoor/'}; % for training

slice_ml = 'ML3';
appendstr = '_qual_ml3';
vocabpath = [imagepath,'/ALL/test/vocabulary.mat']; % e means full images, filtered

% --------------------------------------------------------------------
% Stage preA: Get vocabulary by running preprocess.m
% --------------------------------------------------------------------


% --------------------------------------------------------------------
% Stage A: Data Preparation - extract all histograms
% --------------------------------------------------------------------
%
vocabulary = load(vocabpath);
[instance_matrix_train,label_vector_train,instance_matrix_test,label_vector_test, labellengths,names] = extractimagefeatures(imagepath, commonpath,qualgroups,cache_poshistograms,slice_ml,vocabulary.vocabulary);
[instance_matrix_train_s, instance_matrix_test_s] =  scaledata(instance_matrix_train, instance_matrix_test);

 % % % --------------------------------------------------------------------
% need label vector to correspond with histograms
label_vector_train(label_vector_train ==2) = -1;
label_vector_test(label_vector_test ==2) = -1;
libsvmwrite(['train',appendstr,'.txt'], label_vector_train, instance_matrix_train')
libsvmwrite(['test',appendstr,'.txt'], label_vector_test, instance_matrix_test')
%
%
% % % --------------------------------------------------------------------
% % % Stage Ba: Find best parameters
%
% % labellengthsadj = sum(labellengths)./labellengths; % this enables the classes to be appropriately weighted
labellengthsadj = [1 1];
kerneltype = num2str(2); % 2 is a radial basis function, 0 is linear?
[bestc, bestg,model] = findbestparams(kerneltype, labellengthsadj, label_vector_train, instance_matrix_train);

% % --------------------------------------------------------------------
% % Stage Bb: Training
% % --------------------------------------------------------------------


% %  % you need to fix this manually is the training data proportions don't reflect reality
% costparameter = num2str(1);
% gamma = num2str(bestgamma);
% regularisation = num2str(bestc);

%
% optionsstr = ['-c ',costparameter,' -g ',gamma,' -r ', regularisation,' -b 1 -t ',kerneltype, ' -w1 ',  num2str(labellengthsadj(1)), ' -w2 ', num2str(labellengthsadj(2))];
%
% modelqual = svmtrain(label_vector_train,instance_matrix_train' ,optionsstr);

% --------------------------------------------------------------------
% Stage C: Prediction
% --------------------------------------------------------------------

% [predict_label_train, accuracy_train, prob_estimates_train] =
%svmpredict(label_vector_train, instance_matrix_train', model3, '-b 1');
% [predict_label, accuracy, prob_estimates] =
%svmpredict(label_vector_test, instance_matrix_test', model3, '-b 1');
%
% % --------------------------------------------------------------------
% % Stage D: Write data to file
% % --------------------------------------------------------------------
%
% % % Make figure showing best images
% fig = figure(3) ; clf ; set(3,'name','Ranked train images (subset)') ;
% if length(prob_estimates_train)>50
%     ind=50;
% else
%     ind = length(prob_estimates_train);
% end
% displayRankedImageList(names{1}(1:ind), prob_estimates_train(1:ind,1), dropboxpath, appendstr)
% saveas(fig,[commonpath,'probestimates',appendstr,'.png'],'png');

% writedata(label_vector_train,instance_matrix_train,appendstr,instance_matrix_test, label_vector_test, dropboxpath, prob_estimates, predict_label, names)

% makeplots()
