class TreeNode:
    def __init__(self, key, parentNode = None, edgeType = None):
        self.key = key
        self.parent = parentNode
        self.edgeType = edgeType
        self.children = dict()

    def __str__(self):
        return (self.key + '---' + str(self.edgeType))

    def addChild(self, childNode):
        if childNode.key in self.children:
            raise Exception("node {} already has {} child, ignore".format(self, childNode))
        self.children[childNode.key] = childNode

    def addParent(self, parentNode, edgeType):
        if self.parent is not None:
            raise Exception("node {} already has a parent {}".format(self, self.parent))
        self.parent = parentNode
        self.edgeType = edgeType

    def childKeys(self):
        for k in self.children:
            yield k

    def childrenIter(self):
        for k in self.children:
            yield self.children[k]

    def numChildren(self):
        return len(self.children)

    def nodeName(self):
        return self.key

    def nodeType(self):
        return self.edgeType

class Tree:
    def __init__(self):
        self.__nodeTable = dict()
        self.__tree = []

    def pushEdge(self, startKey, endKey, edgeType):
        parentNode = TreeNode(startKey)
        childNode = TreeNode(endKey)
        if startKey in self.__nodeTable:
            parentNode = self.__nodeTable[startKey]
        if endKey in self.__nodeTable:
            childNode = self.__nodeTable[endKey]
        parentNode.addChild(childNode)
        childNode.addParent(parentNode, edgeType)
        self.__nodeTable[startKey] = parentNode
        self.__nodeTable[endKey] = childNode
        # print("---> push edge: [{}] --- {} ---> [{}]".format(startKey, edgeType, endKey))

    def getRoot(self):
        if "ROOT" not in self.__nodeTable:
            raise Exception("No root not found!")
        return self.__nodeTable["ROOT"]

    def printTree(self, startspace = 0, startNode = "ROOT"):
        if startNode not in self.__nodeTable:
            raise Exception("Cannot find {} in the tree\n{}".format(startNode, self.__nodeTable))
        node = self.__nodeTable[startNode]
        prefix = "    " * startspace
        # print(prefix + str(node))
        self.__tree.append(prefix + str(node))
        for key in node.childKeys():
            self.printTree(startspace + 1, key)

    def getTree(self):
        return self.__tree



# tree = Tree()
# tree.pushEdge("children", "happy", "amod")
# tree.pushEdge("like", "children", "nsubj")
# tree.pushEdge("ROOT", "like", "root")
# tree.pushEdge("play", "to", "aux")
# tree.pushEdge("like", "play", "xcomp")
# tree.pushEdge("play", "with", "prep")
# tree.pushEdge("friends", "their", "poss")
# tree.pushEdge("with", "friends", "pobj")
# tree.pushEdge("like", ".", "punc")

# tree.printTree()
