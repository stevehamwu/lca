#!/usr/bin/env python 3.5
# -*- coding:utf-8 -*- 
import jieba as jb
import jieba.analyse
import math
class QA(object):
	def __init__(self, id, query, candidates, answer):
		self.id = id
		self.query = query
		self.candidates = candidates
		self.answer = answer
		self.qwords = self.getQWords()
		self.cwords = self.getCWords()
		self.nw = self.getNW()
		self.nc = self.getNC()
		self.N = len(self.candidates)

	def getQWords(self):
		#return jb.lcut(self.query)
		return jieba.analyse.extract_tags(self.query, 5)

	def getCWords(self):
		cwords = []
		for candidate in self.candidates:
			cwords.append(jieba.analyse.extract_tags(candidate, 15))
		return cwords

	def getNW(self):
		nw = {}
		for qword in self.qwords:
			nw[qword] = self.countWF(qword)
		return nw

	def getNC(self):
		nc = {}
		for cword in self.cwords:
			for cw in cword:
				nc[cw] = self.countWF(cw)
		return nc

	def getNCW(self, concept, word):
		count = 0
		for cword in self.cwords:
			if (word in cword) and (concept in cword):
				count = count + 1
		return count

	def countWF(self, word):
		count = 0
		for cword in self.cwords:
			if word in cword:
				count = count + 1
		return count

	def idf(self, word):
		if self.nw[word] == 0:
			return 1
		growth = math.log(self.N/self.nw[word])/5
		if growth < 1:
			return growth
		return 1

	def En(self, concept, word):
		return self.nw[word]*self.nc[concept]/self.N

	def co_degree(self, concept, word):
		co_occur = (self.getNCW(word, concept)-self.En(concept, word)-1)/self.nc[concept]
		if co_occur > 0:
			return co_occur
		return 0

	def getF(self, concept):
		f = 1
		for word in self.qwords:
			f = f * math.pow((0.01 + self.co_degree(concept, word)), self.idf(word))
		return f

	def getFCQ(self):
		fcq = {}
		for concept in self.nc:
			if concept not in self.nw:
				fcq[concept] = self.getF(concept)
		return fcq

	def print(self):
		print('id: ',self.id)
		print('query: ', self.query)
		print('candidates: ', self.candidates)
		print('answer: ', self.answer)

def read():
	with open('ir.txt', 'r') as f:
		text = f.read()
		docs = text.split('==================================================\n')
		qalist = []
		for doc in docs:
			query, candidates, answer = doc.split('@@@@@@@@@@\n')
			id, query = query.split('\n', 1)
			candidates = list(candidates.split('\n'))
			qalist.append(QA(id, query, candidates, answer.strip()))
		return qalist

def __main__():
	qalist = read()
	count = 0
	for qa in qalist:
		fcq = qa.getFCQ()
		max_fcq = max(fcq.items(), key=lambda x: x[1])
		print('answer:', qa.answer, ' max_lca: ', max_fcq, qa.answer == max_fcq[0])
		if qa.answer == max_fcq[0]:
			count = count + 1

	print('Accuracy: ', count/len(qalist))
	# for qa in qalist:
	# 	cwords = qa.getCWords()
	# 	print(len(cwords))
		# ws = jb.cut_for_search(qa.query)
		# for w in ws:
		# 	print(w)

__main__()