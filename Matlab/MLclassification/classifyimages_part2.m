function [ ] = classifyimages(diskpath)

% Notes - see part1

commonpath = [diskpath,'/practical_image_registration/data/'];
basepath = [diskpath,'/practical_image_registration/'];
vocabpath = [commonpath,'/vocabulary.mat'];

postrainpath =[commonpath,'/Pos/Train/']; % positive training images
postestpath =[commonpath,'/Pos/Test/'];% positive testing images
cache_poshistograms =[commonpath,'/cache/Images_Train/']; % this is where histograms for training images will be stored
negtrainpath = [commonpath,'/Neg/Train/'];% negative training images
negtestpath = [commonpath,'/Neg/Test/'];% negative testing images
cache_neghistograms = [commonpath,'/cache/Images_Train/'];

% Specify path for where all your test images are
testimagepath = ['/Users/helenlramsden/Desktop/TempImages/'];

% This is where test image histograms will be saved
testhistograms = [commonpath,'/cache/Images_Test/'];

% add required search paths
setup;

% --------------------------------------------------------------------
% Stage A: Data Preparation
% --------------------------------------------------------------------
vocabulary = load(vocabpath) ;

fprintf('Loading Training data..\n');

% Compute positive histograms from training images
pos.names = getImageSet(postrainpath);
pos.histograms = computeHistogramsFromImageList(vocabulary, pos.names, cache_poshistograms);
neg.names = getImageSet(negtrainpath);
neg.histograms = computeHistogramsFromImageList(vocabulary, neg.names, cache_neghistograms);

names = {pos.names{:}, neg.names{:}};
histograms = [pos.histograms, neg.histograms];
labels = [ones(1,numel(pos.names)), - ones(1,numel(neg.names))];
clear pos neg;

fprintf('Loading Test data..\n');

% Compute test from own images that you have not assigned a label to
pos.names = getImageSet(testimagepath);
pos.histograms = computeHistogramsFromImageList(vocabulary, pos.names, testhistograms) ;
neg.names = {};
neg.histograms = [];

testNames = {pos.names{:}, neg.names{:}};
testHistograms = [pos.histograms, neg.histograms] ;
testLabels = [ones(1,numel(pos.names)), - ones(1,numel(neg.names))] ;
clear pos neg;


% count how many images are there
fprintf('Number of training images: %d positive, %d negative\n', ...
    sum(labels > 0), sum(labels < 0)) ;
fprintf('Number of testing images: %d positive, %d negative\n', ...
    sum(testLabels > 0), sum(testLabels < 0)) ;

% Hellinger's kernel (histograms are l1 normalized)
histograms = sqrt(histograms) ;
testHistograms = sqrt(testHistograms) ;

% --------------------------------------------------------------------
% Stage B: Training a classifier
% --------------------------------------------------------------------

fprintf('Training SVM..\n');

C = 100;  % best param value found on validation set - see part1

[w, bias] = trainLinearSVM(histograms, labels, C);
    
% Evaluate the scores
scores = w' * histograms + bias ;
    
fprintf('Testing SVM..\n');
    
% Test the linear SVM
testScores = w' * testHistograms + bias ;

% Print results
[drop,drop,info] = vl_pr(testLabels, testScores) ;
fprintf('Test AP: %.2f\n', info.auc) ;

[drop,perm] = sort(testScores,'descend') ;
topN = 100;
fprintf('Correctly retrieved in the top %d: %d\n',topN,sum(testLabels(perm(1:topN)) > 0)) ;
    
% write test scores to disk?
writeNamesScores( testNames, testScores,basepath );

end

