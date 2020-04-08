#-*- coding:utf-8 -*-
import numpy as np
import random

def getLength(train, test):
	maxLength = 0
	tempLength = 0
	f1 = open(train,'r')
	if test != None:
		f2 = open(test,'r')
		lines = f1.readlines() + f2.readlines()
	else:
		lines = f1.readlines()
	for line in lines:
		if line in ['\n','\r\n']:
			if tempLength > maxLength:
				maxLength = tempLength
			tempLength = 0
		else:
			tempLength += 1
	return maxLength

def loadDic(embedding):
	dic = {}
	for line in open(embedding):
		if len(line.split(' ')) < 3:
			continue
		line = line.strip()
		word = line.split(' ')[0]
		tempvec = []
		for token in line.split(' ')[1:]:
			tempvec.append(float(token))
		dic[word] = tempvec
	return dic, len(tempvec)

def getWordEmbedding(token, wsd):
	lemma = ''
	if wsd:
		if token[4] == '00':
			lemma = token[0]+'/'+token[1]
		else:
			if token[0][0] == '<' :
				lemma = token[0]+'/'+token[1]	
			else:
				lemma = token[0]+'__'+token[4]+'/'+token[1]
	else:
#		try:
		lemma = token[0]+'/'+token[2]
#		except:
#			print token[0]
	return lemma

def getTagVec(tag, tags):
	oneHot = [0.0 for _ in range(len(tags))]
	for i, t in enumerate(tags):
		if tag == t:
			oneHot[i] = 1
			return oneHot
	oneHot[len(tags)-1] = 1
	return oneHot

def makeData(data, maxLength, dic, wordDim):
	word = []
	tag = []
	sentence = []
	sentenceTag = []
	posTags = ['NNG','NNP','NNB','NP','NR','VV','VA','VX','VCP','VCN','MM','MAG','MAJ','IC',
	'JKS','JKC','JKG','JKO','JKB','JKV','JKQ','JX','JC','EP','EF','EC','ETN','ETM','XPN','XSN',
	'XSV','XSA','XR','SF','SP','SS','SE','SO','SL','SH','SW','NF','NV','SN','NA','-'] 
	nerTags = ['LC','OG','AF','DT','TI','CV','AM','PT','QT','FD','TR','EV','MT','TM','-']
	sentiTags = ['0', '1', '2', '3']
	sentenceLength = 0
	temp_tag = [0.0 for _ in range(len(sentiTags))]
	temp_tag[len(temp_tag)-1] = 1.0
	linenum=0
	for line in open(data):
		linenum+=1
		if line in ['\n','\r\n']:
			temp = np.array([0.0 for _ in range(len(word[0]))]) #zero padding
			for _ in range(maxLength - sentenceLength):
				tag.append(np.array(temp_tag))      
				word.append(temp)
			sentence.append(word)
			sentenceTag.append(np.array(tag))
			sentenceLength = 0
			word = []
			tag = []
		else:
			line = line.strip()
			token = line.split('\t')
			sentenceLength += 1
#			print linenum
			lemma = getWordEmbedding(token, False)
			if dic.get(lemma) != None:
				embedding = dic[lemma]
			else:
				
				if dic.get('<unk>/'+token[2]):
					embedding = dic['<unk>/'+token[2]]
				else:
					dic['<unk>/'+token[2]] = [ 2*random.random()-1 for _ in range(wordDim)]
					embedding = dic['<unk>/'+token[2]]


			pos = getTagVec(token[2], posTags)
			
			ner = getTagVec(token[3][:2], nerTags)
#			try:
#			cate = getTagVec(token[5], cateTags)
#			except:
#				print token[0]
			temp = embedding + pos 
			temp = np.array(temp)
			word.append(temp)

			#output
			outputLayer = getTagVec(token[4], sentiTags)
			outputLayer = np.array(outputLayer)
			tag.append(outputLayer)

	return sentence, sentenceTag

def loadData(train, test, embedding):
	embeddingDic, wordDim = loadDic(embedding)
	maxLength = getLength(train, test)
	trainInput, trainOutput = makeData(train, maxLength, embeddingDic, wordDim)
	if test != None:
		testInput, testOutput = makeData(test, maxLength, embeddingDic, wordDim)
		return trainInput, trainOutput, testInput, testOutput, maxLength
	else:
		return trainInput, trainOutput, maxLength
