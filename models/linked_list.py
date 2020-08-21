class LLNode(object):
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

    def __str__(self) -> bool:
        return str(self.data)

class LinkedList(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __len__(self):
        return self.length

    def pushHead(self, data):
        newNode = LLNode(data)
        self.length += 1
        if not self.head:
            self.head = newNode
            self.tail = newNode
        else:
            newNode.next = self.head
            self.head.prev = newNode
            self.head = newNode

    def pushTail(self, data):
        newNode = LLNode(data)
        self.length += 1
        if not self.tail:
            self.head = newNode
            self.tail = newNode
        else:
            newNode.prev = self.tail
            self.tail.next = newNode
            self.tail = newNode

    def popHead(self):
        if not self.head:
            return None
        self.length -= 1
        nextNode = self.head.next
        headNode = self.head
        if not nextNode:
            self.tail = None
            self.head = None
            if self.length != 0:
                print("Warning: something wrong, linked list empty but length = {}".format(self.length))
                self.length = 0
        else:
            self.head = nextNode
            nextNode.prev = None
        headNode.next = None
        return headNode

    def popTail(self):
        if not self.tail:
            return None
        self.length -= 1
        prevNode = self.tail.prev
        tailNode = self.tail
        if not prevNode:
            self.tail = None
            self.head = None
            if self.length != 0:
                print("Warning: something wrong, linked list empty but length = {}".format(self.length))
                self.length = 0
        else:
            self.tail = prevNode
            prevNode.next = None
        tailNode.prev = None
        return tailNode

    def iterateForward(self):
        node = self.head
        while node:
            yield node
            node = node.next

    def __str__(self):
        result = "# "
        for node in self.iterateForward():
            result += (str(node) + " <-> ")
        result += '#\n'
        return result

    def __len__(self):
        return self.length
