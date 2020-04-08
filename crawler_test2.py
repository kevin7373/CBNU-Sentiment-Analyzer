#-*- coding:utf-8 -*-
from selenium import webdriver
import urllib
import requests
from bs4 import BeautifulSoup
import time
import sys
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.chrome.options import Options 
from pyvirtualdisplay import Display

def main():
	
	display=Display(visible=0, size=(1024,768))
	display.start()
	save=open(sys.argv[1],'w')
	print("시발1")	
	driver = webdriver.Chrome('chromedriver')
	print("시발2")	
	driver.get('https://search.shopping.naver.com/detail/lite.nhn?nv_mid=15158400401&cat_id=50000830&frm=&query=&NaPm=ct%3Djnvabukg%7Cci%3D0047d97a867f42fb75bfd1e2ccad68adc2da1039%7Ctr%3Dslsl%7Csn%3D95694%7Chk%3D3096bf847999ea0997a5f4214a12cd6c873c3c32')
	time.sleep(2)

	total = driver.find_element_by_xpath("//div[contains(@class, 'atc')]")
	total_text = total.text
	total_array= total_text.split()
	print("시발")	
	for i in len(total_array):
		save.write("%s\n"%total_array[i])


if __name__=='__main__':
	main()
