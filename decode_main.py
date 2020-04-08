#-*- coding:utf-8 -*-

import tensorflow as tf
from tensorflow.python.framework import ops
import argparse
import sys
from loader import *
from model import *
from learn_main import makePred
from eval_label import makeMergeF1

def main(args):
	sentiTags=['0','1','2','3']
	save = open(args.result,'w')

	inputData, solData, maxLength = loadData(args.inputData, None, args.embedding)
	ops.reset_default_graph()
	model = Model(maxLength, len(inputData[0][0]), len(solData[0][0]), args.rnnSize, args.gpu)
	maximum = 0
	e = 0
	config = tf.ConfigProto(allow_soft_placement = True)
	print 'finish setting'
	with tf.Session(config = config) as sess:
		with tf.device(args.gpu):
			sess.run(tf.global_variables_initializer())
			saver = tf.train.Saver()
			saver.restore(sess, args.model)

			print 'start Decoding'
			tfUnaryScores, tfTransitionParams, sentenceLength = sess.run(
				[model.unaryScore, model.transitionParams, model.length], 
				{model.inputData: inputData, model.outputData: solData})
			pred = makePred(tfUnaryScores, tfTransitionParams, sentenceLength)
			m, precision, recall = makeMergeF1(pred, solData)
			microArgF1 = (len(solData[0][0])/2) + 1

			print 'finish Decoding'
			i = 0
			j = 0
			save.write('micro F1: %f\r\n'%microArgF1)
			for line in open(args.inputData,'r'):
				if line in ['\n','\r\n']:
					i += 1
					j = 0
					save.write('\r\n')
				else:
					line = line.strip()
					predTag = sentiTags[pred[i][j]]
					#lemma solution predtag
					save.write(line+'\t'+predTag+'\r\n')
					j+=1
			print 'finish save'

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputData', type=str, help='input data', required=True)
	parser.add_argument('--model', type=str, help='path of model data', required=True)
	parser.add_argument('--result', type=str, help='path of result data', default=None)
	parser.add_argument('--embedding', type=str, help='embedding vectors', required=True)
	parser.add_argument('--rnnSize',type=int, help='rnn size defalut 256', default=256)
	parser.add_argument('--gpu', type=str, help='GPU number', default='/gpu:0')
	main(parser.parse_args())
