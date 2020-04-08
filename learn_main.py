#-*- coding:utf-8 -*-

import tensorflow as tf
from tensorflow.python.framework import ops
import numpy as np
import argparse
import sys
from loader import *
from model import *
from eval_label import makeF1

def makePred(unaryScores, transitionParams, sentenceLength):
	prediction = []
	for unaryScore, length in zip(unaryScores, sentenceLength):
		unaryScore = unaryScore[:length]
		viterbiSequence, _ = tf.contrib.crf.viterbi_decode(unaryScore, transitionParams)
		viterbiSequence = np.array(viterbiSequence)
		prediction.append(viterbiSequence)
	return prediction

def saveScore(save, f1, precision, recall):
	save.write('F1\t')
	for f in f1:
		save.write('%f\t'%f)
	save.write('\r\nPrecision\t')
	for p in precision:
		save.write('%f\t'%p)
	save.write('\r\nRecall\t')
	for r in recall:
		save.write('%f\t'%r)
	save.write('\r\n')

def submodel(args, trainInput, trainOutput, testInput, testOutput, maxLength, isall, sentiTags, modelname):
	ops.reset_default_graph()
	model = Model(maxLength, len(trainInput[0][0]), len(trainOutput[0][0]), args.rnnSize, args.gpu)
	print 'finish model setting'
	if sentiTags != None:
		save = open(args.result,'w')
		savePred = open(args.pred,'w')

	maximum = 0
	e = 0
	config = tf.ConfigProto(allow_soft_placement = True)
	with tf.Session(config = config) as sess:
		with tf.device(args.gpu):
			sess.run(tf.global_variables_initializer())
			print 'start learning'
			saver = tf.train.Saver()
			while(e <= args.maxepoch):
				for ptr in range(0, len(trainInput), args.batchSize):
					if (ptr + args.batchSize) > len(trainInput):
						break
					sess.run(model.trainOp, 
						{model.inputData: trainInput[ptr: ptr + args.batchSize], 
						model.outputData: trainOutput[ptr: ptr + args.batchSize]})

				tfUnaryScores, tfTransitionParams, sentenceLength = sess.run(
					[model.unaryScore, model.transitionParams, model.length], 
					{model.inputData: testInput, model.outputData: testOutput})
				
				pred = makePred(tfUnaryScores, tfTransitionParams, sentenceLength)
				m, precision, recall = makeF1(pred, testOutput)
				overall = len(testOutput[0][0])

				if m[overall] > maximum:
					print 'maximum F1 epoch: %d F1: %f'%(e,m[overall])
					print m
					bestOutput = pred;
					maximum = m[overall]
					f1s = m
					testEntityOutput = tfUnaryScores
					trainEntityOutput = sess.run(model.unaryScore, 
					{model.inputData: trainInput, model.outputData: trainOutput})
					if sentiTags != None:
						save.write('best epoch: %d F1: %f\r\n'%(e, m[overall]))
						saveScore(save, m, precision, recall)
					#모델 저장 
					save_path = saver.save(sess, 'model/'+modelname+'.ckpt')
				elif e % 10 ==0 :
					print 'epoch: %d F1: %f '%(e,m[overall])
					if sentiTags != None:
						save.write('epoch : %d F1: %f\r\n'%(e,m[overall]))
						saveScore(save, m, precision, recall)
				e += 1
			sess.close()

	if sentiTags != None:
		i = 0
		j = 0
		savePred.write('F1: %f\r\n'%maximum)
		for line in open(args.test,'r'):
			if line in ['\n','\r\n']:
				i += 1
				j = 0
				savePred.write('\r\n')
			else:
				line = line.strip()
				predTag = sentiTags[bestOutput[i][j]]
				savePred.write(line+'\t'+predTag+'\r\n')
				j+=1
	return trainEntityOutput, testEntityOutput, f1s

def main(args):
	sentiTags = ['0', '1', '2', '3']
	trainInput, trainOutput, testInput, testOutput, maxLength = loadData(args.train, args.test, args.embedding)
	temp = len(trainInput[0][0])
	for tr in trainInput:
		for t in tr:
			if temp != len(t):
				print len(t)
	temp = len(testOutput[0][0])
	for tr in testOutput:
		for t in tr:
			if temp != len(t):
				print len(t)

	print 'finish loading'
	submodel(args, trainInput, trainOutput, testInput, testOutput, maxLength, False, sentiTags, 'single')


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--train', type=str, help='train data', required=True)
	parser.add_argument('--test', type=str, help='test data', required=True)
	parser.add_argument('--pred', type=str, help='predition test data', required=True)
	parser.add_argument('--maxepoch', type=int, help='maxium epoch', default=500)
	parser.add_argument('--embedding', type=str, help='embedding vectors', required=True)
	parser.add_argument('--result', type=str, help='path of result data', default=None)
	parser.add_argument('--learningRate',type=float, help='learning rate defalut 0.01', default=0.01)
	parser.add_argument('--rnnSize',type=int, help='rnn size defalut 256', default=256)
	parser.add_argument('--gpu', type=str, help='GPU number', default='/gpu:0')
	parser.add_argument('--batchSize',type=int, help='batch size defalut 64', default=64)
	main(parser.parse_args())
