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
		return(jieba.analyse.extract_tags(self.query, 5))

	def getCWords(self):
		cwords = []
		for candidate in self.candidates:
			cwords.append(jieba.analyse.extract_tags(candidate, 20))
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
		for sentence in self.cwords:
			wflag = False
			cflag = False
			for cword in sentence:
				if cword.__contains__(word):
					wflag = True
				if cword.__contains__(concept):
					cflag = True
				if wflag and cflag:
					count = count + 1
					break
		return count

	def countWF(self, word):
		count = 0
		for sentence in self.cwords:
			for cword in sentence:
				if cword.__contains__(word):
					count = count + 1
					break
		return count

	def idf(self, word):
		if self.nw[word] == 0:
			return 1
		growth = math.log(self.N/self.nw[word], 10)/5
		return min(1, growth)

	def En(self, concept, word):
		return self.nw[word]*self.nc[concept]/self.N

	def co_degree(self, concept, word):
		co_occur = (abs(self.getNCW(word, concept) - self.En(concept, word)) - 1)/self.nc[concept]
		return max(co_occur, 0)

	def getF(self, concept):
		f = 1
		for word in self.qwords:
			f = f * math.pow(0.01 + self.co_degree(concept, word), self.idf(word))
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
			candidates = list(candidates.split('\n', candidates.count('\n')-1))
			qalist.append(QA(id, query, candidates, answer))
		return qalist

def main(topK=1, matchmode='precise'):
	qalist = read()
	count = 0
	for qa in qalist:
		print(qa.N)
		fcq = qa.getFCQ()
		max_fcq = sorted(fcq.items(), key=lambda x:x[1], reverse=True)[0:topK]
		correct = False
		for mf in max_fcq:
			if matchmode == 'precise':
				if qa.answer.strip() == mf[0].strip():
					correct = True
					count = count + 1
					break
			elif matchmode == 'approximate':
				if qa.answer.strip().__contains__(mf[0].strip()) or mf[0].strip().__contains__(qa.answer.strip()):
					correct = True
					count = count + 1
					break
		print('answer:', qa.answer,'top ', topK, 'max_lca: ', max_fcq, correct)

	print('Accuracy: ', count/len(qalist))

main(5, 'precise')