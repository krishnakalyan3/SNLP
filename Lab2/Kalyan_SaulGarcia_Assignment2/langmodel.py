#!/usr/bin/env python2
import auxiliar as ax
import math

def perplexity(entropy):
	return 2 ** entropy

def freq_count(corpus_dict):
	n_gram_sum = 0
	for word, word_freq in corpus_dict.iteritems():
		n_gram_sum += word_freq
	return n_gram_sum

# P(x)
def prob_x(uni_gram_list, freq_x):
	dict_prob_x = {}
	for word, word_freq in uni_gram_list.iteritems():
		dict_prob_x[word] = 1.0 * (word_freq) / freq_x
	return dict_prob_x

def uni_entropy(uni_gram_prob_dict):
	H = 0
	for word, word_prob in uni_gram_prob_dict.iteritems():
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

def entropy(word_list, flag = 0):
	if flag == 0:
		U,B,T = ax.countNgrams(word_list, 0)
	else:
		U,B,T = word_list

	freq_uni = freq_count(U)
	uni_prob = prob_x(U, freq_uni)
	h_uni_gram = uni_entropy(uni_prob)
	
	bi_prob = prob_yx(B, U)
	h_bi_gram =  bi_entropy(bi_prob, uni_prob)

	tri_prob = prob_zxy(T, B)
	h_tri_gram = tri_entropy(tri_prob, bi_prob, uni_prob)

	return (h_uni_gram, h_bi_gram, h_tri_gram)

def smooth(tagged_list, prime = 0):
	brown_words = remove_tags(tagged_list)

	if prime == 0:
		return brown_words

	if prime == 1:
		x_prime = remove_words(tagged_list)
		U,B,T = ax.countNgrams(x_prime, 0)
		word_tag_dict = word_tag(tagged_list)

		Uy,By,Ty = ax.countNgrams(brown_words, 0)
		bigram_dict = prime_bigram(By, word_tag_dict)

		trigram_dict = prime_trigram(Ty, word_tag_dict)

		full_data =  [U,bigram_dict,trigram_dict]
		return entropy(full_data, 1)
	
	x_prime = remove_words(tagged_list)
	word_tag_dict = word_tag(tagged_list)
	U,B,T = ax.countNgrams(x_prime, 0)
	Uy,By,Ty = ax.countNgrams(brown_words, 0)
	xy_bigram_dict = xy_prime_bigram(By, word_tag_dict)
	xy_trigram_dict = xy_prime_trigram(Ty, word_tag_dict)
	full_data =  [U,xy_bigram_dict,xy_trigram_dict]
	return entropy(full_data, 1)



def remove_words(tagged_list):
	tags = []
	for words,tag in tagged_list:
		tags.append(tag)
	return tags

def remove_tags(tagged_list):
	words = []
	for word,tags in tagged_list:
		words.append(word)
	return words

# ['adv', 'noun', 'adp', 'pron', 'det', 'num', '.', 'prt', 'verb', 'x', 'conj', 'adj']
def word_tag(tagged_list):
	word_tag_dict = {}
	for word,tag in tagged_list:
		word_tag_dict[word] = tag
	return word_tag_dict

def prime_bigram(bigram_list, word_tag_dict):
	x_prime_bi = {}
	for word,count in bigram_list.iteritems():
		bi_key = (word_tag_dict[word[0]],word[1])
		if bi_key not in x_prime_bi:
			x_prime_bi[bi_key] = count
		else:
			x_prime_bi[bi_key] += count
	return x_prime_bi

def prime_trigram(trigram_list, word_tag_dict):
	x_prime_tri = {}
	for word,count in trigram_list.iteritems():
		tri_key = (word_tag_dict[word[0]],word[1],word[2])
		if tri_key not in x_prime_tri:
			x_prime_tri[tri_key] = count
		else:
			x_prime_tri[tri_key] += count
	return x_prime_tri

def xy_prime_bigram(bigram_list, word_tag_dict):
	xy_prime_bi = {}
	for word,count in bigram_list.iteritems():
		bi_key = (word_tag_dict[word[0]],word_tag_dict[word[1]])
		if bi_key not in xy_prime_bi:
			xy_prime_bi[bi_key] = count
		else:
			xy_prime_bi[bi_key] += count
	return xy_prime_bi

def xy_prime_trigram(trigram_list, word_tag_dict):
	xy_prime_tri = {}
	for word,count in trigram_list.iteritems():
		tri_key = (word_tag_dict[word[0]],word_tag_dict[word[1]],word[2])
		if tri_key not in xy_prime_tri:
			xy_prime_tri[tri_key] = count
		else:
			xy_prime_tri[tri_key] += count
	return xy_prime_tri




