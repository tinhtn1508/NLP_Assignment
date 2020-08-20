from stack import Stack
from queue import Queue
from tree import Tree
from tokenize import Tokenize

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


# table = {
#     "children": { "happy": "amod" },
#     "like": { "children": "nsubj", "play": "xcomp", ".": "punc" },
#     "ROOT": { "like": "root" },
#     "play": { "to": "aux", "with": "prep" },
#     "friends": {"their": "poss"},
#     "with": {"friends": "pobj"},
# }

# string = "happy children like to play with their friends ."
# parser = MaltParser(table)
# parser.parse(string.split())


# table = {
#     "ROOT": { "den": "root" },
#     "den": { "nao": "which-query", "thanh_pho": "to-loc", "luc": "arrive-time" },
#     "nao": { "xe_bus": "lsubj" },
#     "thanh_pho": { "<VAR-LOC>": "<var>name" },
#     "luc": { "<VAR-TIM>": "<var>time-hour" },
# }

# string = Tokenize('Xe bus nào đến thành phố Huế luc 20:00HR ?').parse()
# print(string)
# parser = MaltParser(table)
# parser.parse(string)

table = {
    "ROOT": { "den": "root", "di": "root", "xuat_phat": "root"},
    "xuat_phat": {"nao": "which-query", "tu": "from-to"},
    "tu": {"thanh_pho": "to_loc", "<VAR-LOC>": "<var>name"},
    "den": { "nao": "which-query", "thanh_pho": "to-loc", "luc": "arrive-time", "<VAR-LOC>": "<var>name"},
    "di": {"nao": "which-query", "den": "to-city", "tu": "from-to"},
    "nao": { "xe_bus": "lsubj", "xe": "lsubj", "nhung": "plural"},
    "thanh_pho": { "<VAR-LOC>": "<var>name" },
    "luc": { "<VAR-TIM>": "<var>time-hour" },
}

string = Tokenize('Những xe nào đi từ Đà nẵng đến thành phố Hồ Chí Minh').parse()
print(string)
parser = MaltParser(table)
parser.parse(string).printTree()
