from linked_list import LinkedList

class Queue(LinkedList):
    def __init__(self):
        super().__init__()

    def enqueue(self, data):
        self.pushHead(data)
        return self

    def dequeue(self):
        if len(self) == 0:
            return None
        node = self.popTail()
        return node.data

    def getHead(self):
        return self.tail.data
