import numpy as np

def calF1(tp, fp, fn):
	precision = []
	recall = []
	fscore = []
	for i in range(len(tp)):
		if (tp[i] + fp[i]) == 0:
			precision.append(0.0)
		else:
			precision.append((tp[i] * 1.0) / (tp[i] + fp[i]))
		if (tp[i] + fn[i]) == 0:
			recall.append(0.0)
		else:
			recall.append((tp[i] * 1.0) / (tp[i] + fn[i]))
		if (precision[i] + recall[i]) == 0:
			fscore.append(0.0)
		else:
			fscore.append((2.0 * precision[i] * recall[i]) / (precision[i] + recall[i]))
	return fscore, precision, recall

def calculate(classSize, prediction, target):
	tp = np.array([0] * (classSize + 1))
	fp = np.array([0] * (classSize + 1))
	fn = np.array([0] * (classSize + 1))

	for i in range(len(prediction)):
		for j in range(len(prediction[i])):
			if target[i][j] == prediction[i][j]:
				tp[target[i][j]] += 1
			else:
				fp[target[i][j]] += 1
				fn[prediction[i][j]] += 1
	for i in range(classSize-1):
		tp[classSize] += tp[i]
		fp[classSize] += fp[i]
		fn[classSize] += fn[i]
	return tp, fp, fn

def makeF1(prediction, target):
	classSize = len(target[0][0])
	target = np.argmax(target, 2)
	tp, fp, fn = calculate(classSize, prediction, target)
	
	fscore, precision, recall = calF1(tp, fp, fn)

	return fscore, precision, recall

def makeMergeF1(prediction, target):
	classSize = len(target[0][0])
	target = np.argmax(target, 2)
	tp, fp, fn = calculate(classSize, prediction, target)

	mergeTp = np.array([0] * ((classSize/2)+2))
	mergeFp = np.array([0] * ((classSize/2)+2))
	mergeFn = np.array([0] * ((classSize/2)+2))

	for i in range(0,classSize-2,2):
		mergeTp[i/2] = tp[i] + tp[i + 1]
		mergeFp[i/2] = fp[i] + fp[i + 1]
		mergeFn[i/2] = fn[i] + fn[i + 1]
	mergeTp[(classSize/2)] = tp[classSize-1]
	mergeFp[(classSize/2)] = fp[classSize-1]
	mergeFn[(classSize/2)] = fn[classSize-1]

	for i in range(classSize-1):
		mergeTp[(classSize/2)+1] += tp[i]
		mergeFp[(classSize/2)+1] += fp[i]
		mergeFn[(classSize/2)+1] += fn[i]

	fscore, precision, recall = calF1(mergeTp, mergeFp, mergeFn)
	return fscore, precision, recall