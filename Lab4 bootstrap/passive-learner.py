#!/usr/bin/env python
# TODO
# Train Count
# Accuracy

'''
Passive Learner Wrapper that works on the complete training data and gets 
accuray for the test set.
'''
import subprocess


train_data = 'f50/train'
model_no = 'C'
model_name = "megam_i686.opt"
parameters = "  -quiet -fvals multiclass "
model_op = "model_out/model"
model_path = model_op + model_no + '.mem'
model_string = "./" + model_name + parameters + train_data + ">" + model_path
build_model = subprocess.call(['bash','-c', model_string])


test_data = 'f50/test'
op_file = 'probs/testC.txt'
model_path = 'model_out/modelC.mem'
input_string = 'python classifier.py '+ model_path + '<'+ test_data +  ">" + op_file
build_prob = subprocess.call(['bash','-c', input_string])


accuracy_string =  'tail -1 probs/testC.txt | cut -d" " -f2-'
print subprocess.call(['bash','-c', accuracy_string])

count_train = 'cat f50/train | wc -l'
subprocess.call(['bash','-c', count_train])

