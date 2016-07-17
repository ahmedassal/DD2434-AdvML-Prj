from __future__ import division
from ete3 import  Tree, NodeStyle, TreeStyle, faces, AttrFace
from abberations import abberations as abbrs
from operator import itemgetter
import numpy as np

print "="*35, " START  ", "="*35

# =============================================================================
#									VARIABLES
# =============================================================================
genDataSet = []
chosenNodes = []
qValue = 0.05 # Easiest value, also used 0.1, 0.25, 0.5

# =============================================================================
# Basic tree style
ts = TreeStyle()
#ts.show_node_name =  True
ts.show_leaf_name = True
ts.show_branch_length = True
ts.show_branch_support = True

# =============================================================================

def generateChildren(node,nrVertices,mutations,oneChild = False):
	""" mutations will be emptied, therefor it needs to be a copy """
	#print "genChild"
	#print "numVertices:", nrVertices
	if(nrVertices == 0):
		#print "gCEND"
		return node
	else:
		values = []
		if (oneChild):
			value = nrVertices-1
			values.append(value)
			nrVertices -= 1 
		else:
			while nrVertices > 1:
				value = np.random.randint(0, nrVertices)
				#print "Value: ", value
				if (value > 0):
					values.append(value)
					nrVertices -= value 

		for i in range(len(values)):
			#print mutations
			tmpName = np.random.choice(mutations)
			mutations.remove(tmpName)
			node.add_child(name = tmpName)
			generateChildren(node.children[i],values[i],mutations,oneChild) # Each child gets a int of children


def generate(nrOfVertices,mutations,oneChild=False):
	t = Tree(name= "root")#(name = np.random.choice(abbrs)) # Root it set to same in all trees, confirmed by Jens.
	if ("root" in  mutations):
		mutations.remove("root")
		nrOfVertices -=1
	generateChildren(t,nrOfVertices,mutations,oneChild)
	return t


def setRandomTreeNodes(tree, hot = False): # global = True
	global qValue
	count = 0
	for node in tree.traverse():
  		# Do some analysis on node
  		if (node.is_root()):
  			#print "root"
  			node.dist = 1
  			if(hot):
  				node.add_feature("Px",  1) #
  				node.add_feature("Ex", np.random.uniform(0.01,qValue))
  				node.add_feature("Ez", np.random.uniform(0.01,qValue))
  				#node.add_feature("Px",  np.random.uniform(q,1)) #
  			else: 
  				node.add_feature("Px",  1) #
  				node.add_feature("Ex", np.random.uniform(0.01,qValue))
  				node.add_feature("Ez", np.random.uniform(0.01,qValue))
  		else:
  			#node.add_feature("Z",0)
  			node.dist = np.random.uniform(0.1,1) # See EQ (7) #Jens suggsted using 0.8
  			if(hot): # See EQ (8)# DEBUGG 
  				node.add_feature("Px",  np.random.uniform(qValue,1)) #
  				node.add_feature("Ex", np.random.uniform(0.01,qValue))
  				node.add_feature("Ez", np.random.uniform(0.01,qValue))
  			else: 
  				node.add_feature("Px",  1) #
  				node.add_feature("Ex", np.random.uniform(0.01,qValue))
  				node.add_feature("Ez", np.random.uniform(0.01,qValue))
  		#node.add_feature("X",0)
  		
  		#node.name += (" "+str(count))
		#print node.name
		count +=1

def setTreeNodes(tree,xProbs):
	for node in tree.traverse():
  		if (node.is_root()):
  			node.dist = 1
  			node.add_feature("Px",  xProbs[node.name]) # 
  		else:
  			node.dist = 1 # See EQ (7) #Jens suggsted using 0.8
  			node.add_feature("Px", xProbs[node.name]) # See EQ (8)# DEBUGG 

		count +=1


def treeProb(tree):
	prob = 1
	for node in tree.traverse():
		prob *= node.dist 
	prob 
	return prob

def setTreeNodesCondProb(tree,allEdgesProbs): # X set to 1.
	for node in tree.traverse():
  		if (node.is_root()):
  			node.dist = 1
  			node.add_feature("Px",  1) # UNSURE about this
  		else:
  			for edge in allEdgesProbs:
  				#print "Count"
  				if (edge[0] == node.name and edge[1] == node.up.name):
  					#print "Found it: ", node.dist
					node.dist = edge[4] #node.name, node.parent.name
					break
  			node.add_feature("Px", 1) # See EQ (8)# DEBUGG 




def createDataFunc(tree,dataSet = [],observed= True): # Returns sets of mutations
	if (observed):
		if tree.is_root():
			dataSet.append((tree.name,True))  # UNSURE, appending root "mutation" to tumors. 
			for node in tree.children:
				if (np.random.uniform(0,1) <= node.dist): 
					createDataFunc(node,dataSet,True)
				else:
					createDataFunc(node,dataSet,False)
		else:
			tmpPx = tree.Px
			if (np.random.uniform(0,1) <= tmpPx):
				dataSet.append((tree.name,True))
			else:
				dataSet.append((tree.name,False))
			for node in tree.children:
				if (np.random.uniform(0,1) <= node.dist): 
					createDataFunc(node,dataSet,True)
				else:
					createDataFunc(node,dataSet,False)
	else:
		dataSet.append((tree.name,False))
		for node in tree.children:
			createDataFunc(node,dataSet,False)
	return 

def createDataFuncHash(tree,dataSet = [],observed= True): # Returns sets of mutations
	if (observed):
		if tree.is_root():
			dataSet[tree.name] = True  # UNSURE, appending root "mutation" to tumors. 
			for node in tree.children:
				if (np.random.uniform(0,1) <= node.dist): 
					createDataFuncHash(node,dataSet,True)
				else:
					createDataFuncHash(node,dataSet,False)
		else:
			tmpPx = tree.Px
			if (np.random.uniform(0,1) <= tmpPx):
				dataSet[tree.name] = True
			else:
				dataSet[tree.name] = False
			for node in tree.children:
				if (np.random.uniform(0,1) <= node.dist): 
					createDataFuncHash(node,dataSet,True)
				else:
					createDataFuncHash(node,dataSet,False)
	else:
		dataSet[tree.name] = False
		for node in tree.children:
			createDataFuncHash(node,dataSet,False)
	return 





def evaluateTrees(tree1,tree2):
	ref_edges_in_source = tree1.compare(tree2,unrooted=True)
	return ref_edges_in_source


def createData(tree, nrOfDatapoints):
	data = []
	for i in range(nrOfDatapoints):
		datapoint = []	
		createDataFunc(tree,datapoint)
		data.append(datapoint)

	return data

def createDataHash(tree,nrOfDatapoints):
	data = []
	for i in range(nrOfDatapoints):
		datapoint = {}	
		createDataFuncHash(tree,datapoint)
		data.append(datapoint)		
	return data

def getAllEdges(mutations):
	""" Takes a set of unique mutations, return a list of all possible edges"""
	allEdges = []
	for mutation in mutations: 
		print mutation
		for mutation2 in mutations:
			if not (mutation == mutation2): # No edges connecting to themselves.
				tmp = []
				tmp.append(mutation)
				tmp.append(mutation2)
				allEdges.append(tmp)
	return allEdges


def getEdges(tree): #Returns a list of touples, edges representet by nodes at it's ends
	edges = []
	count = 0
	for node in tree.traverse():
  		# Do some analysis on node
  		if not(node.is_root()):
			edges.append((node.up.name,node.name))
	return edges


def getSimilarity(edges1,edges2):
	""" Takes two sets of edges and return the probability of the later occuring
	in the first set """
	count = 0
	for edge in edges2:
		if (edge in edges1):
			count +=1
	return count / len(edges2)

def calcProbX(data): # probability that a mutation is in a toumor
	""" Input data: a set of tumors containing mutatuions. returns a dict, 
	containing mutations & their probablitiy"""
	flatData = [item for sublist in data for item in sublist]
	flatDataSet = list(set(flatData))
	mutXProbs = {}
	for mutation in flatDataSet: # Could be remade more effective
		mutCount = 0
		for tumor in data:
			if (mutation in	tumor):
				mutCount +=1
		mutXProbs[mutation] = mutCount/len(data) # Occurences / Total nr tumors
	
	return mutXProbs

def condProbs(xProbs,allEdgesProbs):
	for edge in allEdgesProbs:
		edge.append(edge[2] / xProbs[edge[1]])


def calcProbXY(data,allEdges):
	""" probability that mutations X and Y both are observed in tumor"""
	for edge in allEdges:
		count = 0
		count1 = 0
		for tumor in data:
			if ((edge[0] in tumor) or (edge[1] in tumor)):
				count1 += 1
			if ((edge[0] in tumor) and (edge[1] in tumor)):
				count += 1
		edge.append(count/len(data))
		edge.append(count/count1)
	return allEdges 

"""
def calcCondProb(data,allEdges):
	# probability that mutations X and Y both are observed in tumor
	for edge in allEdges:
		countX = 0
		countY = 0
		for tumor in data:
			if (edge[0] in tumor):# or (edge[1] in tumor)):
				countX += 1
				if (edge[1] in tumor):# and (edge[1] in tumor)):
					countY += 1
		#edge.append(count/len(data))
		#edge.append(count/count1)
	return allEdges 
"""
