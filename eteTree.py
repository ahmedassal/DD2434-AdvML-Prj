from ete3 import  Tree, NodeStyle, TreeStyle 
from abberations import abberations as abbrs
import numpy as np
print "="*35, " START  ", "="*35
# =============================================================================
#									CONSTANTS
# =============================================================================
constNrVertices = 25



# =============================================================================
# Basic tree style
ts = TreeStyle()
#ts.show_node_name = 
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
	t = Tree(name = np.random.choice(abbrs))
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


"""
# =============================================================================
# Draws nodes as small red spheres of diameter equal to 10 pixels
nstyle = NodeStyle()
nstyle["shape"] = "sphere"
nstyle["size"] = 10
nstyle["fgcolor"] = "blue"

for n in t.traverse():
   n.set_style(nstyle)

# Gray dashed branch lines
nstyle["hz_line_type"] = 1
nstyle["hz_line_color"] = "#cccccc"
# =============================================================================
"""
def traveseTree(tree):
	count = 0
	for node in tree.traverse():
  		# Do some analysis on node
  		if (node.is_root()):
  			print "root"
  			node.add_feature("Z",1)
  		else:
  			node.add_feature("Z",0)
  		node.add_feature("X",0)
  		#node.name += (" "+str(count))
		#print node.name
		count +=1

def main():
	tree = generate(constNrVertices)
	print "="*80, "\n\t\t\t\tThis is test tree"
	print tree
	print "="*80
	traveseTree(tree)
	attributes = ["name","Z","X"]
	print tree.get_ascii(show_internal=True, compact=False, attributes=attributes)
	tree.show(tree_style=ts)

	return 0
	


main()
print "="*35, "   END  ", "="*35
