# An implementation of RAKE algorithm for Chinese test based on python 3.
# The algorithm is described in:
# Rose, S., D. Engel, N. Cramer, and W. Cowley (2010).
# Automatic keyword extraction from indi-vidual documents.
# In M. W. Berry and J. Kogan (Eds.), Text Mining: Applications and Theory.unknown: John Wiley and Sons, Ltd.

import re
import operator

# for Chinese word segmentation
import jieba

debug = False
test = True

def load_text(text_file_path):
	'''
	Utility function to load Chinese text from a file
	:param text_file_path: path of a file containing Chinese text
	:return: the Chinese text
	'''
	text = open(text_file_path, encoding = 'utf8').read()
	return text

def load_stop_words(stop_word_file_path):
	'''
	Utility function to load stop words from a file and return as a list of words
	:param stop_word_file_path: path of a file containing Chinese stop words
	:return: a list of Chinese stop words
	'''
	stop_words = []
	for stp_wd in open(stop_word_file_path, encoding = 'utf8'):
		stop_words.append(stp_wd.strip())
	return stop_words

def separate_words(text, min_word_return_size):
	'''
	Utility function to return a list of all words that are have a length greater than a specified number of characters
	:param text: the text that must be split in to words
	:param min_word_return_size: The minimum length of the Chinese word(s) must have to be included
	:return: a list of separate words
	'''
	words = []
	for wd in jieba.cut(text, cut_all = False):
		if len(wd) > min_word_return_size and wd != '':
			words.append(wd)
	return words

def split_sentences(text):
	'''
	Utility function to return a list of sentences.
	:param text: the text that must be split in to sentences
	:return: a list of sentences
	'''
	sentence_delimiters = re.compile(u'[.、。!！?？,，;；:：“”\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s ')
	sentences = sentence_delimiters.split(text)
	return sentences

def build_stop_word_regex(stop_word_file_path, min_length = 1, max_length = 3):
	stop_word_list = load_stop_words(stop_word_file_path)
	stop_word_regex_list = []
	for word_regex in stop_word_list:
		if len(word_regex) <= max_length and len(word_regex) >=  min_length:
			stop_word_regex_list.append(word_regex)
	stop_word_pattern = re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)
	return stop_word_pattern

def generate_candidate_keywords(sentence_list, stopword_pattern):
	phrase_list = []
	for s in sentence_list:
		tmp = re.sub(stopword_pattern, '|', s.strip())
		phrases = tmp.split("|")
		for phrase in phrases:
			if phrase != "":
				phrase_list.append(phrase)
	return phrase_list

def calculate_word_scores(phraseList):
	word_frequency = {}
	word_degree = {}
	for phrase in phraseList:
		word_list = separate_words(phrase, 0)
		word_list_length = len(word_list)
		word_list_degree = word_list_length - 1
		#if word_list_degree > 3: word_list_degree = 3 #exp.
		for word in word_list:
			word_frequency.setdefault(word, 0)
			word_frequency[word] += 1
			word_degree.setdefault(word, 0)
			word_degree[word] += word_list_degree  #orig.
			#word_degree[word] += 1/(word_list_length*1.0) #exp.
	for item in word_frequency:
		word_degree[item] = word_degree[item] + word_frequency[item]
		# Calculate Word scores = deg(w)/frew(w)
	word_score = {}
	for item in word_frequency:
		word_score.setdefault(item, 0)
		word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  #orig.
	#word_score[item] = word_frequency[item]/(word_degree[item] * 1.0) #exp.
	return word_score

def generate_candidate_keyword_scores(phrase_list, word_score):
	keyword_candidates = {}
	for phrase in phrase_list:
		keyword_candidates.setdefault(phrase, 0)
		word_list = separate_words(phrase, 0)
		candidate_score = 0
		for word in word_list:
			candidate_score += word_score[word]
		keyword_candidates[phrase] = candidate_score
	return keyword_candidates

class Rake(object):
	def __init__(self, stop_words_path):
		self.stop_words_path = stop_words_path
		self.__stop_words_pattern = build_stop_word_regex(stop_words_path)

	def run(self, text_file_path):

		test = load_text(text_file_path)

		sentence_list = split_sentences(text)

		phrase_list = generate_candidate_keywords(sentence_list, self.__stop_words_pattern)

		word_scores = calculate_word_scores(phrase_list)

		keyword_candidates = generate_candidate_keyword_scores(phrase_list, word_scores)

		sorted_keywords = sorted(keyword_candidates.items(), key = lambda x :x[1], reverse = True)
		return sorted_keywords


if test:
	text = load_text('Chinese_text.txt')
	# Split text into sentences
	sentenceList = split_sentences(text)
	stoppath = 'Chinese_stop_words.txt'
	stopwordpattern = build_stop_word_regex(stoppath)

	# generate candidate keywords
	phraseList = generate_candidate_keywords(sentenceList, stopwordpattern)

	# calculate individual word scores
	wordscores = calculate_word_scores(phraseList)

	# generate candidate keyword scores
	keywordcandidates = generate_candidate_keyword_scores(phraseList, wordscores)
	if debug: print (keywordcandidates)

	sortedKeywords = sorted(keywordcandidates.items(), key = lambda s: s[1], reverse = True)
	if debug:
		print (sortedKeywords)

	totalKeywords = len(sortedKeywords)
	if debug:
		print (totalKeywords)
		print (sortedKeywords[0:(totalKeywords // 3)])

	rake = Rake("Chinese_stop_words.txt")
	keywords = rake.run('Chinese_text.txt')
	print(keywords)