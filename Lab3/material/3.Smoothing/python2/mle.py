##
## Estimates (via MLE) the parameters of a character 
## trigram model using the given corpus as training data.
##
## Usage:  python2 mle.py <corpus.txt >model.dat

import sys

## ----------------------------------
## Global variables 
t1={}  # unigram counts
t2={}  # bigram counts
t3={}  # trigram counts
n=0    # total characters


## ---------------------------------
## increment (or initialize if needed) in 'x'
## the count of 'c' in table 't'
def increment(t,c,x): 
  if (c in t):
    t[c]=t[c]+x
  else:
    t[c]=x

## ---------------------------------
## Read input text and store occurrence count
## for each 1,2,3-gram in tables t1,t2,t3.
def readText() :
  global n,t1,t2,t3
  l1=sys.stdin.readline().decode("utf-8"); l1=l1.lower();
  while (l1!=""):
    l2=sys.stdin.readline().decode("utf-8"); l2=l2.lower();

    buff=l1+l2;  
    buff=buff.replace("\n","#")
    buff=buff.replace(" ","#");

    mx = len(l1)-1
    if (len(l2)<2) : 
      mx = mx - (2-len(l2))

    for i in range(0,mx):
      increment(t1, buff[i],1.0)
      increment(t2, buff[i]+buff[i+1],1.0)
      increment(t3, buff[i]+buff[i+1]+buff[i+2],1.0)

    n=n+len(l1);
    l1=l2


## MAIN ---------------------

## -- read text and compute n-gram occurrences
readText()

## -- Compute model parameters, and output them to stdout
## output trigram probs P(z|xy) and absolute frecuencies of xyz and xy
for tg in t3 :
  x=tg[0]; y=tg[1]; z=tg[2];

  if (x+y in t2) :
    ## COMPLETE THIS
    count_tg = ???
    count_bg = ???
    prob_tg = ???
    sys.stdout.write(tg.encode("utf-8")+" "+str(prob_tg)+" "+str(count_tg)+" "+str(count_bg)+"\n")
    

