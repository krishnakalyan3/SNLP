#!/usr/bin/env python2
import auxiliar as ax
import math

path_en = '/Users/krishna/MIRI/SNLP/Homework/data/en.txt'
path_tagged_en = '/Users/krishna/MIRI/SNLP/Homework/data/tagged_brown_en.txt'
enWords = ax.getWordsFromFile(path_en)
tagged_en = ax.getTaggedWordsFromFile(path_tagged_en)

def filter_data(data,n_gram):
	return data[n_gram - 1]

def freq(n_gram_dict):
	n_gram_sum = 0
	for word, word_freq in n_gram_dict.iteritems():
		n_gram_sum += word_freq
	return n_gram_sum

# P(x)
def prob_x(uni_gram_dict, freq_x):
	dict_prob_x = {}
	for word, word_freq in uni_gram_dict.iteritems():
		dict_prob_x[word] = 1.0 * (word_freq) / freq_x
	return dict_prob_x

def uni_entropy(uni_gram_prob_dict):
	H = 0
	for word, word_prob in uni_gram_prob_dict.iteritems():
		H += word_prob * math.log(word_prob, 2)
	return -1 * H

# P(y|x)
def prob_yx(bi_gram_dict, uni_gram_dict):
	dict_prob_yx = {}
	for bi_word, bi_word_freq in bi_gram_dict.iteritems():
		dict_prob_yx[bi_word] = 1.0 * bi_word_freq / uni_gram_dict[bi_word[0]]
	return dict_prob_yx

def bi_entropy(bi_gram_prob_dict, uni_gram_prob_dict):
	H = 0
	for word, word_prob in bi_gram_prob_dict.iteritems():
		H += uni_gram_prob_dict[word[0]] * word_prob * math.log(word_prob, 2)
	return -1 * H

# P(z|xy)
def prob_zxy(tri_gram_dict, bi_gram_dict):
	dict_prob_zxy ={}
	for (x,y,z) , tri_word_freq in tri_gram_dict.iteritems():
		dict_prob_zxy[x,y,z] = 1.0 * tri_word_freq / bi_gram_dict[x,y]
	return dict_prob_zxy

def tri_entropy(tri_gram_prob_dict, bi_gram_prob_dict, uni_gram_prob_dict):
	H = 0
	for (x,y,z), word_prob in tri_gram_prob_dict.iteritems():
		H += uni_gram_prob_dict[x] * bi_gram_prob_dict[x,y] * word_prob * math.log(word_prob, 2)
	return -1 * H

def get_brown_tri(tagged_data):
	words_without_tag = []
	#for i in range(0,len(tagged_data), 3):
	#	words_without_tag.append([tagged_data[i][0], tagged_data[i+1][0], tagged_data[i+2][0]])
	for word,tag in tagged_data:
		words_without_tag.append(word)
	return words_without_tag

# Get Data
n_grams_en = ax.countNgrams(enWords, 0)
uni_gram_dict = filter_data(n_grams_en, 1)

freq_uni = freq(uni_gram_dict)
uni_prob = prob_x(uni_gram_dict, freq_uni)
H_uni = uni_entropy(uni_prob)


bi_gram_dict = filter_data(n_grams_en, 2)
bi_prob = prob_yx(bi_gram_dict, uni_gram_dict)
H_bi =  bi_entropy(bi_prob, uni_prob)

tri_gram_dict = filter_data(n_grams_en, 3)
tri_prob = prob_zxy(tri_gram_dict, bi_gram_dict)
H_tri = tri_entropy(tri_prob, bi_prob, uni_prob)

print "***"
print "Entopy unigram ", H_uni
print "Entopy bigram ", H_bi
print "Entopy trigram ", H_tri
print "***"

# Split tagged data
full_tagged_data = tagged_en
half_tagged_data = tagged_en[0:len(full_tagged_data)/2]
quarter_tagged_data = tagged_en[0:len(full_tagged_data)/4]

print "Data Split Sizes ", len(full_tagged_data), len(half_tagged_data), len(quarter_tagged_data)

# Brown Corpus
n_grams_en_b =  get_brown_tri(full_tagged_data)
n_grams_en_b = ax.countNgrams(n_grams_en_b, 0)
uni_gram_dict_b = filter_data(n_grams_en_b, 1)
uni_prob_b = prob_x(uni_gram_dict_b, freq_uni)
bi_gram_dict_b = filter_data(n_grams_en_b, 2)
bi_prob_b = prob_yx(bi_gram_dict_b, uni_gram_dict_b)
tri_gram_dict_b = filter_data(n_grams_en_b, 3)
tri_prob_b = prob_zxy(tri_gram_dict_b, bi_gram_dict_b)
H_tri = tri_entropy(tri_prob_b, bi_prob_b, uni_prob_b)
print 2 ** H_tri





