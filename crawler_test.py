#-*- coding:utf-8 -*-
#linux version

from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import requests
import os

def main():
	save = open(sys.argv[1],'w')
	flag=0
	for i in range(1,2):
		url='https://search.shopping.naver.com/detail/lite.nhn?nv_mid=15183262434&cat_id=50000805&frm=&query=&NaPm=ct%3Djmrtzvso%7Cci%3D96719f774941546a316b0557230fabdc3c5533f5%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D044ad853c54c11218d3d0d9879c1e8659ab75817'
		
		source_code = requests.get(url)
		source_code.encoding = 'utf-8'
		plain_text = source_code.text
		soup = BeautifulSoup(plain_text,'html.parser')	
		title = soup.title
		if title == None:
			continue
#save.write('%s\r\n\r\n'%title)
		reviews= soup.find_all('div',{'class':'atc'})
		for review in reviews:	
			review_text=review.get_text().strip().split('\r\n')
			for text in review_text:
				save.write('%s\r\n'%text.encode('utf-8')

		button_stats= driver.find_elements_by_xpath("shop.detail.ReviewHandler.page(2,'_review-paging')").click()
		driver.excute_script("arguments[0].click()", button_stats[1])
		
#		source_code = requests.get(url)
#		source_code.encoding = 'utf-8'
#		plain_text = source_code.text
		soup = BeautifulSoup(driver.page_source,'html.parser')	
		title = soup.title
		if title == None:
			continue
#save.write('%s\r\n\r\n'%title)
		reviews= soup.find_all('div',{'class':'atc'})
		for review in reviews:	
			review_text=review.get_text().strip().split('\r\n')
			for text in review_text:
				save.write('%s\r\n'%text)










if __name__=='__main__':
	main()
