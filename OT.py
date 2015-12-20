# This file contains a oncogenetic tree
class Vertex: # This is single vertex of a tree
	def __init__(self, Z=0,X=0):
		self.dataH = Z
		self.dataO = X

	parent = 0 # Points to parent.
	childreen = [] # Points to childreen 
	dataH = 0 # Hidden variable
	dataO = 0 # Observable variable


def treePrint(treeRoot): # Recursive print 
	if(treeRoot.childreen): # List is not empty
		print "Has child"
		treePrint(treeRoot.childreen[0]) # Recursive call with child


	print treeRoot.dataO,treeRoot.dataH


class Tree(): # Tree class, contains root, vertexes and methods
	# Attributes of tree
	root = 0; # Pointer to root?
	vertices = []
	def createChild(Z=0,X=0):
		tmpChild = vertex(Z,X)

	
root = Vertex()
child = Vertex(1,2)
root.childreen.append(child)




#treePrint(root)

test = []
test.append("1")
if(test):
	print "Hej"

