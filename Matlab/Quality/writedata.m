function writedata(label_vector_train, instance_matrix_train,appendstr,instance_matrix_test, label_vector_test, dropboxpath, prob_estimates, predict_label, names)
libsvmwrite(['train',appendstr,'.txt'], label_vector_train, instance_matrix_train')
libsvmwrite(['test',appendstr,'.txt'], label_vector_test, instance_matrix_test')

dlmwrite([dropboxpath,'probestimates',appendstr,'.txt'], prob_estimates,'delimiter','\t')
dlmwrite([dropboxpath,'probestimatestrain',appendstr,'.txt'], prob_estimates_train,'delimiter','\t')

dlmwrite([dropboxpath,'labelestimates',appendstr,'.txt'], predict_label,'delimiter','\t')
dlmwrite([dropboxpath,'labels',appendstr,'.txt'], label_vector_test,'delimiter','\t')


fid=fopen([dropboxpath,'names',appendstr,'.txt'],'wt');

[rows,cols]=size(names{2});

for i=1:rows
fprintf(fid,'%s\n',names{2}{i,1:end-1});
fprintf(fid,'%s\n',names{2}{i,end});
end

fclose(fid);

end