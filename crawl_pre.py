#-*- coding:utf-8 -*-

import sys
import re

def crawl_pre(a,b):
	
	f=open('./input_pre/'+str(a)+'.txt','r')
	save=open('./input_pre/'+str(b)+'.txt','w')

	linenum=0

	lines=f.readlines()

	for line in lines:
		linenum+=1
		if linenum <3:
			continue
		line.strip()
		line=re.split('\?|\,|\.|\^|\!|\:|\;|\(|\)|\-',line)
		
#		line1=line.split('?')
		for li in line:
			li=li.strip()
			if len(li)>10 :
				if len(li)<300 :
					save.write('%s. \r\n'%(li))

	return save
