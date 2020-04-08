#-*- coding:utf-8 -*-
import json
from collections import OrderedDict

def result_jason(a, ss):
	
	con_tag=['NNG','NNP','NNB','NP','NR','VA','VV','VX','MAG','VCP','VCN','XR']
	josa_tag=['MM','MAJ','IC','JKS','JKC','JKG','JKO','JKB','JKV','JKQ','JX','JC','EP','EF','EC','ETN','ETM','XPN','XSN','XSV','XSA']

	#f=open(a,'r')
	lines=a.readlines()
	save=open('./input_save/' + str(ss)+'.txt','w')
	for line in lines:
		save.write(line)
	
	sentence_count=0
	entity_dic={}
	dic_con={}
	line_score=0
	total_linescore=0
	keyword=[0,0,0,0,0]
	line_count=0
	neg_sen=0
	pos_sen=0
	not_sen=0
	neg_word=0
	pos_word=0
	not_word=0
	entity_text=''
	senti_text=''
	entity_flag=0
	josa_flag=0
	
	for line in lines:
		line_count+=1
		line=line.strip()
		line=line.split('\t')
		if len(line)<2:
			continue	
		if line[0].find('<SOS>') != -1:
			sentence_count+=1
			line_score=0
			entity_flag=0
			josa_flag=0
			entity_text=''
			senti_text=''
			continue
		elif line[0].find('<EOS>') != -1:
			if line_score>0:
				pos_sen+=1
			elif line_score<0:
				neg_sen+=1
			else:
				not_sen+=1
			total_linescore+=line_score
			
			if entity_text != '':
				if senti_text != '':
					if entity_dic.get(entity_text) ==None:
						entity_dic[entity_text]=[]
						entity_dic[entity_text].append(senti_text)
					else:
						entity_dic[entity_text].append(senti_text)
			continue
		elif line[0].find('<BLN>') != -1:
			continue
		else:
			for i in range(len(con_tag)):
				if line[2].find(con_tag[i]) != -1:
					if dic_con.get(line[0]) == None:
						dic_con[line[0]]=1
					else:
						dic_con[line[0]]+=1
					if line[5] == '1':
						entity_flag=0
						pos_word+=1
						line_score+=1
						if entity_text != '':
							if senti_text == '':
								senti_text=line[0]
							else :
								senti_text= senti_text+' '+line[0]
					elif line[5] =='2':
						
						entity_flag=0
						neg_word+=1
						line_score-=1
						if entity_text != '':
							
							if senti_text == '':
								senti_text=str(line[0])
							else :
								senti_text= senti_text+' '+str(line[0])

					elif line[5] =='3':
						entity_flag=0
						not_word+=1
						if entity_text != '':
							if senti_text != '':
								senti_text=senti_text+' '+line[0]
							else :
								senti_text= senti_text+' '+str(line[0])
#								if entity_dic.get(entity_text) ==None:
#									entity_dic[entity_text]=[]
#									entity_dic[entity_text].append(senti_text)
#								else:
#									entity_dic[entity_text].append(senti_text)
					elif line[5] =='0':			#개체 나왔을때
						if entity_text == '':	#새개체면
							entity_text=line[0]
							senti_text=''
							entity_flag=1
						else:					#헌개체면
							if senti_text !='':	#sen 있으면
								if entity_dic.get(entity_text) ==None:
									entity_dic[entity_text]=[]
									entity_dic[entity_text].append(senti_text)
								else:
									entity_dic[entity_text].append(senti_text)
									
								entity_text=line[0]
								senti_text=''
								entity_flag=1
								
							else:				#sen 없으면
								if entity_flag ==1:
									entity_text=entity_text+' '+line[0]
								else:
									entity_text=line[0]
									entity_flag=1
					break
			for tag in josa_tag:
				if line[2] in tag:
					entity_flag=0
					if entity_text != '':
							if senti_text != '':
								senti_text= senti_text+str(line[0])
			
	for key in dic_con.keys():
		for i in range(len(keyword)-1):
			if keyword[i]==0:
				keyword[i]=key
				continue
			elif dic_con[keyword[i]]< dic_con[key]:
				for j in range(3, i-1,-1):
					keyword[j+1]=keyword[j]	
				keyword[i]= key
				break
			else:
				continue
	
	dic_top={}
	flag=0
	top=[0,0,0,0,0]
	for num in range(len(keyword)):
		dic_top={}
		for line in lines:
			line=line.strip()
			line=line.split('\t')
			if flag==1:
				if dic_top.get(line[0])==None:
					dic_top[line[0]]=1
				else:
					dic_top[line[0]]+=1
				flag=0
				continue	
			if line[0]==keyword[num]:
				flag=1	
				continue
		for	key in dic_top.keys():
			if top[num]==0:
				top[num]=key
			else:
				if dic_top[top[num]]<dic_top[key]:
					top[num]=key

	print('sen_count: %s'%sentence_count)
	print('total line score: %s'%total_linescore)
	print('pos_sen: %s'%pos_sen)
	print('not_sen: %s'%not_sen)
	print('neg_sen: %s'%neg_sen)
	print('pos_word: %s'%pos_word)
	print('not_word: %s'%not_word)
	print('neg_word: %s'%neg_word)
	
	group_data = OrderedDict()

	group_data["sen_count"]= sentence_count
	group_data["pos_sen"]= pos_sen
	group_data["neg_sen"] = neg_sen
	group_data["not_sen"] = not_sen
	group_data["pos_word"] = pos_word
	group_data["neg_word"] = neg_word
	group_data["not_word"] = not_word
	
		
	for key in entity_dic.keys():
		group_data[key]=[]
		value=[]
		for i in range(len(entity_dic[key])):
			value.append(entity_dic[key][i])
		group_data[key]= value
	
	group_data["entity"] =entity_dic.keys()
	group_data["entity_context"] = entity_dic.values()
	
	#print(json.dumps(group_data,ensure_ascii=False, indent=4) )
	#group_data= group_data.decode('cp949').encode('utf-8')
	return json.dumps(group_data, ensure_ascii=True, indent=4)
	

#	with open('bbb.json', 'w') as make_file:
#		json.dump(group_data, make_file, ensure_ascii=False, indent=4)
