from eteTree import generate
from operator import itemgetter
import likelyhood as lh
import numpy as np

def observedMutationSet(data):
	flatData = []#[item for sublist in data for item in sublist.keys()]
	for X in data:
		for mutation in X.keys():
			flatData.append(mutation)
	flatDataSet = list(set(flatData))
	return flatDataSet

def emAlgorithm(data):

	return tree


def createTreeFromData(data):
	flatDataset = observedMutationSet(data)
	#print flatDataset
	return generate(len(flatDataset),list(flatDataset))


def saveBetterHalf(treesAndlikelyhoods):
	ret = []
	ret = sorted(treesAndlikelyhoods, key=itemgetter(1), reverse = True)
	ret = ret[:len(ret)/2]
	return ret


def probListA(tree,data):
	probDict = {}

	for arc in tree.iter_descendants():
		ab = np.matrix([[0,0],[0,0]])
		for a in range(0,1):
			for b in range(0,1):
				for i in data:
					ab[a][b] += lh.likelyhoodOfXZandZp(tree,i,arc,a,b) * lh.likelyhoodOfX(tree,i)

		probDict[arc] = ab
	return probDict

def probListB(tree,data):
	probDict = {}

	for arc in tree.iter_descendants():
		aList = np.matrix([[0,0],[0,0]])
		for a in range(0,1):
			for X in data:
				if X(arc.name):
					ab[1][a] += lh.likelyhoodOfXZ(tree,i,arc,a) * lh.likelyhoodOfX(tree,i)
				else:
					ab[0][a] += lh.likelyhoodOfXZ(tree,i,arc,a) * lh.likelyhoodOfX(tree,i)

		probDict[arc] = aList
	return probDict


def Asum(probList,arc,a,b):
	probDict = {}
	ab = np.matrix([[0,0],[0,0]])
	for a in range(0,1):
		for b in range(0,1):
			for i in data:	
				print i


def Asum(probList,arc,a,b):
	probDict = {}
	ab = np.matrix([[0,0],[0,0]])
	for a in range(0,1):
		for b in range(0,1):
			for i in data:
				print i