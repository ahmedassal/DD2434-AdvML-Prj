from __future__ import division
import math as math

epsilonZ = 0.01
epsilonX = 0.01
def calcProbForDataPoint(tree,X): # X is a datapoint
	""" Should probably use reverse order traversal for this. The use dynamic 
		programming to speed up process. """
	#print "calcProb:", X
	prob = 0
	for node in tree:
			#print "leaf"
			if (X[node.name]):
				tmp = 1
				#t.get_leaves_by_name(name)
				# Traverse tree from mutation to root
				# check distance from all mutations. 

				node = tree.search_nodes(name=mutation[0])[0]

				while node:
					tmp *= node.dist
					node = node.up
				prob += tmp
			else: 
				#if (mutation[1]):
				tmp = 1
				#t.get_leaves_by_name(name)
				# Traverse tree from mutation to root
				# check distance from all mutations. 

				node =tree.search_nodes(name=mutation[0])[0]

				while node:
					tmp *= (1-node.dist)
					#print node.dist
					node = node.up
				prob += tmp
			print mutation, tmp
	print prob
"""
def calcAllposProbForDataPoint(tree): # X is a datapoint
	print "calcProb:", X
	for mutation in X:
"""
def allChildrenAreLeaves(tree):
	#print tree
	if (tree.is_leaf()):
		#print "Tree is leaf"
		return False
	for node in tree.children:
		if not (node.is_leaf()):
			return False
	#print "All leaves"
	return True

def calcProbForSubtree(tree,X):
	""" SHould probably be re-written using only trees, no X. """
	ret = 1
	#for node in tree: # Iterates over all leaves
	for node in tree:
		#print "Mutation: ", mutation[0]
		#print tree
		if node.is_leaf():
			#print mutation[0]," is in the tree"
			if (X[node.name]):	
				ret *= node.dist * node.Px
			else: 
				ret *= (1-node.dist + node.dist*(1-node.Px))
		if node.is_root():
			if (mutation[1]):	
				ret *= node.dist * node.Px
			else: 
				ret *= (1-node.dist + node.dist*(1-node.Px))
	#print "subtreeProb: ",ret
	return ret

def calcProbForLeaf(tree,X):
	ret = 1
	observed = False
	for node in tree:
		#print "X: ",X, "node name: ",node.name, "Tree: ",tree
		if (X[node.name]):	
			ret *= tree.dist * tree.Px
			observed = True
		else: 
			ret *= ((1-tree.dist) + (tree.dist*(1-tree.Px)))
	#print tree, observed, " is this likley ", ret
	return ret, observed

""" # Used before use of dicts.
def mutationObserved(name,X):
	for mutation in X:
		if mutation[0] == name:
			if mutation[1]:
				return True
	return False
"""

def calcProbForDataPoint2(tree,X): # X is a datapoint
	""" Should probably use reverse order traversal for this. The use dynamic 
		programming to speed up process. """
	ret = 1
	observed = False
	#print "l1",tree
	if(tree.is_leaf()):
		#print "leaf"
		return calcProbForLeaf(tree,X)

	"""
	if (allChildrenAreLeaves(tree)):
		print "This tree has only leaves as children"
		#tree.add_feature("Searched",True)
		return calcProbForSubtree(tree,X)
	"""
	
	for node in tree.children:
		#print "child"
		tmp, tmpObs = calcProbForDataPoint2(node,X)
		ret *= tmp
		observed = observed or tmpObs
		#if not (allChildrenAreLeaves(node)):
		#print "This tree has only leaves as children", node
		#return calcProbForDataPoint2(node)

	#print "l2",tree, "r1 ",ret, observed
	if (X[tree.name]):
		#print tree.name," was observed"
		ret *= tree.dist*tree.Px
	else:
		if (observed):
			#print "Alpha was observed"
			ret *= tree.dist*(1-tree.Px)
		else: 
			#print "nothing was observed"
			ret *= ((1-tree.dist) + (tree.dist*(1-tree.Px)))
	#print "r2 ",ret
	#calcProbForDataPoint2(node,X)
	return ret, observed

def likelyhoodOfX(tree,X):
	tmp, observed = calcProbForDataPoint2(tree,X)
	#print "Obeservation ", X, " in tree ", tree, " is this likley ", tmp
	return tmp

def logLikelyhood(tree,data):
	ret = 0
	for i in range(len(data)):
		ret += math.log(likelyhoodOfX(tree,data[i]))
	return ret


def calcProbForLeafAndZ(tree,X,Zu,Zvalue):
	ret = 1
	#global epsilonZ
	#global epsilonX
	observed = False
	if (X[tree.name]): # If observed
		#print tree.name, Zu, Zvalue
 	 	if (tree.name == Zu): 
			if(Zvalue):
				ret *= tree.dist * tree.Px
			else:
				ret = tree.Ez # constant
		else: 
			ret *= tree.dist * tree.Px
		observed = True
	else:
		if (tree.name == Zu): 
			if(Zvalue):
				ret *= tree.Ex
				observed = True  # Check
			else:
				ret = 1-tree.dist
		else:
			ret *= ((1-tree.dist) + (tree.dist*(1-tree.Px)))
	#print tree, observed, " is this likley ", ret
	return ret, observed

def calcProbForDataPointAndZ(tree,X,Zu,Zvalue):
	ret = 1 
	observed = False
	if(tree.is_leaf()):
		return calcProbForLeafAndZ(tree,X,Zu,Zvalue)
	for node in tree.children:
		tmp, tmpObs = calcProbForDataPointAndZ(node,X,Zu,Zvalue)
		ret *= tmp
		observed = observed or tmpObs
	if X[tree.name]:
		if (tree.name == Zu and not Zvalue):
			ret *= tree.Ex # Check 
		else:
			ret *= tree.dist*tree.Px
	else:
		if (observed):
			if (tree.name == Zu and not Zvalue):
				ret *= tree.Ex # Check 
			else:
				ret *= tree.dist*(1-tree.Px)
		else: 
			if (tree.name == Zu and Zvalue):
				ret *= tree.dist*(1-tree.Px)
			elif (tree.name == Zu and not Zvalue):
				ret *= 1-tree.dist
			else:
				ret *= ((1-tree.dist) + (tree.dist*(1-tree.Px)))
	return ret, observed

def calcProbForLeafZandZp(tree,X,Zu,Zp,Zvalue,Zpvalue):
	Zswitch = False
	ret = 0
	#global epsilonZ
	#global epsilonX
	observed = False
	if (X[tree.name]): # If observed
		#print tree.name, Zu, Zvalue
		if (tree.name == Zu): 
			if(tree.up.name == Zp):
				if(Zvalue and not Zpvalue):
					ret = tree.Ez
				elif(Zvalue and Zpvalue):
					ret = tree.dist * tree.Px
				elif(not Zvalue and Zpvalue):
					ret = tree.Ex
				elif(not Zvalue and not Zpvalue):
					ret = tree.Ex  
			else:
				raw_input("ERROR")
		else: 
			ret *= tree.dist * tree.Px
		observed = True
	else:
		if (tree.name == Zu): 
			if(tree.up.name == Zp):
				if(Zvalue and not Zpvalue):
					ret = 1-tree.Px
					observed = True
				elif(Zvalue and Zpvalue):
					ret = 1-tree.Px
					observed = True
				elif(not Zvalue and Zpvalue):
					ret = 1-tree.dist
				elif(not Zvalue and not Zpvalue):
					ret = 1-tree.Ez # Check
			else:
				raw_input("ERROR")
		else:
			ret *= ((1-tree.dist) + (tree.dist*(1-tree.Px)))
	#print tree, observed, " is this likley ", ret
	return ret, observed

def calcProbForDataPointZandZp(tree,X,Zu,Zp,Zvalue,Zpvalue):
	ret = 1 
	observed = False
	if(tree.is_leaf()):
		return calcProbForLeafZandZp(tree,X,Zu,Zvalue,Zp,Zpvalue)

	for node in tree.children:
		tmp, tmpObs = calcProbForDataPointAndZ(node,X,Zu,Zvalue)
		ret *= tmp
		observed = observed or tmpObs

	if X[tree.name]:
		if (tree.name == Zu):
			if(tree.up.name == Zp):
				if(Zvalue and not Zpvalue):
					ret = tree.Ez
				elif(Zvalue and Zpvalue):
					ret = tree.dist * tree.Px
				elif(not Zvalue and Zpvalue):
					ret = tree.Ex
				elif(not Zvalue and not Zpvalue):
					ret = tree.Ex  
			else:
				raw_input("ERROR")
		else:
			ret *= tree.dist*tree.Px
		observed = True
	else:
		#if (observed):
		if (tree.name == Zu):
			if(tree.up.name == Zp):
				if(Zvalue and not Zpvalue):
					ret = 1-tree.Px
					observed = True
				elif(Zvalue and Zpvalue):
					ret = 1-tree.Px
					observed = True
				elif(not Zvalue and Zpvalue):
					ret = 1-tree.dist
				elif(not Zvalue and not Zpvalue):
					ret = 1-tree.Ez # Check
		else:
			ret *= tree.dist*(1-tree.Px)
		"""		
		else: 
			if (tree.name == Zu and Zvalue):
				ret *= tree.dist*(1-tree.Px)
			elif (tree.name == Zu and not Zvalue):
				ret *= 1-tree.dist
			else:
				ret *= ((1-tree.dist) + (tree.dist*(1-tree.Px)))
		"""
	return ret, observed

def likelyhoodOfXandZ(tree,X,Z,Zvalue):
	tmp, observed = calcProbForDataPointAndZ(tree,X,Z,Zvalue)
	#print "Obeservation ", X, " in tree ", tree, " is this likley ", tmp
	return tmp		

def likelyhoodOfXZandZp(tree,X,Zu,Zvalue,Zpvalue):
	Zp = tree.search_nodes(Zu).up.name
	tmp, observed = calcProbForDataPointZandZp(tree,X,Z,Zp,Zvalue,Zpvalue)
	#print "Obeservation ", X, " in tree ", tree, " is this likley ", tmp
	return tmp
"""
def Aarc(tree,data,arc,a,b,p_x_t):
	ret = 0
	for X in data:
		ret += likelyhoodOfXZandZp(tree,X,arc,a,b)*p_x_t
	return ret

def Barc(tree,data,a,b,p_x_t):
	ret = 0
	for X in data:
		ret += likelyhoodOfXZ(tree,X,arc,a)*p_x_t
	return ret	

def tmp2(tree,data,arc,a,b,p_x_t):
	ret = 0 
	tmp = Aarc(tree,data,arc,ta,tb,p_x_t)
	tmpA = 0
	for ta in range(0,1):
		for tb in range(0,1):
			tmpA += Aarc(tree,data,arc,ta,tb,p_x_t)
	return tmp / tmpA

def tmp4(tree,data,arc,a): # Divide on positive and negative.
	ret = 0 
	tmpA = 0
	tmp = Barc(tree,data,arc,a,p_x_t)
	for ta in range(0,1):
		for tt in range(0,1):
			tmpA += Barc(tree,data,arc,ta,tt,p_x_t)
	return tmp/tmpA

def Q(tree,data):
	tmp5 = likelyhoodOfX(tree,data)
	for arc in tree.iter_descendants():
		tmp, tmp2,tmp3.tmp4 = 0,0,0,0
		for a in range(0,1):
			for b in range(0,1):
				t1p1 = likelyhoodOfXZandZp(tree,i,arc,a,b)*tmp5 
				t1p2 = math.log(t1p1/tmp2(tree,data,arc,a,b,tmp5)) # include log
				t2p1 = likelyhoodOfXandZ(tree,i,arc,a)*tmp5
				t2p2 = math.log(tmp2(tree,data,arc,a,tmp5))	# include log
				tmptotal = (t1p1 * t1p2) + (t2p1 * t2p2)
		arcW += tmptotal
		print arcW
	return
"""
"""
def createDataFunc(tree,dataSet,observed= True): # Returns sets of mutations
	if (observed):
		if tree.is_root():
			dataSet.append((tree.name,True))  # UNSURE, appending root "mutation" to tumors. 
			for node in tree.children:
				tmpPz = tree.get_distance(node) # Distance to child	
				if (np.random.uniform(0,1) <= tmpPz): 
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
				tmpPz = tree.get_distance(node) # Distance to child	
				if (np.random.uniform(0,1) <= tmpPz): 
					createDataFunc(node,dataSet,True)
				else:
					createDataFunc(node,dataSet,False)
	else:
		dataSet.append((tree.name,False))
		for node in tree.children:
			createDataFunc(node,dataSet,False)
	return 
"""
#def calcProbForNode(node):
	#