from malt_parser import MaltParser
from tokenize import Tokenize
from database import ruleTable

class QueryLogic:
    def __init__(self, tree):
        if tree is None:
            raise Exception("input None tree!!!")
        if tree.getRoot() is None:
            raise Exception("input None root node!!!")
        # print("parse logical form for tree:\n{}".format(tree.printTree()))
        self.tree = tree
        self.fromLocation = None
        self.toLocation = None
        self.fromTime = None
        self.toTime = None
        self.busName = None
        self.queryTheme = None
        self.pluralQuery = False

    def findEdgeNode(self, node, edgeName):
        if node is None or node.numChildren() == 0: None
        for cnode in node.childrenIter():
            if cnode.edgeType == edgeName:
                return cnode
            lowerResult = self.findEdgeNode(cnode, edgeName)
            if lowerResult is not None: return lowerResult
        return None

    def getFromLoc(self):
        rootNode = self.tree.getRoot()
        fromToNode = self.findEdgeNode(rootNode, "from-to")
        if fromToNode is None:
            return None
        nameNode = self.findEdgeNode(fromToNode, "<var>name")
        if nameNode is None:
            raise Exception("<var>name not exist while from-to node is represent")
        return nameNode.nodeName()

    def parse(self):
        self.fromLocation = self.getFromLoc()
        print(self.fromLocation)


# class LogicalFormParser:
#     def __init__(self, tree):
#         if tree is None:
#             raise Exception("input None tree!!!")
#         if tree.getRoot() is None:
#             raise Exception("input None root node!!!")
#         # print("parse logical form for tree:\n{}".format(tree.printTree()))
#         self.tree = tree

#     def queryLogic(self):



    # def parse(self):









questions = ["Xe bus nào đến thành phố Huế lúc 20:00HR ?",
             "Thời gian xe bus B3 đi từ Đà Nẵng đến Huế ?",
             "Xe bus nào đến thành phố Hồ Chí Minh ?",
             "Những xe bus nào đi đến Huế ?",
             "Những xe nào xuất phát từ thành phố Hồ Chí Minh ?",
             "Những xe nào đi từ Đà nẵng đến thành phố Hồ Chí Minh ?"]

for question in questions:
    string = Tokenize(question).parse()
    parser = MaltParser(ruleTable)
    tree = parser.parse(string)
    tree.printTree()
    query = QueryLogic(tree)
    query.parse()

