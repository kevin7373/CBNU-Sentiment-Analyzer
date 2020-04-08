#-*- coding:utf-8 -*-
#linux version

from bs4 import BeautifulSoup
import sys
import requests
import os
def crawl(a,b):
	save = open('./input_pre/' +str(b) +'.txt','w')
	flag=0
	for i in range(1,2):
#		if i ==1:
#			url ='https://search.shopping.naver.com/detail/lite.nhn?nv_mid=14446377701&cat_id=50000804&frm=NVSCPRO&query=%EC%98%B7&&section=review'
#		elif i==2:
#			url ='http://search.shopping.naver.com/detail/lite.nhn?nv_mid=14407949390&cat_id=50000804&frm=&query'
#		url='http://search.shopping.naver.com/detail/lite.nhn?nv_mid=15373663521&cat_id=50000804&frm=&query=&NaPm=ct%3Djm8xkomw%7Cci%3D205069c4668e423bf091cc707cede3dcb4b8424e%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D60e5245d93841e792d33653edd30e166c66fd2eb' 
#		url='https://search.shopping.naver.com/detail/lite.nhn?nv_mid=15183262434&cat_id=50000805&frm=&query=&NaPm=ct%3Djmrtzvso%7Cci%3D96719f774941546a316b0557230fabdc3c5533f5%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D044ad853c54c11218d3d0d9879c1e8659ab75817'
		url=a
		source_code = requests.get(url)
		source_code.encoding = 'utf-8'
		plain_text = source_code.text
		soup = BeautifulSoup(plain_text,'html.parser')	
		title = soup.title
		if title == None:
			continue
		title = title.string.encode('utf-8')
		title = title.strip()
		save.write('%s\r\n\r\n'%title)
		reviews= soup.find_all('div',{'class':'atc'})
		for review in reviews:	
			review_text=review.get_text().strip().split('\r\n')
			for text in review_text:
#				text=text.encode('utf-8')
#				print(text)

				save.write('%s\r\n'%text.encode('utf-8'))
#				print(len(text))
	return
