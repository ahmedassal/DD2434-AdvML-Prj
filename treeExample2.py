import numpy as np
N = 10
#1,np.random.unifrom(0,1)
class node(object):
    def __init__(self, Z,X, children = []):
        self.Z = Z
        self.X = X
        self.children = children

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.Z)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __repr__(self):
        return '<tree node representation>'



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
        if (np.random.uniform(0.1,1.0) >= 0.5): # COMMENT, see (7)
            return 1
        # See eq. (8)
        return 0
        
    else: #small probability of childZ
        return 0
def addChild(parent,child):
    print parent.children
    #parent.children.append(child)

#for i in range(N):
rootZ = 1 # Given in article
tmpX = probXGenerator(1)
root = node(rootZ,tmpX)
tmpZ = probZGenerator(rootZ)
tmpZ = probZGenerator(rootZ)
tmpX = probXGenerator(tmpZ)
root.children = [node(tmpZ,tmpX)]
addChild(root,node(tmpZ,tmpX))
"""
>>> root = node('grandmother')
>>> root.children = [node('daughter'), node('son')]
>>> root.children[0].children = [node('granddaughter'), node('grandson')]
>>> root.children[1].children = [node('granddaughter'), node('grandson')]
"""
#root.children[0].children = [node(1,0), node(1,0)]
#root.children[1].children = [node(0,0), node(0,0)]


print root
