#!/usr/bin/env python2
import langmodel as lm
import auxiliar as ax

def get_brown_words(tagged_data):
	words_without_tag = []
	for word,tag in tagged_data:
		words_without_tag.append(word)
	return words_without_tag

def get_brown_tags(tagged_data):
	tags = []
	#for word,tag in tagged_data[0]:
	#	tags.append(tag)
	#return tags

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


if __name__ == '__main__':
	path_tagged_en = '/Users/krishna/MIRI/SNLP/Homework/data/tagged_brown_en.txt'
	tagged_en = ax.getTaggedWordsFromFile(path_tagged_en)

	path_en = '/Users/krishna/MIRI/SNLP/Homework/data/en.txt'
	enWords = ax.getWordsFromFile(path_en)
	
	H1,H2,H3 = lm.entropy(enWords)
	print H1,H2,H3

	full_tagged_data = tagged_en
	half_tagged_data = tagged_en[0:len(full_tagged_data)/2]
	quarter_tagged_data = tagged_en[0:len(full_tagged_data)/4]

	print "Data Split Sizes ", len(full_tagged_data), len(half_tagged_data), len(quarter_tagged_data)

	# Brown Corpus Perplexities x,y,z
	# FULL
	H1bf,H2bf,H3bf = lm.entropy(full_tagged_data)
	print 'Entropy Full ', H3bf
	print 'perplexity Full ',lm.perplexity(H3bf)

	# Half
	H1bh,H2bh,H3bh = lm.entropy(half_tagged_data)
	print 'Entropy Half ', H3bh
	print 'perplexity Half ',lm.perplexity(H3bh)

	# Quarter
	H1bq,H2bq,H3bq = lm.entropy(quarter_tagged_data)
	print 'Entropy Quarter ', H3bq
	print 'perplexity Quarter ',lm.perplexity(H3bq)

	#Brown Corpus Perplexities x',y,z
	# compute x', y, z
	# tagged brown corpus
	# run brown corpus through countNgrams
	# This is for tag [0]th
	# filter for tags -> noun, vb   
	# Unigrams
	# dict -> noun : count
	#		  verb : count

	# This is for word [1] st
	# bgram -> noun, word : count
	#		   verb, word : count 


	# uni,bi,tri

	#dict_bi_xprime_full, dict_tri_xprime_full = dict_bi_tri_xprime(n_grams_en_b_f)
	#full_corpus = (FreqDist(list(getTagsFromTaggedWords(full))), dict_bi_xprime_full, dict_tri_xprime_full)
	#n_grams_b_fx = get_brown_tags(full_tagged_data)
	#print n_grams_b_fx
	
	#H1bfx,H2bfx,H3bfx = lm.smooth(n_grams_en_b_f, n_grams_b_fx)
	#print H3bfx


