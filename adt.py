#!/usr/bin/python3

import unittest as ut
import random

class heap:

    class Node:
        def __init__(self, val, priority = None):
            self.val = val
            self.priority = priority

        @staticmethod
        def unpack(arg):
            try:
                return heap.Node(*arg)
            except:
                return heap.Node(arg)

        def __repr__(self):
            return str( (self.val, self.priority) )

    def __init__(self, arr = []):
        self.arr = [self.Node.unpack(arg) for arg in arr]

        for root in range( (len(arr) - 2) // 2, -1, -1):
            self.__siftDown(root)

    def push(self, elt, priority = None):
        self.arr.append(self.Node(elt, priority))
        self.__siftUp()

    def pop(self):
        tmp = self.arr[0].val
        self.arr[0] = self.arr[-1]
        del self.arr[-1]
        self.__siftDown()
        return tmp

    def pushpop(self, elt, priority = None):
        tmp = self.arr[0].val
        self.arr[0] = self.Node(elt, priority)
        self.__siftDown()
        return tmp

    def peek(self):
        return self.arr[0].val

    #should be overwritten in subclass
    def comp(self, parent_priority, child_priority):
        """
        This function returns True if parent and child are in strict heap order, False otherwise
        None should be considered to be the lowest priority element (infinity in minheap, -infinity in max heap)

        Args:
            parent_priority (int): priority of parent element
            child_priority  (int): priority of child element

        Returns:
            bool: result of comparison
        """
        return parent_priority is None and child_priority is None or child_priority is None

    def set_priority(self, i, new_priority):
        comp = self.comp(self.arr[i].priority, new_priority) #would old priority be parent of new prioirty
        self.arr[i].priority = new_priority
        if comp:
            self.__siftDown(i)
        else:
            self.__siftUp(i)

    def __siftUp(self, child = -1):
        if child < 0:
            child += len(self.arr)

        while child > 0:
            root = (child - 1) // 2

            if self.comp(self.arr[child].priority, self.arr[root].priority): #if child should be a parent of it's parent
                self.arr[child], self.arr[root] = self.arr[root], self.arr[child]
                child = root
            else:
                break

    def __siftDown(self, root = 0):
        swap = root

        while True:
            left = root * 2 + 1
            for child in (left, left + 1):
                if child < len(self.arr) and self.comp(self.arr[child].priority, self.arr[swap].priority): #if child should be a parent of swap
                    swap = child

            if swap == root:
                break

            self.arr[swap], self.arr[root] = self.arr[root], self.arr[swap]

            root = swap

class maxheap(heap):

    def comp(self, pp, cp):
        if pp is None or cp is None:
            return super().comp(pp, cp)
        return pp > cp

class minheap(heap):

    def comp(self, pp, cp):
        if pp is None or cp is None:
            return super().comp(pp, cp)
        return pp < cp

class MaxHeapTester(ut.TestCase):

    def test_init(self):
        self.assertEqual(maxheap().arr, [])
        l = maxheap([random.randint(0, 50) for i in range(1000)]).arr
        self.assertTrue(self.is_maxheap(l))
        l = maxheap([(random.randint(0, 50), random.randint(0, 50)) for i in range(1000)]).arr
        self.assertTrue(self.is_maxheap(l))


    def test_push(self):
        h = maxheap()
        for i in range(1000):
            h.push(random.randint(0, 50), random.randint(0, 50))
        self.assertTrue(self.is_maxheap(h.arr))

    def test_pop(self):
        h = maxheap([(random.randint(0, 50), random.randint(0, 50)) for i in range(1000)])
        for i in range(1000):
            val = max(h.arr, key = lambda x: x.priority if x.priority is not None else -float('inf')).val
            self.assertEqual(val, h.pop())

    def test_pushpop(self):
        h = maxheap([(random.randint(0, 50), random.randint(0, 50)) for i in range(1000)])
        for i in range(1000):
            val = max(h.arr, key = lambda x: x.priority if x.priority is not None else -float('inf')).val
            self.assertEqual(val, h.pushpop(random.randint(0, 50), random.randint(0, 50)))
        self.assertTrue(self.is_maxheap(h.arr))

    def test_peek(self):
        h = maxheap([(random.randint(0, 50), random.randint(0, 50)) for i in range(1000)])
        for i in range(1000):
            self.assertEqual(h.peek(), h.pop())

    @staticmethod
    def is_maxheap(l, root = 0):
        left = root * 2 + 1
        for child in (left, left + 1):
            if child < len(l):
                cp = l[child].priority if l[child].priority is not None else -float('inf')
                pp = l[root].priority if l[root].priority is not None else -float('inf')
                if cp > pp or not MaxHeapTester.is_maxheap(l, child):
                    return False

        return True

class MinHeapTester(ut.TestCase):

    def test_init(self):
        self.assertEqual(minheap().arr, [])
        l = minheap([random.randint(0, 50) for i in range(1000)]).arr
        self.assertTrue(self.is_minheap(l))
        l = minheap([(random.randint(0, 50), random.randint(0, 50)) for i in range(1000)]).arr
        self.assertTrue(self.is_minheap(l))

    def test_push(self):
        h = minheap()
        for i in range(1000):
            h.push(random.randint(0, 50), random.randint(0, 50))
        self.assertTrue(self.is_minheap(h.arr))

    def test_pop(self):
        h = minheap([(random.randint(0, 50), random.randint(0, 50)) for i in range(1000)])
        for i in range(1000):
            val = min(h.arr, key = lambda x: x.priority if x.priority is not None else float('inf')).val
            self.assertEqual(val, h.pop())

    def test_pushpop(self):
        h = minheap([(random.randint(0, 50), random.randint(0, 50)) for i in range(1000)])
        for i in range(1000):
            val = min(h.arr, key = lambda x: x.priority if x.priority is not None else float('inf')).val
            self.assertEqual(val, h.pushpop(random.randint(0, 50), random.randint(0, 50)))
        self.assertTrue(self.is_minheap(h.arr))

    def test_peek(self):
        h = minheap([(random.randint(0, 50), random.randint(0, 50)) for i in range(1000)])
        for i in range(1000):
            self.assertEqual(h.peek(), h.pop())

    @staticmethod
    def is_minheap(l, root = 0):
        left = root * 2 + 1
        for child in (left, left + 1):
            if child < len(l):
                cp = l[child].priority if l[child].priority is not None else float('inf')
                pp = l[root].priority if l[root].priority is not None else float('inf')
                if cp < pp or not MinHeapTester.is_minheap(l, child):
                    return False

        return True

class doublyLL:

    class Node:
        def __init__(self, val, next = None, prev = None):
            self.val = val
            self.next = next
            self.prev = prev

    def __init__(self, arr = []):
        if not len(arr):
            self.head, self.tail = None, None
            self.size = 0
        else:
            self.head = self.Node(arr[0])
            prev = self.head

            for elt in arr[1:]:
                curr = self.Node(elt, prev=prev)
                prev.next = curr
                prev = curr

            self.tail = prev
            self.size = len(arr)

    def insert(self, elt, pos = None):
        if not self.size:
            self.head = self.Node(elt)
            self.tail = self.head
        elif pos is None:
            tmp = self.Node(elt, prev=self.tail)
            self.tail.next = tmp
            self.tail = tmp
        else:
            curr = self.__get(pos)
            tmp = self.Node(elt, next=curr, prev=curr.prev)
            if curr.prev is not None:
                curr.prev.next = tmp
            else:
                self.head = tmp
            curr.prev = tmp

        self.size += 1

    def remove(self, pos = -1):
        if not self.size:
            return
        if self.head == self.tail:
            tmp = self.head
            self.head, self.tail = None, None
        else:
            tmp = self.__get(pos)
            if tmp == self.head:
                self.head = self.head.next
                self.head.prev = None
            elif tmp == self.tail:
                self.tail = self.tail.prev
                self.tail.next = None
            else:
                tmp.next.prev = tmp.prev
                tmp.prev.next = tmp.next

        self.size -= 1
        return tmp.val

    def __len__(self):
        return self.size

    def __str__(self):
        arr = []

        curr = self.head
        while curr is not None:
            arr.append(curr.val)
            curr = curr.next

        return str(arr)

    def __get(self, pos):
        if pos < 0:
            pos += self.size

        if pos > self.size // 2:
            curr = self.tail

            for i in range(self.size - 1, pos, -1):
                curr = curr.prev

            return curr
        else:
            curr = self.head

            for i in range(pos):
                curr = curr.next

            return curr

class DoublyLLTester(ut.TestCase):

    def test_init(self):
        ll = doublyLL()
        self.assertEqual(ll.head, ll.tail)
        self.assertEqual(ll.head, None)

        arr = [i for i in range(10000)]
        ll = doublyLL(arr)

        self.assertTrue(self.compare(ll, arr))

    def test_insert(self):
        arr = [i for i in range(10000)]
        ll = doublyLL(arr)

        for i in range(1000):
            ll.insert(i, i)
            arr.insert(i, i)
            self.assertTrue(self.compare(ll, arr))

        ll.insert(100)
        arr.append(100)
        self.assertTrue(self.compare(ll, arr))

    def test_remove(self):
        arr = [i for i in range(10000)]
        ll = doublyLL(arr)

        for i in range(1000):
            v1 = ll.remove(i)
            v2 = arr.pop(i)
            self.assertEqual(v1, v2)
            self.assertTrue(self.compare(ll, arr))

        v1 = ll.remove()
        v2 = arr.pop()

        self.assertEqual(v1, v2)
        self.assertTrue(self.compare(ll, arr))

    @staticmethod
    def compare(ll, arr):
        if len(ll) != len(arr):
            return False

        curr, i = ll.head, 0
        while curr is not None:
            if arr[i] != curr.val:
                return False
            curr = curr.next
            i += 1

        return True

class avl:

    class Node:
        def __init__(self, val):
            self.val = val
            self.l, self.r = None, None
            self.bal = 0

    def __init__(self, arr = []):
        self.root = None

        for elt in arr:
            self.insert(elt)
            #print('='*80)
            #avl.print(self.root)
            #print()

    def insert(self, val):
        if self.root is None:
            self.root = self.Node(val)
        else:
            self.root = avl.__insert(self.root, val)

    def remove(self, val):
        if self.root is not None:
            self.root = avl.__remove(self.root, val)

    def search(self, val):
        return avl.__search(self.root, val)

    @staticmethod
    def __insert(node, val):
        if val == node.val:
            return node

        if val > node.val:  #right descent
            if node.r is not None:
                old_bal = node.r.bal
                node.r = avl.__insert(node.r, val)
                if not old_bal and node.r.bal:  #from zero to non-zero
                    node.bal += 1
            else: #new leaf, can't be unbalanced
                node.r = avl.Node(val)
                node.bal += 1
        else:               #left descent
            if node.l is not None:
                old_bal = node.l.bal
                node.l = avl.__insert(node.l, val)
                if not old_bal and node.l.bal:  #from zero to non-zero
                    node.bal -= 1
            else: #new leaf, can't be unbalanced
                node.l = avl.Node(val)
                node.bal -= 1

        return avl.__bal(node)

    @staticmethod
    def __remove(node, val):
        if val <= node.val:
            if node.l:
                old_bal = node.l.bal
                node.l = avl.__remswap(node.l, node) if val == node.val else avl.__remove(node.l, val)
                child = node.l
                right = False
            elif val == node.val:
                return node.r
            else:
                return node
        else:
            if node.r:
                old_bal = node.r.bal
                node.r = avl.__remove(node.r, val)
                child = node.r
                right = True
            else:
                return node

        return avl.__rembal(node, old_bal, child, right)

    @staticmethod
    def __remswap(node, swap):
        if node.r is not None:
            old_bal = node.r.bal
            node.r = avl.__remswap(node.r, swap)
            return avl.__rembal(node, old_bal, node.r, True)
        else:
            swap.val = node.val
            return node.l

    @staticmethod
    def __rembal(node, old_bal, child, right):
        if child is None or old_bal and not child.bal:
            node.bal -= 1 if right else -1

        return avl.__bal(node)

    @staticmethod
    def __bal(node):
        if node.bal == -2:
            if node.l.bal == 1: #double rotation
                node.l = avl.__lr(node.l)
                node = avl.__rr(node)

                node.r.bal, node.l.bal = 0, 0
                if node.bal == 1:       #value of node.l.r.bal from before both rotations
                    node.l.bal = -1     #left subtree was shorter, which is now inner right, weight on left is left
                elif node.bal == -1:
                    node.r.bal = 1      #right subtree was shorter, which is now inner left, weight on right is right

                node.bal = 0            #root is perfectly balanced
            else: #single rotation
                node = avl.__rr(node)
                if node.bal == 0:       #left child was balanced
                    node.bal = 1
                    node.r.bal = -1
                else:                   #left child was unbalanced
                    node.bal, node.r.bal = 0, 0
        elif node.bal == 2:
            if node.r.bal == -1: #double rotation
                node.r = avl.__rr(node.r)
                node = avl.__lr(node)

                node.r.bal, node.l.bal = 0, 0
                if node.bal == 1:       #value of node.r.l.bal from before both rotations
                    node.l.bal = -1     #left subtree was shorter, which is now inner right, weight on left is left
                elif node.bal == -1:
                    node.r.bal = 1      #right subtree was shorter, which is now inner left, weight on right is right

                node.bal = 0            #root is perfectly balanced
            else: #single rotation
                node = avl.__lr(node)
                if node.bal == 0:       #right child was balanced
                    node.bal = -1
                    node.l.bal = 1
                else:                   #right child was unbalanced
                    node.bal, node.l.bal = 0, 0
        return node

    @staticmethod
    def __rr(node):
        l = node.l

        node.l = l.r
        l.r = node

        return l

    @staticmethod
    def __lr(node):
        r = node.r

        node.r = r.l
        r.l = node

        return r

    @staticmethod
    def __search(node, val):
        if node is None:
            return False
        if val == node.val:
            return True

        return avl.__search(node.l, val) if val < node.val else avl.__search(node.r, val)

    @staticmethod
    def print(node, d = 0):
        if node is None:
            return

        avl.print(node.r, d + 1)
        print('  '*d, node.val)
        avl.print(node.l, d + 1)

class AVLTester(ut.TestCase):

    def test_init(self):
        bst = avl()
        self.assertIsNone(bst.root)

        bst = avl([i for i in range(1000)])
        self.isBalanced(bst.root)

    def test_insert(self):
        bst = avl()

        for i in range(1000):
            val = random.randint(0, 1000)
            bst.insert(val)
            self.isBalanced(bst.root)
            self.assertTrue(bst.search(val))

    def test_search(self):
        arr = [random.randint(0, 1000) for i in range(1000)]
        bst = avl(arr)

        for elt in arr:
            self.assertTrue(bst.search(elt))

        self.assertFalse(bst.search(-1))
        self.assertFalse(bst.search(1001))

    def test_remove(self):
        arr = [random.randint(0, 1000) for i in range(1000)]
        bst = avl(arr)

        for elt in arr:
            bst.remove(elt)
            self.isBalanced(bst.root)
            self.assertFalse(bst.search(elt))

    def isBalanced(self, root):
        if root is None:
            return 0

        hr, hl = self.isBalanced(root.r), self.isBalanced(root.l)

        self.assertEqual(hr - hl, root.bal)
        self.assertTrue(root.bal < 2 and root.bal > -2)

        return (hr if hr > hl else hl) + 1

if __name__ == '__main__':
    suite = ut.TestSuite()
    suite.addTest(ut.TestLoader().loadTestsFromTestCase(MaxHeapTester))
    suite.addTest(ut.TestLoader().loadTestsFromTestCase(MinHeapTester))
    suite.addTest(ut.TestLoader().loadTestsFromTestCase(DoublyLLTester))
    suite.addTest(ut.TestLoader().loadTestsFromTestCase(AVLTester))
    ut.TextTestRunner(verbosity=2).run(suite)
    #h = maxheap([(i, i) for i in range(10)])
    #print(h.arr)
