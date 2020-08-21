from malt_parser import MaltParser
from tokenize import Tokenize
from database import ruleTable, Database

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

    def getToLoc(self):
        rootNode = self.tree.getRoot()
        toToNode = self.findEdgeNode(rootNode, "to-loc")
        if toToNode is None:
            toToNode = self.findEdgeNode(rootNode, "to-city")
            if toToNode is None:
                return None
        nameNode = self.findEdgeNode(toToNode, "<var>name")
        if nameNode is None:
            raise Exception("<var>name not exist while to-loc node is represent")
        return nameNode.nodeName()

    def getBusName(self):
        rootNode = self.tree.getRoot()
        busToNode = self.findEdgeNode(rootNode, "lsubj")
        if busToNode is None:
            return None
        nameNode = self.findEdgeNode(busToNode, "<var>name")
        if nameNode is None:
            # print("[WARN] <var>name not exist while lsubj node is represent")
            return None
        return nameNode.nodeName()

    def getToTime(self):
        rootNode = self.tree.getRoot()
        toTimeToNode = self.findEdgeNode(rootNode, "arrive-time")
        if toTimeToNode is None:
            return None
        nameNode = self.findEdgeNode(toTimeToNode, "<var>time-hour")
        if nameNode is None:
            raise Exception("<var>time-hour not exist while arrive-time node is represent")
        return nameNode.nodeName()

    def getQueryTheme(self):
        rootNode = self.tree.getRoot()
        queryToNode = self.findEdgeNode(rootNode, "which-query")
        if queryToNode is not None:
            return "which"
        queryToNode = self.findEdgeNode(rootNode, "time-query")
        if queryToNode is not None:
            return "time"
        return None

    def parse(self):
        self.fromLocation = self.getFromLoc()
        self.toLocation = self.getToLoc()
        self.busName = self.getBusName()
        self.toTime = self.getToTime()
        self.queryTheme = self.getQueryTheme()

    def answer(self):
        if self.queryTheme == 'time':
            return Database().getTimeFromBusFromToLocation(self.busName, self.fromLocation, self.toLocation)
        if self.queryTheme == 'which':
            if self.fromLocation is not None and self.toLocation is not None:
                return Database().getBusNameFromToLocation(self.fromLocation, self.toLocation)
            elif self.toLocation is not None and self.toTime is not None:
                return Database().getBusFromDtimeAndToLocation(self.toTime, self.toLocation)
            elif self.fromLocation is None and self.toLocation is not None:
                return Database().getBusNameToLocation(self.toLocation)
            elif self.fromLocation is not None and self.toLocation is None:
                return Database().getBusNameFromLocation(self.fromLocation)





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









questions = ["Thời gian xe bus B3 đi từ Đà Nẵng đến Hồ Chí Minh ?",
             "Những xe nào đi từ Đà nẵng đến thành phố Huế ?",
             "Xe bus nào đến thành phố Hồ Chí Minh ?",
             "Những xe nào xuất phát từ thành phố Hồ Chí Minh ?",
             "Những xe bus nào đi đến Huế ?",
             "Xe bus nào đến thành phố Huế lúc 8:30HR ?"]

for question in questions:
    string = Tokenize(question).parse()
    parser = MaltParser(ruleTable)
    tree = parser.parse(string)
    # tree.printTree()
    query = QueryLogic(tree)
    query.parse()
    print("Question: {}".format(question))
    print("Answer: {}".format(query.answer()))

