#!/usr/bin/env python2
import langmodel as lm
import auxiliar as ax

# 

if __name__ == '__main__':
	path_tagged_en = '/Users/krishna/MIRI/SNLP/Homework/data/tagged_brown_en.txt'
	tagged_en = ax.getTaggedWordsFromFile(path_tagged_en)

	path_en = '/Users/krishna/MIRI/SNLP/Homework/data/en.txt'
	enWords = ax.getWordsFromFile(path_en)
	
	print "####"
	H1,H2,H3 = lm.entropy(enWords)
	print 'Unigram Entropy ', H1
	print 'Bigram Entropy ', H2
	print 'Trigram Entropy ', H3

	full_tagged_data = tagged_en
	half_tagged_data = tagged_en[0:len(full_tagged_data)/2]
	quarter_tagged_data = tagged_en[0:len(full_tagged_data)/4]
	
	print "####"
	print "No Smoothing"
	# Smoothing Brown
	# <x, y, z>
	brown_words_full = lm.smooth(full_tagged_data)
	HB1,HB2,HB3 = lm.entropy(brown_words_full)
	print 'Entropy Full Brown',HB3
	print 'Perplexity Full Brown',lm.perplexity(HB3)

	brown_words_half = lm.smooth(half_tagged_data)
	HB1h,HB2h,HB3h = lm.entropy(brown_words_half)
	print 'Entropy Half Brown',HB3h
	print 'Perplexity Half Brown',lm.perplexity(HB3h)

	brown_words_quarter = lm.smooth(quarter_tagged_data)
	HB1q,HB2q,HB3q = lm.entropy(brown_words_quarter)
	print 'Entropy Quarter Brown',HB3q
	print 'Perplexity Quarter Brown',lm.perplexity(HB3q)
	

	print "####"
	# <x', y, z>
	print 'Brown Corpus X prime'
	HB1xp,HB2xp,HB3xp = lm.smooth(full_tagged_data, 1)
	print 'Entropy Full', HB3xp
	print 'Perplexity Full', lm.perplexity(HB3xp)

	HB1xph,HB2xph,HB3xph = lm.smooth(half_tagged_data, 1)
	print 'Entropy Half', HB3xph
	print 'Perplexity Half', lm.perplexity(HB3xph)

	HB1xpq,HB2xpq,HB3xpq = lm.smooth(quarter_tagged_data, 1)
	print 'Entropy Quarter', HB3xpq
	print 'Perplexity Quarter', lm.perplexity(HB3xpq)
	
	print "####"
	# <x', y', z>
	print "Brown Corpus X Y prime"
	HB1xyp,HB2xyp,HB3xyp = lm.smooth(full_tagged_data, 2)
	print 'Entropy Full', HB3xyp
	print 'Perplexity Full', lm.perplexity(HB3xyp)

	HB1xyph,HB2xyph,HB3xyph = lm.smooth(half_tagged_data, 2)
	print 'Entropy Half', HB3xyph
	print 'Perplexity Half', lm.perplexity(HB3xyph)

	HB1xypq,HB2xypq,HB3xypq = lm.smooth(quarter_tagged_data, 2)
	print 'Entropy Quarter', HB3xypq
	print 'Perplexity Quarter', lm.perplexity(HB3xypq)



