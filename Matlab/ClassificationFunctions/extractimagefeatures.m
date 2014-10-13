function [shistograms_train,label_vector_train,shistograms_test,label_vector_test,lengthlabelstrain,names] = extractimagefeatures(imagepath,commonpath,groups,cache_poshistograms, slice_ml,vocabulary)

% add required search paths
setup;

fprintf('Loading Training data..\n');

% Compute positive histograms from training images
testtrain = {'/train/','/test/'};


for j=1:length(testtrain)
    names = [];
    label_vector = [];
    lengthlabels = [];
    % Iterate around subfolders
    for i=1:length(groups)
     
     trainpath =[imagepath,groups{i},testtrain{j}];   
     tmpnames = getImageSet(trainpath, slice_ml);
     
     label_vector = [label_vector,ones(1,length(tmpnames))*i]; 

     names = [names,tmpnames];
     lengthlabels = [lengthlabels,length(tmpnames)];
    end

    histograms = computeHistogramsFromImageList(vocabulary, names, cache_poshistograms);

    % Hellinger's kernel (histograms are l1 normalized)
    histograms = sqrt(histograms) ;
    histograms = double(histograms);

    shistograms = sparse(histograms);
    
    if j==1
        label_vector_train = label_vector';
        shistograms_train = shistograms;
        lengthlabelstrain = lengthlabels;
        namestrain = names;
    else
        label_vector_test = label_vector';
        shistograms_test = shistograms;
        lengthlabelstest = lengthlabels;
        namestest = names;
    end

    

end
names = {namestrain,namestest};
end

