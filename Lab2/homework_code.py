#!/usr/bin/env python2
import auxiliar as ax
import math

enWords = ax.getWordsFromFile("../data/en.txt")

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

# Get Data
n_grams_en = ax.countNgrams(enWords, 0)


uni_gram_dict = filter_data(n_grams_en, 1)
freq_uni = freq(uni_gram_dict)
uni_prob = prob_x(uni_gram_dict, freq_uni)
print uni_entropy(uni_prob)


bi_gram_dict = filter_data(n_grams_en, 2)
bi_prob = prob_yx(bi_gram_dict, uni_gram_dict)
print bi_entropy(bi_prob, uni_prob)

tri_gram_dict = filter_data(n_grams_en, 3)
tri_prob = prob_zxy(tri_gram_dict, bi_gram_dict)
print tri_entropy(tri_prob, bi_prob, uni_prob)


