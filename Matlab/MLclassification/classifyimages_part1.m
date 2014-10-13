function [ ] = classifyimages()

% Notes -
%(1) once you've run an image through the classifer, its histogram will be stored in the cache forever, so next time you run the image it will be much quicker.
% (2) You run this in multiple stages.
% (a) First, you want to see how well the classifier can separate the groups for images that you have already looked at, so take all images that you consider to be 'positive' and all images that you consider to be 'negative' and move them into the 'Pos' and 'Neg' folders
% (b) Use randomTrainTestAssign (copy in pos folder and neg folder) to split the images into Train and Test
% (C) run code and see how well it classifies test data
% (d) optimise hyperparameters by uncommenting bottom section - C currently set at 100
% Once you've optimised the hyperparameter you're ready to run the code on new images that you haven't previously classified - see classifyimages_part2

diskpath = '';
commonpath = [diskpath,'data/'];
basepath = diskpath;
vocabpath = [commonpath,'vocabulary.mat'];

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

% Compute test from own images
pos.names = getImageSet(postestpath);
pos.histograms = computeHistogramsFromImageList(vocabulary, pos.names, cache_poshistograms) ;
neg.names = getImageSet(negtestpath);
neg.histograms = computeHistogramsFromImageList(vocabulary, neg.names, cache_neghistograms) ;

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

% C param validation
% C_params = [(0.001:0.001:0.1),(0.1:0.1:100),(101:1:1000)];
%
% ap_list = zeros(1,length(C_params));
% correct_topN = zeros(1,length(C_params));
%
% for i=1:length(C_params)

    % Train the linear SVM
    %C = 100; % default
    C = 100;  % best param value found on validation set
%
%     C = C_params(i);
    [w, bias] = trainLinearSVM(histograms, labels, C);

    % Evaluate the scores on the training data
    scores = w' * histograms + bias ;

    % Visualize the ranked list of images
     figure(1) ; clf ; set(1,'name','Ranked training images (subset)') ;
     displayRankedImageList(names, scores) ;

    % Visualize the precision-recall curve
     figure(2) ; clf ; set(2,'name','Precision-recall on train data') ;
     vl_pr(labels, scores);

    % --------------------------------------------------------------------
    % Stage C: Classify the test images and assess the performance
    % --------------------------------------------------------------------

    fprintf('Testing SVM..\n');

    % Test the linear SVM
    testScores = w' * testHistograms + bias ;

    % Visualize the ranked list of images
     figure(3) ; clf ; set(3,'name','Ranked test images (subset)') ;
     displayRankedImageList(testNames, testScores)  ;

    % Visualize the precision-recall curve
     figure(4) ; clf ; set(4,'name','Precision-recall on test data') ;
     vl_pr(testLabels, testScores) ;


    % Print results
    [drop,drop,info] = vl_pr(testLabels, testScores) ;
    fprintf('Test AP: %.2f\n', info.auc) ;

    [drop,perm] = sort(testScores,'descend') ;
    topN = 20;
    fprintf('Correctly retrieved in the top %d: %d\n',topN,sum(testLabels(perm(1:topN)) > 0)) ;

    % record validation set stats
%     fprintf('C param %d of %d\n',i,length(C_params));
%     ap_list(i) = info.auc;
%     correct_topN(i) = sum(testLabels(perm(1:topN)) > 0);
% end % end C param

% fprintf('%d',max(C_params));

% write test scores to disk?
writeNamesScores( testNames, testScores,basepath );

end
