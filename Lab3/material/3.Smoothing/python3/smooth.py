##
## Loads a MLE trigram model, and uses it to compute
## the probabilitity of the input sequence, smoothing
## unseen events
##
##  Usage:   python3 smooth.py model.dat <text
##

import sys


## ----------------------------------
## Global variables 
ptr={} # trigram probabilities P(z|xy)
ctr={} # trigram absolute counts (xyz)
cbr={} # bigram absolute counts (xy)
cur={} # unigram absolute counts (xy)
ntr=0   # total observations

## ---------------------------------
## increment (or initialize if needed) in 'x'
## the count of 'c' in table 't'
def increment(t,c,x): 
  if (c in t):
    t[c]=t[c]+x
  else:
    t[c]=x

## ---------------------------------
## Load MLE model in given file into 'ptr'
def loadModel(fname) :
  global ntr,ctr,cbr,cur
  # open file
  model = open(fname, encoding='utf-8')

  # load rest of lines into ptr
  lin=model.readline(); 
  while (lin!="") :
    t=lin.split()
    ptr[t[0]] = float(t[1])  # trigram prob P(z|xy)
    ctr[t[0]] = float(t[2])  # trigram (xyz) count
    cbr[t[0][0:2]] = float(t[3]) # bigram (xy) count 
    increment(cur,t[0][2],float(t[2])) # unigram (z) count
    ntr=ntr+float(t[2]);
    lin=model.readline();

## ---------------------------------
## Lidstone smoothing
def lidstone(ngram,counts,B,N,l) :
  if (ngram in counts) :
    c = counts[ngram]
  else :
    c = 0.0

  return (c+l)/(N+B*l)

## ---------------------------------
## Laplace smoothing
def laplace(ngram,counts,B,N) :
  return lidstone(ngram,counts,B,N,1.0)


## ---------------------------------
## Given trigram xyz, compute smoothed
## transition probability P(z|xy)
def ptrig(trig) :
 
  if (trig in ptr):
    return ptr[trig]
  else:
    return 0.0

  ## REPLACE THE TRIGRAM PROBABILITY COMPUTATION ABOVE BY
  ## A SMOOTHING USING LAPLACE OR LIDSTONE LAWS
  ## You need to :
  ## 1) Compute smoothed probability of trigram: P(xyz)
  ## 2) Compute smoothed probability of bigram: P(xy)
  ## 3) Compute transition probability P(z|xy) = P(xyz)/P(xy)


## MAIN ---------------------

## -- load MLE trigram model
loadModel(sys.argv[1])

## -- load input sentence/s
text=""
for line in sys.stdin:
   line=line.lower()
   line=line.replace("\n","#")
   line=line.replace(" ","#")
   text=text+line

## compute input probability
prob=1.0;
for i in range(0,len(text)-3):
   x=text[i]; y=text[i+1]; z=text[i+2] 
   pt = ptrig(x+y+z)
   prob = prob * pt
   sys.stdout.write(x+y+z+" "+str(pt)+" "+str(prob)+"\n")

sys.stdout.write("Sequence probability: "+str(prob)+"\n")
