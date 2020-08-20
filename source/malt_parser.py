from stack import Stack
from queue import Queue
from tree import Tree
from tokenize import Tokenize
from database import ruleTable

class MaltParser:
    def __init__(self, relationTable):
        self.relationTable = relationTable

    def __getRelation(self, item1, item2):
        value1 = item1
        value2 = item2
        print("get relation {} --- {}".format(item1, item2))
        if item1[0:9] in set(("<VAR-LOC>", "<VAR-TIM>", "<VAR-BUS>")):
            value1 = item1[9:]
            item1 = item1[0:9]
        if item2[0:9] in set(("<VAR-LOC>", "<VAR-TIM>", "<VAR-BUS>")):
            value2 = item2[9:]
            item2 = item2[0:9]

        if item1 not in self.relationTable:
            return None
        if item2 not in self.relationTable[item1]:
            return None
        return value1, value2, self.relationTable[item1][item2]

    def parse(self, strlst):
        tree = Tree()
        stack = Stack()
        queue = Queue()
        rootWord = None

        if strlst is None or len(strlst) <= 0:
            raise Exception("invalid string list: {}".format(strlst))

        for  s in strlst:
            queue.enqueue(s)

        stack.push("ROOT")

        while(len(queue) > 0):
            print("=================================")
            print(stack)
            print(queue)
            print("=================================")
            rItem = queue.getHead()
            lItem = stack.getHead()
            if rItem is None or lItem is None:
                raise Exception("rItem is {} and lItem is {}".format(rItem, lItem))

            larc = self.__getRelation(rItem, lItem)
            if larc is not None:
                tree.pushEdge(*larc)
                stack.pop()
                continue

            rarc = self.__getRelation(lItem, rItem)
            if rarc is not None:
                tree.pushEdge(*rarc)
                if "<var>" not in rarc[2]:
                    stack.push(queue.dequeue())
                    if rarc[2] == "root":
                        rootWord = rItem
                else:
                    queue.dequeue()
                continue

            if rootWord is not None:
                rootRelation = self.__getRelation(rootWord, rItem)
                if rootRelation is not None:
                    while len(stack) > 2:
                        stack.pop()
                    tree.pushEdge(*rootRelation)
                    stack.push(queue.dequeue())
                    continue

            stack.push(queue.dequeue())
        return tree

questions = ["Xe bus nào đến thành phố Huế lúc 20:00HR ?",
             "Thời gian xe bus B3 đi từ Đà Nẵng đến Huế ?",
             "Xe bus nào đến thành phố Hồ Chí Minh ?",
             "Những xe bus nào đi đến Huế ?",
             "Những xe nào xuất phát từ thành phố Hồ Chí Minh ?",
             "Những xe nào đi từ Đà nẵng đến thành phố Hồ Chí Minh ?"]

for question in questions:
    string = Tokenize(question).parse()
    parser = MaltParser(ruleTable)
    parser.parse(string).printTree()
