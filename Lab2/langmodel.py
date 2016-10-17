#!/usr/bin/env python2
import auxiliar as ax
import math

def perplexity(entropy):
	return 2 ** entropy

def freq_count(corpus_list):
	n_gram_sum = 0
	for word, word_freq in corpus_list.iteritems():
		n_gram_sum += word_freq
	return n_gram_sum

# P(x)
def prob_x(uni_gram_list, freq_x):
	dict_prob_x = {}
	for word, word_freq in uni_gram_list.iteritems():
		dict_prob_x[word] = 1.0 * (word_freq) / freq_x
	return dict_prob_x

def uni_entropy(uni_gram_prob_list):
	H = 0
	for word, word_prob in uni_gram_prob_list.iteritems():
		H += word_prob * math.log(word_prob, 2)
	return -1 * H

# P(y|x)
def prob_yx(bi_gram_list, uni_gram_list):
	dict_prob_yx = {}
	for bi_word, bi_word_freq in bi_gram_list.iteritems():
		dict_prob_yx[bi_word] = 1.0 * bi_word_freq / uni_gram_list[bi_word[0]]
	return dict_prob_yx

def bi_entropy(bi_gram_prob_list, uni_gram_prob_list):
	H = 0
	for word, word_prob in bi_gram_prob_list.iteritems():
		H += uni_gram_prob_list[word[0]] * word_prob * math.log(word_prob, 2)
	return -1 * H

# P(z|xy)
def prob_zxy(tri_gram_list, bi_gram_list):
	dict_prob_zxy ={}
	for (x,y,z) , tri_word_freq in tri_gram_list.iteritems():
		dict_prob_zxy[x,y,z] = 1.0 * tri_word_freq / bi_gram_list[x,y]
	return dict_prob_zxy

def tri_entropy(tri_gram_prob_list, bi_gram_prob_list, uni_gram_prob_list):
	H = 0
	for (x,y,z), word_prob in tri_gram_prob_list.iteritems():
		H += uni_gram_prob_list[x] * bi_gram_prob_list[x,y] * word_prob * math.log(word_prob, 2)
	return -1 * H

def entropy(word_list):
	n_grams_en = ax.countNgrams(word_list, 0)
	
	uni_gram_dict = n_grams_en[0]
	freq_uni = freq_count(uni_gram_dict)
	uni_prob = prob_x(uni_gram_dict, freq_uni)
	h_uni_gram = uni_entropy(uni_prob)

	bi_gram_dict = n_grams_en[1]
	bi_prob = prob_yx(bi_gram_dict, uni_gram_dict)
	h_bi_gram =  bi_entropy(bi_prob, uni_prob)

	tri_gram_dict = n_grams_en[2]
	tri_prob = prob_zxy(tri_gram_dict, bi_gram_dict)
	h_tri_gram = tri_entropy(tri_prob, bi_prob, uni_prob)

	return (h_uni_gram, h_bi_gram, h_tri_gram)

def smooth(corpus_list, tagged_word_list):
	n_grams_en = ax.countNgrams(tagged_word_list, 0)
	n_grams_en = n_grams_en[0]
	freq_uni = freq_count(tagged_word_list)
	uni_prob = prob_x(n_grams_en, freq_uni)
	h_uni_gram = uni_entropy(uni_prob)

	return h_uni_gram



