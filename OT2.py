import numpy as np # Used for matrises, probabilities etc. 
import matplotlib as plt # used for plotting etc. 
# =============================================================================
#									INFO
# =============================================================================
# This file contains a oncogenetic tree
# Code is written within 80 columns. 
# CammelCasing is being used.
# Classes start with large letters. 
# =============================================================================
#									CONSTANTS
# =============================================================================

qProbability = 0.05 # 0.05, 0.1, 0.25, 0.5 # See page 6; 3.1.1
nrVertices = 10 # 25, 40 # See page 6; 3.1.1

# =============================================================================
#	   								 CLASSES
# =============================================================================

class Vertex: # This is single vertex of a tree
	def __init__(self,parent = None, Z=0,X=0,children=[]):
		if not(parent): # If ROOT
			self.Z = 1 #
			self.level = 1
		else:
			self.Z = Z #
			self.level = parent.level+1
		self.X = X #
		self.children = children # Points to childreen 
		self.parent = parent # Points to parent.	
		

	def __str__(self, level=0):
		ret = "\t"*level+repr(self.Z)+"\n"
		for child in self.children:
			ret += child.__str__(level+1)
		return ret

	def __repr__(self):
		return '<tree node representation>'


class Tree(): # Tree class, contains root, vertexes and methods
	# Attributes of tree
	root = Vertex(); # Pointer to root?
	def createChild(self,parent=root,Z=0,X=0):
		#Z = parent.Z
		#X = Z
		tmpChild = vertex(parent,Z,X)

	def isLeaf(self,vertex):
		if not(vertex.children):
			return True
		else:
			return False

# =============================================================================
#									Functions
# =============================================================================

def probZGenerator(parentZ): # Pr[Z(u) = 1|Z(p(u)) = 1] e [0.1,1.0] See page 6. (7)
	if( parentZ == 1): # great probability of childz
		if (np.random.uniform(0.1,1.0) >= 0.5): # COMMENT, see (7)
			return 1
		else:
			return 0
	else: #small probability of childZ
		return 0


def probXGenerator(Z): # Pr[X(u) = 0|Z(u) = 1] e [0.01,q] See page 6. 3.1.1 (8)
	if( Z == 1): # great probability of childZ
		#childZ = numpy.random.uniform(0.01,qProbability) # COMMENT
		# See eq. (8)
		return 1
		
	else: #small probability of childZ
		return 0



root = Tree()
root
str(root)
print root


#treePrint(root)

#root = Vertex()
#root.children = [Vertex(root), Vertex(root)]
#root.children[0].children = [Vertex(), Vertex()]
#root.children[1].children = [Vertex(), Vertex()]
#root
#<tree node representation>
#str(root)
#'grandmother'\n\t'daughter'\n\t\t'granddaughter'\n\t\t'grandson'\n\t'son'\n\t\t'granddaughter'\n\t\t'grandson'\n"
#print root
