#!/usr/bin/env python2
import auxiliar as ax
import math

enWords = ax.getWordsFromFile("../data/en.txt")
#esWords = ax.getWordsFromFile("../data/es.txt")

def filter_data(data,n_gram):
	return data[n_gram - 1]

def prob(data, total_freq):
	prob_dict = {} 
	for word, count in data.iteritems():
		prob_dict[word] = float(count)/float(total_freq)
	return prob_dict

def total_freq(data):
	freq_count =  0
	for word, count in data.iteritems():
		freq_count = freq_count + count
	return freq_count

def unigram(uni_probs):
	H = 0
	sum_prob_uni = 0
	for word, prob in uni_probs.iteritems():
		sum_prob_uni = sum_prob_uni + prob
		H =  H +  prob * math.log(prob, 2)
	return (-1 * H, sum_prob_uni)

def bigram(bi_probs, sum_prob_uni):
	H = 0
	sum_prob_bi = 0
	for word, bi_prob in bi_probs.iteritems():
		sum_prob_bi = sum_prob_bi  + bi_prob
		H = H + bi_prob * math.log(bi_prob)
	H = H * sum_prob_uni
	return (H,sum_prob_bi)

def trigram(tri_probs, sum_prob_uni, sum_prob_bi):
	H = 0
	for word, tri_prob in tri_probs.iteritems():
		H = H  + tri_prob * math.log(tri_prob)
	H = H * sum_prob_uni * sum_prob_bi
	return H

n_grams_en = ax.countNgrams(enWords, 0)
unigram_data = filter_data(n_grams_en, 1)
total_terms = total_freq(unigram_data)
uni_gram_prob = prob(unigram_data, total_terms)
h_unigram = unigram(uni_gram_prob)
print h_unigram[0]