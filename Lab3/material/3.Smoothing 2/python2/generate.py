##
## Loads a MLE trigram model, and uses it to generate
## sequences of given length.
##
##  Usage:   python3 generate.py model.dat length
##

import sys
import random
import codecs

## ----------------------------------
## Global variables 
ptr={}  # trigram probabilities
ug={} # unigram probabilities

## ---------------------------------
## Load MLE model in given file into 'ptr'
def loadModel(fname) :
  # open file
  model = codecs.open(fname, "r", "utf-8")

  # load rest of lines into ptr
  lin=model.readline(); 
  while (lin!="") :
    t=lin.split(" ")
    ptr[t[0]] = float(t[1])

    # seen unigrams
    ug[t[0][2]]=1

    lin=model.readline();

## ---------------------------------
## Given a bigram xy, randomly select z, according 
## to distribution in ptr
def transition(xy) :
    r=random.random()
    s=0.0
    for z in ug : 
      if (xy+z in ptr):
        s = s +  ptr[xy+z]
      if (s>r) :
        return z


## MAIN ---------------------

## -- load MLE trigram model
loadModel(sys.argv[1])
## length to generate
maxc = int(sys.argv[2])

## select a random initial state ".#z" using probabilities in ptr
## COMPLETE THIS
x= ??; y=??;
z= ??
 
sys.stdout.write(z.encode("utf-8"))
for i in range(1,maxc) :
  # next state
  ## select a random next state, according to transition probabilities
  ## COMPLETE THIS
  x=??; y=??;
  z=??

  ## write character for selected state.
  if (z=="#") :
    sys.stdout.write(" ")
  else :
    sys.stdout.write(z.encode("utf-8"))

sys.stdout.write("\n");
