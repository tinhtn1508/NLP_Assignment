from linked_list import LinkedList

class Stack(LinkedList):
    def __init__(self):
        super().__init__()

    def push(self, data):
        self.pushHead(data)
        return self

    def pop(self):
        if len(self) == 0:
            return None
        node = self.popHead()
        return node.data

    def getHead(self):
        return self.head.data
