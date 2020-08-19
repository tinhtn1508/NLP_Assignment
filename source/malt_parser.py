from stack import Stack
from queue import Queue
from tree import Tree

class MaltParser:
    def __init__(self, relationTable):
        self.relationTable = relationTable
        self.tree = Tree()
        self.stack = Stack()
        self.queue = Queue()

    def __getRelation(self, item1, item2):
        if item1 not in self.relationTable:
            return None
        if item2 not in self.relationTable[item1]:
            return None
        return self.relationTable[item1][item2]

    def parse(self, strlst):
        if strlst is None or len(strlst) <= 0:
            raise Exception("invalid string list: {}".format(strlst))

        for  s in strlst:
            self.queue.enqueue(s)

        self.stack.push("ROOT")

        while(len(self.queue) > 0):
            print("=================================")
            print(self.stack)
            print(self.queue)
            print("=================================")
            rItem = self.queue.getHead()
            lItem = self.stack.getHead()
            if rItem is None or lItem is None:
                raise Exception("rItem is {} and lItem is {}".format(rItem, lItem))

            larc = self.__getRelation(rItem, lItem)
            if larc is not None:
                self.tree.pushEdge(rItem, lItem, larc)
                self.stack.pop()
                continue

            rarc = self.__getRelation(lItem, rItem)
            if rarc is not None:
                self.tree.pushEdge(lItem, rItem, rarc)

            self.stack.push(self.queue.dequeue())
        self.tree.printTree()


table = {
    "children": { "happy": "amod" },
    "like": { "children": "nsubj", "play": "xcomp", ".": "punc" },
    "ROOT": { "like": "root" },
    "play": { "to": "aux", "with": "prep" },
    "friends": {"their": "poss"},
    "with": {"friends": "pobj"},
}

string = "happy children like to play with their friends"
parser = MaltParser(table)
parser.parse(string.split())
