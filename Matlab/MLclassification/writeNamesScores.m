function [  ] = writeNamesScores( names, scores,basepath )

% This function writes the results of the classification to disk. You can parse this

% create unique filename
dateTime = regexp(datestr(now), ' ', 'split');
theDate = dateTime{1};
theTime = dateTime{2};

%basepath = '/disk/scratch/practical-image-classification/';

filename = ['classifications_',theDate,'_',theTime,'.log'];

% open file
fid = fopen([basepath,filename],'a+');

% just write each line in turn for now
for i=1:length(names)
 fprintf(fid,'%s %.10f\n',names{i},scores(i));
end

% close file
fclose(fid);

end

