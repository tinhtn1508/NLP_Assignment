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
        fromToNode = self.findEdgeNode(rootNode, "from-loc")
        if fromToNode is None:
            return None
        nameNode = self.findEdgeNode(fromToNode, "<var>name")
        if nameNode is None:
            raise Exception("<var>name not exist while from-loc node is represent")
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





class LogicalFormParser:
    def __init__(self, tree):
        if tree is None:
            raise Exception("input None tree!!!")
        if tree.getRoot() is None:
            raise Exception("input None root node!!!")
        self.varCount = {}
        self.tree = tree

    def findEdgeNode(self, node, edgeName):
        if node is None or node.numChildren() == 0: None
        for cnode in node.childrenIter():
            if cnode.edgeType == edgeName:
                return cnode
            lowerResult = self.findEdgeNode(cnode, edgeName)
            if lowerResult is not None: return lowerResult
        return None

    def chooseVarName(self, varType):
        c = varType[0].lower()
        if c < 'a' or c > 'z': c = 'n'
        if c in self.varCount:
            self.varCount[c] += 1
        else:
            self.varCount[c] = 1
        return c + str(self.varCount[c])

    def parseAllChild(self, node):
        if node is None:
            raise Exception("input node is None!!!")
        describe = []
        for cnode in node.childrenIter():
            nodeType = cnode.nodeType()
            nodeName = cnode.nodeName()
            if "<var>" == nodeType[0:5]:
                obj = nodeType[5:].upper()
                nodeName = nodeName.upper()
                varName = self.chooseVarName(nodeName)
                describe.append("<{} {} {}>".format(obj, varName, nodeName))
            elif "lsubj" == nodeType:
                describe.append("({} {})".format(nodeName.upper(), self.chooseVarName(nodeName)))
            elif "plural" == nodeType:
                describe.insert(0, "PLURAL")
            else:
                describe.append(cnode.nodeName().upper())

            describe.append(self.parseAllChild(cnode))

        if len(describe) == 0: return ""
        return "".join(describe)

    def parseRootBranch(self, node, var):
        if node is None:
            raise Exception("input node is None!!!")
        nodeType = node.nodeType().upper()
        return "({} {} {})".format(nodeType, var, self.parseAllChild(node))

    def parse(self):
        varCount = { 'e': 1 }
        describe = []
        lform = "(∃ e1: (&\n{}\n))"

        rootNode = self.tree.getRoot()
        mainVerbNode = self.findEdgeNode(rootNode, "root")
        if mainVerbNode is None:
            raise Exception("There is no main verb in this tree!\n{}".format(self.tree.printTree()))
        mainVerb = mainVerbNode.nodeName().upper()
        describe.append("({} e1)".format(mainVerb))

        for cnode in mainVerbNode.childrenIter():
            describe.append(self.parseRootBranch(cnode, "e1"))

        return lform.format("    " + ("\n    ").join(describe))









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
    logical = LogicalFormParser(tree)
    print(logical.parse())
    print("Question: {}".format(question))
    print("Answer: {}".format(query.answer()))

