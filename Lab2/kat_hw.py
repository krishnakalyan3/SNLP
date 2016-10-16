
# coding: utf-8

# In[1]:

import re
from string import *
import sys
from nltk import *
import math
import time

start_time = time.time()

def importingBrownCorpusFromNLTK(outF):
    "importing tagged brown corpus from NLTK and writing on a file OutF"
    outF = open(outF,'w')
    from nltk.corpus import brown
    brown_news_tagged = brown.tagged_words(categories='news',simplify_tags=True)
    print ('size', len(brown_news_tagged))
    for i in brown_news_tagged:
        outF.write(i[0]+'\t'+i[1]+'\n')
    outF.close()

def getWordsFromFile(inF):
    "get a list of words from a text file"
    lines = map(lambda x:x.replace('\n','').lower(),open(inF).readlines())
    words=[]
    for line in lines:
        for word in line.split():
            words.append(word)
    print (len(words),'words read')
    return words

def getTaggedWordsFromFile(inF):
    "get a list of pairs <word,POS> from a text file"
    lines = map(lambda x:x.replace('\n','').lower(),open(inF).readlines())
    words=[]
    for line in lines:
        word,pos = line.split('\t')
        words.append((word,pos))
    print (len(words),'tagged words read')
    return words

def getTagsFromTaggedWords(l):
    "from a list of tagged words build a list of tags"
    return map(lambda x:x[1],l)

def countNgrams(l,inic,end=0):
    """
    From a list l (of words or pos), an inic position and an end position
    a tuple(U,B,T) of dics corresponding to unigrams, bigrams and trigrams are built
    """
    if end == 0:
        end = len(l)
    U={}
    B={}
    T={}
    U[(l[inic])]=1
    if (l[inic+1]) not in U:
        U[(l[inic+1])]=1
    else:
        U[(l[inic+1])]+=1
    B[(l[inic],l[inic+1])]=1
    for i in range(inic+2,end):
        if (l[i]) not in U:
            U[(l[i])]=1
        else:
            U[(l[i])]+=1
        if (l[i-1],l[i]) not in B:
            B[(l[i-1],l[i])] = 1
        else:
            B[(l[i-1],l[i])] +=1
        if (l[i-2],l[i-1],l[i]) not in T:
            T[(l[i-2],l[i-1],l[i])] = 1
        else:
            T[(l[i-2],l[i-1],l[i])] +=1
    return (U,B,T)


# reading the corpus

taggedWords = getTaggedWordsFromFile("../data/taggedBrown.txt")
enWords = getWordsFromFile("../data/tagged_brown_en.txt")


ngrams_en = countNgrams(enWords,0,0)

U = ngrams_en[0]
B = ngrams_en[1]
T = ngrams_en[2]


# In[62]:

# function for calculating the entropy of unigram, bigram and trigram model of the corpus

def getH(corpus):
    en_prob = list(corpus[0].values())
    sums = sum(en_prob)
    en_prob = [x / sums for x in en_prob] 
    plogp_en = [x*math.log(x,2) for x in en_prob] 
    h_1 = -sum(plogp_en) 
    
    keys_uni = corpus[0].keys()
    dict_uni = dict(zip(keys_uni, en_prob))

    dict_bi = {}
    U = corpus[0]
    B = corpus[1]
    T = corpus[2]
    for k in B.keys():
        x = k[0]
        dict_bi[k] = B[k] * 1.0/U[x] 
        h_2 = 0.0
    for key in dict_bi.keys():
        x = key[0]
        y = key[1]
        p_yx = dict_bi[key]
        p_x = dict_uni[x]
        h_2 -= p_x * p_yx * math.log(p_yx, 2.0)
    
    dict_tri = {}
    for k in T.keys():
        x = k[0]
        y = k[1]  
        dict_tri[k] = T[k] * 1.0/ B[(x,y)]
    h_3 = 0.0
    for key, value in T.items():
        x = key[0]
        y = key[1]
        z = key[2]
        p_x = dict_uni[x]
        p_yx = dict_bi[(x,y)]
        p_zxy = dict_tri[key]
        h_3 -= p_x * p_yx * p_zxy * math.log(p_zxy, 2.0)
    return (h_1, h_2, h_3)


# In[61]:

# entropy for unigram, bigram and trigram models of the english corpus

H_uni, H_bi, H_tri  = getH(ngrams_en)


print("\nEntropy for unigram, bigram and trigram models of the english corpus\n\nH unigram (en) = ", 
      H_uni, "\nH bigram (en) = ", H_bi,"\nH trigram (en) = ", H_tri)


# In[5]:

# getting Ngrams from words in Brown Corpus

def ngramsForBrown(text):
    words_Brown = []
    i = 1
    for k in text:
        x = k[0]
        words_Brown.append(x) 
        i += 1

    ngrams_Brown = countNgrams(words_Brown,0,0)
    return(ngrams_Brown)


# In[6]:

# split into 3 corpora and calculate Ngrams

full = taggedWords
half = taggedWords[0:int(len(full)/2)]
quarter = taggedWords[0:int(len(full)/4)]
print (len(full), len(half), len(quarter))

fullNgram = ngramsForBrown(full)
halfNgram = ngramsForBrown(half)
quarterNgram = ngramsForBrown(quarter)


# In[63]:

# applying the entropy calculating function to 3 corpora

print("\n********************\nNo smoothing\n")

H_uni_full, H_bi_full, H_tri_full = getH(fullNgram)

H_uni_half, H_bi_half, H_tri_half = getH(halfNgram)

H_uni_quarter, H_bi_quarter, H_tri_quarter = getH(quarterNgram)

print("H 100% (Brown) = ", H_tri_full)
p_full = math.pow(2.0, H_tri_full)
print("Perplexity 100% (Brown) = ", p_full)

print("\nH 50% (Brown) = ", H_tri_half)
p_half = math.pow(2.0, H_tri_half)
print("Perplexity 50% (Brown) = ", p_half)

print("\nH 25% (Brown) = ", H_tri_quarter)
p_quarter = math.pow(2.0, H_tri_quarter)
print("Perplexity 25% (Brown) = ", p_quarter)


# In[9]:

# getting a dictionary of tags

keys = []
val = []
i = 0
for n in taggedWords:
    keys.append(n[0])
    val.append(n[1])
dictTagged = dict(zip(keys, val))


# In[24]:

# getting frequencies for bigrams and trigrams with smoothing 1 (x')

def dict_bi_tri_xprime(corpus):
    dict_bi_xprime = {}
    for k in corpus[1].keys():
        x = k[0]
        y = k[1]
        for k1 in dictTagged.keys():
            if (x==k1):
                key = (dictTagged[k1], y)
                if key not in dict_bi_xprime.keys():
                    dict_bi_xprime[key] = corpus[1][k]
                else:
                    dict_bi_xprime[key] += corpus[1][k]

    dict_tri_xprime = {}
    for k in corpus[2].keys():
        x = k[0]
        y = k[1]
        z = k[2]
        for k1 in dictTagged.keys():
            if (x==k1):
                key = (dictTagged[k1], y, z)
                if key not in dict_tri_xprime.keys():
                    dict_tri_xprime[key] = corpus[2][k]
                else:
                    dict_tri_xprime[key] += corpus[2][k]
                
    return(dict_bi_xprime, dict_tri_xprime)


# getting frequencies for bigrams and trigrams with smoothing 2 (x', y')

def dict_bi_tri_x_y_prime(corpus):
    dict_bi_x_y_prime = {}
    if (corpus == "full"):
        dict_bi = dict_bi_xprime_full
        dict_tri = dict_tri_xprime_full
    elif (corpus == "half"):
        dict_bi = dict_bi_xprime_half
        dict_tri = dict_tri_xprime_half
    else:
        dict_bi = dict_bi_xprime_quarter
        dict_tri = dict_tri_xprime_quarter

    for k in dict_bi.keys():
        x = k[0]
        y = k[1]
        for k1 in dictTagged.keys():
            if (y==k1):
                key = (x, dictTagged[k1])
                if key not in dict_bi_x_y_prime.keys():
                    dict_bi_x_y_prime[key] = dict_bi[k]
                else:
                    dict_bi_x_y_prime[key] += dict_bi[k]
                    
    dict_tri_x_y_prime = {}
    for k in dict_tri.keys():
        x = k[0]
        y = k[1]
        z = k[2]
        for k1 in dictTagged.keys():
            if (y==k1):
                key = (x, dictTagged[k1], z)
                if key not in dict_tri_x_y_prime.keys():
                    dict_tri_x_y_prime[key] = dict_tri[k]
                else:
                    dict_tri_x_y_prime[key] += dict_tri[k]
                
    return(dict_bi_x_y_prime, dict_tri_x_y_prime)


# In[25]:

# getting frequencies for bigrams and trigrams with smoothing 1 (x') for 3 corpora

dict_bi_xprime_full, dict_tri_xprime_full = dict_bi_tri_xprime(fullNgram)
dict_bi_xprime_half, dict_tri_xprime_half = dict_bi_tri_xprime(halfNgram)
dict_bi_xprime_quarter, dict_tri_xprime_quarter = dict_bi_tri_xprime(quarterNgram)


# In[54]:

# getting ngram lists for smoothing 1 (x') for all corpora: corpus[0] is unigram frequencies,
# corpus[1] is bigram frequencies, corpus[2] is trigram frequencies

full_corpus = (FreqDist(list(getTagsFromTaggedWords(full))), dict_bi_xprime_full, dict_tri_xprime_full)
half_corpus = (FreqDist(list(getTagsFromTaggedWords(half))), dict_bi_xprime_half, dict_tri_xprime_half)
quarter_corpus = (FreqDist(list(getTagsFromTaggedWords(quarter))), dict_bi_xprime_quarter, dict_tri_xprime_quarter)


# In[64]:

# applying the entropy calculating function to 3 corpora

print("\n********************\nSmoothing x_prime\n")

H_uni_full, H_bi_full, H_tri_full = getH(full_corpus)

H_uni_half, H_bi_half, H_tri_half = getH(half_corpus)

H_uni_quarter, H_bi_quarter, H_tri_quarter = getH(quarter_corpus)

print("H 100% (Brown) = ", H_tri_full)
p_full = math.pow(2.0, H_tri_full)
print("Perplexity 100% (Brown) = ", p_full)

print("\nH 50% (Brown) = ", H_tri_half)
p_half = math.pow(2.0, H_tri_half)
print("Perplexity 50% (Brown) = ", p_half)

print("\nH 25% (Brown) = ", H_tri_quarter)
p_quarter = math.pow(2.0, H_tri_quarter)
print("Perplexity 25% (Brown) = ", p_quarter)


# In[42]:

# getting frequencies for bigrams and trigrams with smoothing 2 (x', y') for 3 corpora

dict_bi_x_y_prime_full, dict_tri_x_y_prime_full = dict_bi_tri_x_y_prime(fullNgram)
dict_bi_x_y_prime_half, dict_tri_x_y_prime_half = dict_bi_tri_x_y_prime(halfNgram)
dict_bi_x_y_prime_quarter, dict_tri_x_y_prime_quarter = dict_bi_tri_x_y_prime(quarterNgram)


# In[56]:

# getting ngram lists for smoothing 2 (x', y') for all corpora: corpus[0] is unigram frequencies,
# corpus[1] is bigram frequencies, corpus[2] is trigram frequencies

full_corpus = (FreqDist(list(getTagsFromTaggedWords(full))), dict_bi_x_y_prime_full, dict_tri_x_y_prime_full)
half_corpus = (FreqDist(list(getTagsFromTaggedWords(half))), dict_bi_x_y_prime_half, dict_tri_x_y_prime_half)
quarter_corpus = (FreqDist(list(getTagsFromTaggedWords(quarter))), dict_bi_x_y_prime_quarter, dict_tri_x_y_prime_quarter)


# In[65]:

# applying the entropy calculating function to 3 corpora

print("\n********************\nSmoothing x_prime, y_prime\n")

H_uni_full, H_bi_full, H_tri_full = getH(full_corpus)

H_uni_half, H_bi_half, H_tri_half = getH(half_corpus)

H_uni_quarter, H_bi_quarter, H_tri_quarter = getH(quarter_corpus)

print("H 100% (Brown) = ", H_tri_full)
p_full = math.pow(2.0, H_tri_full)
print("Perplexity 100% (Brown) = ", p_full)

print("\nH 50% (Brown) = ", H_tri_half)
p_half = math.pow(2.0, H_tri_half)
print("Perplexity 50% (Brown) = ", p_half)

print("\nH 25% (Brown) = ", H_tri_quarter)
p_quarter = math.pow(2.0, H_tri_quarter)
print("Perplexity 25% (Brown) = ", p_quarter)

print("\n\n--- %s seconds ---" % (time.time() - start_time))