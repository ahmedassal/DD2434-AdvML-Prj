from __future__ import division
from ete3 import  Tree, NodeStyle, TreeStyle 
from abberations import abberations as abbrs
import numpy as np
import random
print "="*35, " START  ", "="*35
# =============================================================================
#									CONSTANTS
# =============================================================================
constNrVertices = 10 #10 + root
nrOfDatapoints = 100
# =============================================================================
#									VARIABLES
# =============================================================================
genDataSet = []
badChildren = []
chosenNodes = []

# =============================================================================
# Basic tree style
ts = TreeStyle()
#ts.show_node_name =  True
ts.show_leaf_name = True
ts.show_branch_length = True
ts.show_branch_support = True

# =============================================================================

def generateChildren(node,nrVertices,mutations):
	#print "genChild"
	if(nrVertices == 0):
		return node
	else:
		values = []
		while nrVertices > 0:
			#print nrVertices
			value = np.random.randint(0, nrVertices)
			values.append(value)
			nrVertices -= value +1

		for i in range(len(values)):
			#print mutations
			tmpName = np.random.choice(mutations)
			mutations.remove(tmpName)
			node.add_child(name = tmpName)
			generateChildren(node.children[i],values[i],mutations) # Each child gets a int of children


def generate(nrOfVertices,mutations):
	t = Tree(name= "root")#(name = np.random.choice(abbrs)) # Root it set to same in all trees, confirmed by Jens.
	generateChildren(t,nrOfVertices,mutations)
	return t


def traveseTree(tree):
	count = 0
	q = 0.05
	for node in tree.traverse():
  		# Do some analysis on node
  		if (node.is_root()):
  			#print "root"
  			node.add_feature("Z",1)
  		else:
  			node.add_feature("Z",0)
  			node.dist =  np.random.uniform(0.8,1) # See EQ (7) #Jens suggsted using 0.8
  			node.add_feature("Px",  np.random.uniform(q,1)) # See EQ (8)  1)# DEBUGG #,
  		node.add_feature("X",0)
  		
  		#node.name += (" "+str(count))
		#print node.name
		count +=1


def createDataFunc(tree,dataSet): # Returns sets of mutations
	if tree.is_root():
		# DO LESS
		for node in tree.children:
			tmpPz = tree.get_distance(node) # Distance to child	
			if (np.random.uniform(0,1) <= tmpPz): 
				createDataFunc(node,dataSet)
	else:
		tmpPx = tree.Px
		if (np.random.uniform(0,1) <= tmpPx):
			dataSet.append(tree.name)
		for node in tree.children:
			tmpPz = tree.get_distance(node) # Distance to child	
			if (np.random.uniform(0,1) <= tmpPz): 
				createDataFunc(node,dataSet)
	return 


def emAlgorithm(data):
	flatData = [item for sublist in data for item in sublist]
	flatDataSet = list(set(flatData))
	tree = generate(len(flatDataSet),flatDataSet)
	#print (len(flatDataSet))
	traveseTree(tree)
	return tree


def evaluateTrees(tree1,tree2):
	ref_edges_in_source = tree1.compare(tree2,unrooted=True)
	return ref_edges_in_source


def createData(tree):
	data = []
	global nrOfDatapoints # Constant
	for i in range(nrOfDatapoints):
		datapoint = []	
		createDataFunc(tree,datapoint)
		data.append(datapoint)

	return data


def getEdges(tree): #Returns a list of touples, edges representet by nodes at it's ends
	edges = []
	count = 0
	q = 0.05
	for node in tree.traverse():
  		# Do some analysis on node
  		if not(node.is_root()):
			edges.append((node.up.name,node.name))
	return edges


def getSimilarity(edges1,edges2):
	count = 0
	for edge in edges2:
		if (edge in edges1):
			count +=1
	return count / len(edges2)


def main():
	global abbrs
	global constNrVertices 
	#mutations = list(abbrs) # making a COPY
	totalresults = []
	counter = 0
	# =========================================================================
	#		 					Create 100 original tree
	# =========================================================================

	for i in range(100): # Create 100 starting trees

		mutations = list(abbrs) # Making a COPY of the mutations.
		# =========================================================================
		#		 					Create original tree
		# =========================================================================

		tree = generate(constNrVertices,mutations)
		traveseTree(tree)

		# =========================================================================
		#							Print original tree
		# =========================================================================	
		attributes = ["name","Px","Z","X"]
		
		# =========================================================================
		#								Create Data
		# =========================================================================
		data = createData(tree) # Resetting tree atributes, ADHOC
		
		# =========================================================================
		#							Create 100(x100) new trees.
		# =========================================================================
		#print "="*35, "   Second tree ", "="*35
		results = []
		for i in range(100): # Create 100 new trees for each starting tree
			counter +=1
			tree2 = emAlgorithm(data)
			result = getSimilarity(getEdges(tree),getEdges(tree2))
			results.append(result)

		totalresults.append(sum(results)/len(results))

		# =========================================================================
		#									MISC
		# =========================================================================
		#print "="*35, "   First tree ", "="*35
		#print tree.get_ascii(show_internal=True, compact=False, attributes=attributes)
		#print "="*35, "   Results ", "="*35
		#print "Results ",results, sum(results)/len(results) # Induvidual results
		
	

	print "\n","="*35, "   RESULTS ", "="*35
	print counter, " trees created."
	print len(totalresults), sum(totalresults)/len(totalresults) 
		
	
	tree.show(tree_style=ts)

	# =========================================================================
	#									MISC
	# =========================================================================
	#print "Get edges: ",tree.get_edges()
	#print len(results["common_edges"])/len(results["source_edges"])
	#print "="*35, "   Edges ", "="*35
	#print "Tree1:",getEdges(tree)
	#print "Tree2:",getEdges(tree2)
	return 0
	

main()
print "="*35, "   END  ", "="*35
