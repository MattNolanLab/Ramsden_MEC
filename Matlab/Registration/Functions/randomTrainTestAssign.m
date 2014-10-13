function [  ] = randomTrainTestAssign()

filepath = pwd;
files = dir('*.png');

trainImCount=0;
testImCount =0;

for i=1:length(files)
   
    % flip a coin to decide whether image is train or test
    if rand() > .5
       moveDir = '/Train/';
       trainImCount = trainImCount+1;
    else
       moveDir = '/Test/'; 
       testImCount = testImCount+1;
    end
    
    % build up destination dir
    destDir = [filepath,moveDir];
    % move image
    system(['mv ',files(i).name,' ',destDir]);
    
end

fprintf('Moved %d training images and %d test images\n',trainImCount,testImCount);

end

