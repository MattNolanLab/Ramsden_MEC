function [bestc, bestg,model] = findbestparams(kerneltype, labellengthsadj, label_vector_train, instance_matrix_train)

bestcv = 0;
for log2c = -5:2:15,
  for log2g = -15:2:3,
    costparameter = num2str(2^log2c);
    gamma = num2str(2^log2g);
    optionsstr = ['-v 5 -q -c ',costparameter,' -g ',gamma,' -t ',kerneltype, ' -w1 ',  num2str(labellengthsadj(1)), ' -w2 ', num2str(labellengthsadj(2))];
    optionsstr = ['-q -c ',costparameter,' -g ',gamma,' -t ',kerneltype, ' -w1 ',  num2str(labellengthsadj(1)), ' -w2 ', num2str(labellengthsadj(2))];
    
    % do_binary_validation allows me to train using metrics other than accuracy, which
    % isn't that useful
    cv = do_binary_cross_validation(label_vector_train,instance_matrix_train,optionsstr, 5);
%     cv = svmtrain(label_vector_train,instance_matrix_train' ,optionsstr);
    if (cv >= bestcv),
      bestcv = cv; bestc = 2^log2c; bestg = 2^log2g;
    end
    fprintf('%g %g %g (best c=%g, g=%g, rate=%g)\n', log2c, log2g, cv, bestc, bestg, bestcv);
  end
end
costparameter = num2str(bestc);
gamma = num2str(bestg);
optionsstr = [' -q -c ',costparameter,' -g ',gamma,' -b 1 -t ',kerneltype, ' -w1 ',  num2str(labellengthsadj(1)), ' -w2 ', num2str(labellengthsadj(2))];
model = svmtrain(label_vector_train,instance_matrix_train' ,optionsstr);

end