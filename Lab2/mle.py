import sys
t1={}  # unigram counts
t2={}  # bigram counts
t3={}  # trigram counts
n=0    # total characters

def increment(t,c,x): 
  if (c in t):
    t[c]=t[c]+x
  else:
    t[c]=x


def readText() :
  global n,t1,t2,t3
  l1=sys.stdin.readline().decode("utf-8")
  l1=l1.lower();
  while (l1!=""):
    l2=sys.stdin.readline().decode("utf-8")
    l2=l2.lower();

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
    print l1

readText()


