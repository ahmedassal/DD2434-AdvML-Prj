from eteTree import *
import likelyhood as lh
import math as math
import emAlgorithm as em
np.random.seed(seed=0)

print "="*35, " MAIN START  ", "="*35
# =============================================================================
#									CONSTANTS
# =============================================================================
constNrVertices = 10 # Report: 10, 25, 40
constNrOfDatapoints = 100 # 
def main():
	global abbrs
	global constNrVertices 
	global constNrOfDatapoints
	#mutations = list(abbrs) # making a COPY
	totalresults = []
	counter = 0
	constStartingTrees = 1
	constGeneratedTrees = 100
	trees = []
	# =========================================================================
	#		 					Create 100 original tree
	# =========================================================================

	for i in range(constStartingTrees): # Create 100 starting trees
		# =========================================================================
		#		 					Create original tree
		# =========================================================================
		mutations = list(abbrs) # Making a COPY of the mutations.
		tree = generate(constNrVertices,mutations,False)
		setRandomTreeNodes(tree, True)
		trees.append(tree)
		data = createDataHash(tree,constNrOfDatapoints) # Resetting tree atributes, ADHOC
		#print data
		#xProbs = calcProbX(data)
		attributes = ["name","Px","Z","X"]
		# =========================================================================
		#							Create 100(x100) new trees.
		# =========================================================================
		#print "="*35, "   Second tree ", "="*35
		 # Start COMMENT
		results = []
		results2 = []
		bestResults = []
		treeProbs = []
		print "Here am I, tree: ", tree
		ts = TreeStyle()
		#ts.rotation = 90
		print "treeLikelyhood", lh.logLikelyhood(tree,data)
		bestScore = -1000000 # Minus infitive 
		treesWithProbs =[]
		bestProbs =[]
		for i in range(constGeneratedTrees): # Create 100 new trees for each starting tree
			#print "\n","="*35, "   TREE NR: ", i, "="*35
			counter +=1
			#print "---------- COUNTER: ",counter
			#tree2 = emAlgorithm(data)
			newTree = em.createTreeFromData(data)
			setRandomTreeNodes(newTree,True)
			
			
			#tmpTreeProb = treeProb(tree)
			newTreeLikelyhood = lh.logLikelyhood(newTree,data)
			result = getSimilarity(getEdges(tree),getEdges(newTree))
			results.append(result)
			treeProbs.append(newTreeLikelyhood)
			treesWithProbs.append((newTree,newTreeLikelyhood))
			"""
			if (bestScore < newTreeLikelyhood):
				bestScore = newTreeLikelyhood
				bestResults.append(result)
				bestProbs.append(newTreeLikelyhood)
			bestResults = bestResults
			"""
			#string = raw_input("continue")
			#trees.append(tree2)
			# =========================================================================
			#								Testing ground
			# =========================================================================
		print "Testing ground START"
		#print data[0]
		for i in data[0].keys():
			print "test: ", tree, "\nData: ",data[0], "\nMutation: ",i, "True", lh.likelyhoodOfXandZ(tree,data[0],i,1)
			print "test: ", tree, "\nData: ",data[0], "\nMutation: ",i, "False", lh.likelyhoodOfXandZ(tree,data[0],i,0)
		print "Testing ground END"
		#treesWithProbs = [] 
		better = treesWithProbs
		while len(better) > 1:
			tmp = []
			better = em.saveBetterHalf(better)
			for i in range(len(better)):
				tmp.append(getSimilarity(getEdges(tree),getEdges(better[i][0])))
			results2.append(tmp)

		#totalresults.append(sum(results)/len(results))
		#totalresults.append(sum(results2)/len(results2))

		
		

		# =========================================================================
		#									MISC
		# =========================================================================
		#print "="*35, "   First tree ", "="*35
		#print tree.get_ascii(show_internal=True, compact=False, attributes=attributes)
		print "="*30, " Induvidual Results ", "="*30
		print bestResults, bestProbs
		print "Average Results ", sum(results)/len(results) # Induvidual results
		#print "Better halfResults ", sum(results2)/len(results2) # Induvidual results
		#print "BestResults ", sum(bestResults)/len(bestResults) # Induvidual results
		#print "Treeprobs ",treeProbs # Induvidual results
		#print "TreeWithprobs ",treesWithProbs # Induvidual results
		for i in range(len(results2)):
			print i, " set is this good: ", sum(results2[i])/len(results2[i]), len(results2[i])

	# =========================================================================
	#								PRINTING RESULTS
	# =========================================================================

	print "\n","="*35, "   OVERALL RESULTS ", "="*35
	print "Count generated trees: ",len(totalresults)
	print "Trees created: ", counter
	#print "Similarity between starting tree and gen-tree: ",sum(totalresults)/len(totalresults) 
	#print "Data presents probabilities:", xProbs
		
	# =========================================================================
	#								PLOTTING RESULTS
	# =========================================================================	
	
	def my_layout(node):
		# Add name label to all nodes
		faces.add_face_to_node(AttrFace("name"), node, column=0, position="branch-right")
		faces.add_face_to_node(AttrFace("Px"), node, column=0, position="branch-right")
		#faces.add_face_to_node(AttrFace("Z"), node, column=0, position="branch-right")
		#faces.add_face_to_node(AttrFace("X"), node, column=0, position="branch-right")
	
	#print tree.features
	ts = TreeStyle()
	#ts.rotation = 90
	ts.show_leaf_name = False
	ts.show_branch_length = True
	ts.layout_fn = my_layout	
	for tmpTree in trees:
		tmpTree.show(tree_style=ts)

	 
	# =========================================================================
	#									MISC
	# =========================================================================
	#print "Get edges: ",tree.get_edges()
	#print len(results["common_edges"])/len(results["source_edges"])
	#print "="*35, "   Edges ", "="*35
	#print "Tree1:",getEdges(tree)
	#print "Tree2:",getEdges(tree2)
	#get_topology_id(attr='name')
	return 0
	

main()
print "="*35, "  MAIN END  ", "="*35