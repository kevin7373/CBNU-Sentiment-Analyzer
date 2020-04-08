#-*- coding:utf-8 -*-

import sys
import json


def normalization(word, word_tag):
	pos = ['SL','SH','SF','SP','SS','SE','SQ','SW','SN']
	replace = ['!','#','%','&',"'",'*','+',',','"']
	for i, tag in enumerate(pos):
		if word_tag == tag:
			return replace[i]
	return word.encode('utf-8')

def result_CoNLL(a,b):
	lm_file = open('./input_pre/'+str(a)+'.txt','r')
	save = open('./input_pre/'+str(b)+'.CoNLL','w')
#	lm = json.loads(str(lm_file.read()).encode("string-escape").replace('\\"','\"'))
	lm = json.loads(lm_file.read())
	temp_tag = '-'
	word_position = 0
	text=[]
	lm=lm["return_object"]
	flag=0
	for sentence in lm['sentence']:
		word_number =0
		lines=[]
		word_id= 0
		for morp in sentence['WSD']:
			if int(morp['id'])==0:
				position = int(morp['position'])
			elif word_position<int(morp['position']):
				temp =[]
				temp.append('<BLN>')#lemma 0
				temp.append('-')	#begin 1
				temp.append('-')	#pos 2
				temp.append('-')	#ner_tag 3
				temp.append('-')	# lable 4
				word_number +=1
				lines.append(temp)
			temp=[]
			lemma=morp['text'].encode('utf-8')
			word_position = int(morp['position']) + len(lemma)
			lemma = normalization(morp['text'], morp['type'])
			position = int(morp['position'])
			pos_tag = morp['type'].encode('utf-8')
			word_num = int(morp['id'])
			word_id = int(morp['begin'])

			temp.append(lemma)
			temp.append(word_num)
			temp.append(pos_tag)
			temp.append('-')
			temp.append(word_id)
			temp.append('-')
			temp.append('-')
			lines.append(temp)


		for NE in sentence['NE']:
			NE_type = NE['type'].encode('utf-8')
			#NE_type = checkNERtag(NE_type)
			begin = int(NE['begin'])
			end = int(NE['end'])
			for i in range(len(lines)):
				if lines[i][4] != '-':
					if end < lines[i][4]:
						break
					if begin <= lines[i][4] and lines[i][4] <= end:
						lines[i][3] = NE_type
		text.append(lines)
	for lines in text:
		if flag ==1:
			save.write('\r\n')
		save.write('<SOS>\t-\t-\t-\t3\r\n')
		for line in lines:
			lemma = str(line[0])
			word_id = str(line[4])
			pos = str(line[2])
			ner_tag = str(line[3])
			
			save.write(lemma+'\t'+word_id+'\t'+pos+'\t'+ner_tag+'\t3\r\n')	
		save.write('<EOS>\t-\t-\t-\t3')
		save.write('\r\n')
		flag=1
	save.write('\r\n')	
	return 
