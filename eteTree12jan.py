from ete3 import  Tree, NodeStyle, TreeStyle 
from abberations import abberations as abbrs
import numpy as np
print "="*35, " START  ", "="*35
# =============================================================================
#									CONSTANTS
# =============================================================================
constNrVertices = 10+1 #10 + root
nrOfDatapoints = 100
# =============================================================================
#									VARIABLES
# =============================================================================
genDataSet = []

# =============================================================================
# Basic tree style
ts = TreeStyle()
#ts.show_node_name =  True
ts.show_leaf_name = True
ts.show_branch_length = True
ts.show_branch_support = True

# =============================================================================

def generateChildren(node):#,nrOfVertices):
	global constNrVertices
	if(constNrVertices <= 0):
		return node
	nrChildren = np.random.randint(constNrVertices)
	constNrVertices-= nrChildren
	for i in range(nrChildren):
		node.add_child(name = np.random.choice(abbrs))
		generateChildren(node.children[i])#,nrOfVertices-1)


def generate(nrOfVertices):
	t = Tree()#(name = np.random.choice(abbrs))
	#t.populate(nrOfVertices)
	generateChildren(t)#,nrOfVertices)
	#nrOfChildren = np.random.randint(nrOfVertices)
	#nrOfVertices -= nrOfChildren
	"""
	for i in range(3):
		t.add_child(name=np.random.choice(abbrs))

	for k in range(3):
		for i in range(3):
			t.children[k].add_child(name=np.random.choice(abbrs))
			#for j in range(3):
			#	t.children[k].children[j].add_child(name=np.random.choice(abbrs))
	"""
	return t


#TreeNode.dist	#stores the distance from the node to its parent (branch length). Default value = 1.0	1.0



def traveseTree(tree):
	count = 0
	q = 0.05
	for node in tree.traverse():
  		# Do some analysis on node
  		if (node.is_root()):
  			print "root"
  			node.add_feature("Z",1)
  		else:
  			node.add_feature("Z",0)
  			node.dist =  np.random.uniform(0.1,1) # See EQ (7)
  			node.add_feature("Px",  np.random.uniform(q,1)) # See EQ (8)  1)# DEBUGG #,
  		node.add_feature("X",0)
  		
  		#node.name += (" "+str(count))
		#print node.name
		count +=1

def createData(tree,dataSet): # Returns sets of mutations
	if tree.is_root():
		# DO LESS
		for node in tree.children:
			tmpPz = tree.get_distance(node) # Distance to child	
			if (np.random.uniform(0,1) <= tmpPz): 
				createData(node,dataSet)
	else:
		tmpPx = tree.Px
		if (np.random.uniform(0,1) <= tmpPx):
			dataSet.append(tree.name)
		for node in tree.children:
			tmpPz = tree.get_distance(node) # Distance to child	
			if (np.random.uniform(0,1) <= tmpPz): 
				createData(node,dataSet)
	return 


def main():
	tree = generate(constNrVertices)
	print "="*80, "\n\t\t\t\tThis is test tree"
	print tree
	print "="*80
	traveseTree(tree)
	data = []
	for i in range(nrOfDatapoints):
		datapoint = []	
		createData(tree,datapoint)
		data.append(datapoint)

	print "Gendata all set:", data
	flatData = [item for sublist in data for item in sublist]
	print "Gendata flat:", flatData # Flatten list
	print "Unique flat data:",set(flatData) # Unique mutations
	attributes = ["name","Px","Z","X"]
	print tree.get_ascii(show_internal=True, compact=False, attributes=attributes)
	tree.show(tree_style=ts)
	return 0

main()
print "="*35, "   END  ", "="*35
