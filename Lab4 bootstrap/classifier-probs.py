#!/usr/bin/python

'''
Folder Structure
 f50 - Contains train, test, unlabeled data
 model_out - contains output obtained from the models

Files:
 megam_i686.opt - Learner
 classifier-probs.py - Active Learner
 classifier.py - Passive Learner

Files Produceed:
 models from 1 to N (modelN)
 Unlabeled data from 1 to N (hufN)
 Training data + k from 1 to N (train.f0)

Files Renamed
 hypothetically_unlabelled has been renamed to huf0

Returns 
 List of tuples
 (traning datasize, accuracy)

Usage 
 ./classifier-probs.py <Number of Samples> <Type of Sampling>
'''

import sys
from math import exp, log
import codecs
import subprocess
reload(sys)
sys.setdefaultencoding('utf-8')

train_dict = {}
unlabel_dict = {}
test_dict = {}
sample_dict = {}

lbd={}
bias={}    
nclas=0    
score = []

def load_model(fname) :
  '''
  Populates the global variables used for the model
  '''
  global nclas,bias,lbd;
  model = codecs.open(fname, "r", "utf-8")
  lin=model.readline()
  bias=lin.split()
  bias=bias[1:len(bias)]
  nclas = len(bias)
  lin=model.readline(); 
  while (lin!="") :
    t=lin.split()
    for i in range(1,len(t)) :      
      lbd[t[0]+"#"+str(i-1)]=float(t[i])
    lin=model.readline()

def margin_sampling(coefficents):
  '''
  Implements Margin Sampling
  
  Returns:
   difference between top two samples
  '''
  sorted_coeff =  sorted(coefficents)
  margin = abs(sorted_coeff[-1] - sorted_coeff[-2])
  return margin

def entropy_sampling(coefficents):
  '''
  Implements Entropy Sampling
  To note that we are minimzing entropy. Hence negative sign removed

  Returns:
   Entropy based on values of coefficents
  '''
  entropy = sum(map(lambda x: x * log(x), coefficents))
  return entropy


def active_learning(type):
  '''
  Function that implements active learning based on sampling type
  1 - Maring Sampling
  2 - Entropy Sampling

  Populates the global variable margin_dict
  '''
  global margin_dict
 
  for key, line in unlabel_dict.iteritems():
    feat = line.split()
    tagOK = int(feat[0])
    p=[]
    z=0
    for c in range(0,nclas) :
      s=0 
      for f in range(1,len(feat),2) :
        s = s+lbd.get(feat[f]+"#"+str(c),0)*float(feat[f+1]) 

      p.append(exp(s+float(bias[c])))
      z = z+p[c]
    mx=0
    for c in range(0,nclas) :
      p[c] = p[c]/z
      if (p[c]>p[mx]):
        mx=c
    
    estimates = []
    for c in range(0,nclas) :
      estimates.append(p[c])
    if(type==1):
      sample_dict[key] = margin_sampling(estimates)
    sample_dict[key] = entropy_sampling(estimates)

def read_data(train_path, hyp_path, test_path):
  '''
  Populates global dictionaries that hold our data
  '''
  global train_dict,unlabel_dict,test_dict
  index = 0
  model1 = codecs.open(train, "r", "utf-8")
  model2 = codecs.open(hyp_path, "r", "utf-8")
  model3 = codecs.open(test_path, "r", "utf-8")
  
  line1 = model1.readline()
  while (line1!="") :
    index += 1
    train_dict[index] = line1
    line1 = model1.readline()
 
  line2 = model2.readline()
  while (line2!="") :
    index += 1
    unlabel_dict[index] = line2
    line2 = model2.readline()

  line3 = model3.readline()
  while (line3!="") :
    index += 1
    test_dict[index] = line3
    line3 = model3.readline()   


def build_model(model_no, train_data):
  '''
  Generates the probability values the trainig data learns.
  Returns
    Model path
  '''
  model_name = "megam_i686.opt"
  parameters = "  -quiet -fvals multiclass "
  model_op = "model_out/model"
  model_path = model_op + str(model_no) + '.mem'
  model_string = "./" + model_name + parameters + train_data + ">" + model_path
  build_model = subprocess.call(['bash','-c', model_string])
  return model_path


def test_accuracy():
  '''
  Method to check model accuracy on the testing set
  Returns:
    Accuracy
  '''
  ntot=0
  nok=0

  for key, line in test_dict.iteritems():
    feat=line.split()
    tagOK = int(feat[0])
    p=[]
    z=0
    for c in range(0,nclas) :
      s=0 
      for f in range(1,len(feat),2) :
        s = s+lbd.get(feat[f]+"#"+str(c),0)*float(feat[f+1])
      p.append(exp(s+float(bias[c])))
      z = z+p[c]
 
    mx=0
    for c in range(0,nclas) :
      p[c] = p[c]/z
      if (p[c]>p[mx]):
         mx=c

    if (mx==tagOK):
      nok = nok+1
    ntot = ntot+1
  acc = 100.0*nok/ntot
  return(acc)

def data_consolidation(topk):
  '''
  This method adds data to training set based on number of samples selected 
  and removes these samples from the unlabeled data.
  '''
  sorted_margin = sorted(sample_dict.items(), key=lambda e: e[1])
  for k,v in sorted_margin[0:int(topk)]:
    train_dict[k] = unlabel_dict[k]
    del unlabel_dict[k]

def write_fs(index):
  '''
  Writes output
  To prevent confusion this method write to different files instead 
  of the same file.
  '''
  train = open('f50/train.f' + str(index), 'w')
  for key, line in train_dict.iteritems():
    train.write(line)
  hu = open('f50/huf'+ str(index), 'w')
  for key, line in unlabel_dict.iteritems():
    hu.write(line)
  train_dict.clear();unlabel_dict.clear();margin_dict.clear()
  

if __name__ == '__main__':
  select_k = sys.argv[1]
  sample_type = sys.argv[2]
  for i  in range(0,12):
    train = 'f50/train.f' + str(i)
    ul = 'f50/huf' + str(i)
    files = [train, ul, 'f50/test']
    read_data(files[0],files[1],files[2])
    model_path = build_model(i,train)
    load_model(model_path)
    accuracy  = test_accuracy()
    report = (len(train_dict),accuracy)
    active_learning(sample_type)
    data_consolidation(select_k)
    write_fs(i+1)
    score.append(report)

  print "Active Learning Output ",score


