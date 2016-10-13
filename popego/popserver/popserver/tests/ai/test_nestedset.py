from popserver.ai.interest.interest_tree import *
from unittest import TestCase
from popserver.tests import *
from fixture import DataTestCase
from popserver.tests import popfixtures
from popserver.model import dbsession

class TestNestedSetPersistence(DataTestCase, TestModel):
    fixture = dbfixture
    datasets = [popfixtures.TagData]
    
    def setUp(self):
        TestModel.setUp(self)
        DataTestCase.setUp(self)

        self.ns = InterestClusterNS()
        
        childA = InterestClusterNS()
        childAA = InterestClusterNS()
        childA.addChild(childAA)
        self.ns.addChild(childA)

        childB = InterestClusterNS()
        self.ns.addChild(childB)

        td = self.data.TagData

        childAA._interests = [Tag.get(td.foo.id)]
        childB._interests = [Tag.get(td.bar.id), 
                             Tag.get(td.baz.id)]
        self.ns.centralInterests = [Tag.get(td.foo.id), 
                                    Tag.get(td.bar.id), 
                                    Tag.get(td.baz.id)]
        
        computeIndices(self.ns)

    def tearDown(self):
        DataTestCase.tearDown(self)
        TestModel.tearDown(self)

    def testPersistence(self):
        preorderList = list(preorder(self.ns))
        dbsession.flush()
        dbsession.remove()

        ns = InterestClusterNS.query.first()

        otherPreorderList = list(preorder(ns.subtree()))

        getId = lambda x: x.id
        assert map(getId, preorderList) == map(getId, otherPreorderList)

        


class TestTree(TestCase):

    def setUp(self):
        def newTree(data):
            t = Tree()
            t.data = data
            return t

        # construir arbol de prueba
        self.root = newTree(1)
        
        two = newTree(2)
        two.addChild(newTree(3))
        two.addChild(newTree(4))
        self.root.addChild(two)

        self.root.addChild(newTree(5))

        six = newTree(6)
        six.addChild(newTree(7))
        six.addChild(newTree(8))
        self.root.addChild(six)

    def testPreorderTraversal(self):
        data = []
        def v(n):
            data.append(n)

        preorderTraversal(self.root, v)
        assert map(lambda n: n.data, data) == [1,2,3,4,5,6,7,8]
        
    def testPreorder(self):
        lst = [n.data for n in preorder(self.root)]
        assert lst == [1,2,3,4,5,6,7,8]
        
        
    def testComputeIndices(self):
        computeIndices(self.root)
        
        data = []
        def v(n):
            data.append(n)

        preorderTraversal(self.root, v)
        assert map(lambda n: (n.lft, n.rgt), data) == \
            [(1,16),
             (2,7),
             (3,4),
             (5,6),
             (8,9),
             (10,15),
             (11,12),
             (13,14)
             ]

    def testPreorder2Tree(self):
        computeIndices(self.root)
        preorderList = list(preorder(self.root))
        otherRoot = preorder2Tree(preorderList)
        otherPreorderList = list(preorder(otherRoot))

        assert otherPreorderList == preorderList
