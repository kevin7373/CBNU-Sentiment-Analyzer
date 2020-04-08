#-*-coding:utf-8 -*-
from flask import Flask, render_template, redirect, request, url_for, jsonify, Blueprint
from pymongo import MongoClient
from jinja2 import Template
import math, decimal
from werkzeug import secure_filename
import sys
import make_jason
import language_module
import makeCoNLLform
import crawler_naver
import crawl_pre
import json
from ast import literal_eval
import ast
import os
from time import localtime, strftime

reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)

sort_flag = 1
user_file_count = 1
f3 = {}
index_1 = 116

@app.route('/')
def main():
	#DB connection
	client = MongoClient('mongodb://localhost:27017/')
	db = client.student
	collection = db.test_1
	results = collection.find().sort('count', -1).limit(3)
	pos_count = collection.find({"$where":"this.jso.pos_sen > this.jso.neg_sen"}).count()
	neg_count = collection.find({"$where":"this.jso.neg_sen > this.jso.pos_sen"}).count()
	pos_num = collection.find({"$where":"this.jso.pos_sen > this.jso.neg_sen"}, {"_id":0, "num":1}).sort('jso.pos_sen', -1)[0]
	neg_num = collection.find({"$where":"this.jso.neg_sen > this.jso.pos_sen"}, {"_id":0, "num":1}).sort('jso.neg_sen', -1)[0] 
	return render_template('index.html', data = results, pos = pos_count, neg = neg_count, pos_num = pos_num, neg_num = neg_num)

@app.route('/index')
def index():
	#DB connection
	client = MongoClient('mongodb://localhost:27017/')
	db = client.student
	collection = db.test_1
	results = collection.find().sort('count', -1).limit(3)
	pos_count = collection.find({"$where":"this.jso.pos_sen > this.jso.neg_sen"}).count()
	neg_count = collection.find({"$where":"this.jso.neg_sen > this.jso.pos_sen"}).count()
	pos_num = collection.find({"$where":"this.jso.pos_sen > this.jso.neg_sen"}, {"_id":0, "num":1}).sort('jso.pos_sen', -1)[0]
	neg_num = collection.find({"$where":"this.jso.neg_sen > this.jso.pos_sen"}, {"_id":0, "num":1}).sort('jso.neg_sen', -1)[0]
	return render_template('index.html', data = results, pos = pos_count, neg = neg_count, pos_num = pos_num, neg_num = neg_num)

@app.route('/analysis')
def analysis():
	global sort_flag
	sort_flag = 1
	return render_template('analysis.html')

@app.route('/analysis2')
def analysis2():
	return render_template('analysis2.html')

@app.route('/analysis3')
def analysis3():
	return render_template('analysis3.html')

@app.route('/index5')
def index5():
	return render_template('index5.html')


@app.route('/board', methods=['POST'])
def search():
	search_contents = request.form['search_contents']
	if search_contents == '':
		return redirect(url_for('board', recent_page = 1, search_contents = ' '))
	else:
		return redirect(url_for('board', recent_page = 1, search_contents = search_contents))

@app.route('/sort/<int:recent_page>/<search_contents>')
def sort(recent_page, search_contents):
	
	return redirect(url_for('board'))

@app.route('/board', defaults={'recent_page':1, 'search_contents':' '})
@app.route('/board/<int:recent_page>/<search_contents>')
def board(recent_page, search_contents):
	global sort_flag
	skip_num = (recent_page - 1) * 10
	
	#DB connection
	client = MongoClient('mongodb://localhost:27017/')
	db = client.student
	collection = db.test_1
	
	if search_contents == ' ':
		results = collection.find().skip(skip_num).sort('num', -1).limit(10)
	
	else:
		results = collection.find({"$or": [{'num':{'$regex':search_contents, '$options':'i'}}, {'title':{'$regex':search_contents, '$options':'i'}}, {'name':{'$regex':search_contents, '$options':'i'}}]}).skip(skip_num).sort('num', -1).limit(10)
	client.close()
	
	#time
	today_date = strftime("%Y-%m-%d", localtime())

	#pagination
	total_record = results.count()
	record_per_page = 10.0
	total_page = math.ceil(total_record / record_per_page)
	total_page = int(total_page)
	page_per_block = 5.0
	total_block = math.ceil(total_page / page_per_block)
	recent_block = math.ceil(recent_page / page_per_block)
	recent_block = int(recent_block)
	
	if recent_block == 0:
		start_page = 1
	
	else:
		start_page = (int(recent_block) - 1) * int(page_per_block) + 1
	
	end_page = start_page + int(page_per_block) - 1
	
	if end_page > total_page:
		end_page = total_page
	
	pre_page = recent_page - 1
	next_page = recent_page + 1
	
	return render_template('board.html', data = results, recent_page = recent_page, start_page = start_page, end_page = end_page, total_page = total_page, recent_block = recent_block, total_block = total_block, total_record = total_record, search_contents = search_contents)

@app.route('/board_2/<int:recent_page>/<int:num>/<search_contents>', methods=['POST'])
def update(recent_page, num, search_contents):
	contents = request.form['contents']
	password = request.form['password']
	client = MongoClient('mongodb://localhost:27017/')
	db = client.student
	collection = db.test_1
	results = collection.find_one({'num':num})
	if password == results['password']:
		update = collection.update({"num":num}, {"$set":{"contents":contents}})
		results = collection.find_one({'num':num})
	else:
		results = collection.find_one({'num':num})
	client.close()
	return render_template('board_2.html', data = results, num = num, recent_page = recent_page, search_contents = search_contents, index_1 = index_1)

@app.route('/board_2/<int:recent_page>/<int:num>/<search_contents>')
def board_2(recent_page, num, search_contents):
	
	client = MongoClient('mongodb://localhost:27017/')
	db = client.student
	collection = db.test_1
	global index_1
	collection.update({'num':num}, {"$inc":{"count":1}})
	global results
	
	results = collection.find_one({'num':num})
	client.close()
	return render_template('board_2.html', data = results, num = num, recent_page = recent_page, search_contents = search_contents, index_1 = index_1)

@app.route('/modify/<int:recent_page>/<int:num>/<search_contents>', methods=['POST'])
def modify(recent_page, num, search_contents):
	client = MongoClient('mongodb://localhost:27017/')
	db = client.student
	collection = db.test_1
	results = collection.find_one({'num':num})
	client.close()
	return render_template('modify.html', num = num, data = results, recent_page = recent_page, search_contents = search_contents)

@app.route('/delete/<int:recent_page>/<int:num>/<search_contents>', methods=['POST'])
def delete(recent_page, num, search_contents):
	password = request.form['password']
	client = MongoClient('mongodb://localhost:27017/')
	db = client.student
	collection = db.test_1
	results = collection.find_one({"num":num})
	if password == results['password']:
		delete = collection.remove({"num":num})
		collection.update({"num":{"$gte":num}}, {"$inc":{"num":int(-1)}}, multi=True)
		results = collection.find({"num":num})

		for file in os.listdir("./static/image"):
			if int(os.path.splitext(file)[0]) == num:
				if os.path.exists("./static/image"):
					os.remove("./static/image/" + str(num) + ".jpg")
					continue
			elif int(os.path.splitext(file)[0]) > num:
				if os.path.exists("./static/image"):
					os.rename("./static/image/" + file, "./static/image/" + str(int(os.path.splitext(file)[0])-1) + ".jpg")
				else:
					print("no exits")
	else:
		results = collection.find({"num":num})
	return redirect(url_for('board', recent_page = recent_page, search_contents = search_contents, num = num))


@app.route('/analysis3', methods = ['POST', 'GET'])
def upload_file():
	lang_csa='lang_csa'
	CoNLL_csa='CoNLL_csa'
	raw_csa = request.files['FileName']
	language_module.result_language(raw_csa,lang_csa)
	makeCoNLLform.result_CoNLL(lang_csa,CoNLL_csa)
	os.system('./decode.sh')
	model_csa=open('./input_pre/model_csa.txt','r')
	f2=make_jason.result_jason(model_csa,user_file_count)
	global index_1
	global user_file_count
	user_file_count += 1
	global f3
	f3 = json.loads(f2)
	return render_template('analysis3.html', jso=f3, index_1 = index_1)


@app.route('/upload_url', methods = ['POST'])
def upload_url():
	lang_csa='lang_csa'
	CoNLL_csa='CoNLL_csa'
	url_name= request.form['urlname']
	crawler_naver.crawl(url_name,'crawltext')
	crawl_pre.crawl_pre('crawltext','crawltext_pre')
	raw_csa=open('./input_pre/crawltext_pre.txt','r')
	language_module.result_language(raw_csa,lang_csa)
	makeCoNLLform.result_CoNLL(lang_csa,CoNLL_csa)
	os.system('./decode.sh')
	model_csa=open('./input_pre/model_csa.txt','r')
	f2=make_jason.result_jason(model_csa,user_file_count)
	global index_1
	global user_file_count
	user_file_count += 1
	global f3
	f3 = json.loads(f2)
	
	return render_template('analysis3.html', jso=f3, index_1 = index_1)


@app.route('/upload_data/<jso>', methods =['POST'])
def upload_data(jso):
	image = request.files['ImgName']
	name = request.form['name']
	contents = request.form['contents']
	password = request.form['password']
	title = request.form['title']

	jso = literal_eval(jso)

	date = strftime("%Y-%m-%d", localtime())
	time = strftime("%H:%M", localtime())

	client = MongoClient('mongodb://localhost:27017/')
	db = client.student
	collection = db.test_1
	total_record = collection.find().count()
	
	insert = collection.insert({"num":total_record + 1, "jso":jso, "contents":contents, "title":title, "name":name, "password":password, "date":date, "time":time})
	image.save('./static/image/' + secure_filename(str(total_record + 1) + '.jpg'))
	return redirect(url_for('board'))

@app.route('/table')
@app.route('/table/<int:index_1>', methods=['POST', 'GET'])
def table(index_1):
	if request.method == 'POST':
		return render_template('table.html', jso=f3, index_1=index_1)
	if request.method == 'GET':
		return render_template('table.html', jso=f3, index_1=index_1)

@app.route('/table_board')
@app.route('/table_board/<int:index_1>', methods=['POST', 'GET'])
def table_board(index_1):
	return render_template('table_board.html', data = results, index_1 = index_1)

if __name__ == '__main__':
	app.run(debug = True, host ='0.0.0.0', port=7000)
