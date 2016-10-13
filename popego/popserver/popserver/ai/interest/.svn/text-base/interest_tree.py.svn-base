# -*- coding: utf-8 -*-
import elixir
from sqlalchemy import text, types, UniqueConstraint
from popserver.model import Tag

from itertools import imap

TREE_QUERY = """ 
  SELECT node.*
    FROM interest_cluster_nested_set AS node,
         interest_cluster_nested_set AS parent
    WHERE node.lft > parent.lft 
          AND node.lft < parent.rgt
          AND parent.id = :parentId
    ORDER BY node.lft
"""



class Tree(object):
    def __init__(self):
        self.parent = None
        self.children = []

    def addChild(self, node):
        node.parent = self
        self.children.append(node)

    def __repr__(self):
        return "<Tree(lft=%(lft)s,rgt=%(rgt)s)>" % self.__dict__

class InterestClusterNS(Tree, elixir.Entity):
    elixir.using_options(tablename='interest_cluster_nested_set')
    id = elixir.Field(types.Integer, primary_key=True)
    lft = elixir.Field(types.Integer, colname='lft')
    rgt = elixir.Field(types.Integer, colname='rgt')
    _interests = elixir.ManyToMany('Tag', tablename='node_interests')
    centralInterests = elixir.ManyToMany('Tag', 
                                         tablename='node_central_interests')

    def __init__(self, *args, **kwargs):
        elixir.Entity.__init__(self, *args, **kwargs)
        Tree.__init__(self)

    def interests(self):
        if len(self.children) > 0:
            return reduce(lambda acc, child: acc + child.interests(),
                   self.children,  [])
        else:
            return self._interests

    def subtree(self):
        nodes = InterestClusterNS.query.from_statement(TREE_QUERY)\
            .params(parentId=self.id).all()
        return preorder2Tree([self] + nodes)

def preorderTraversal(node, visitor):
    visitor(node)
    for child in node.children: preorderTraversal(child, visitor)

def preorder(tree):
    """ Generador para recorrer un ``Tree`` en forma preorder """
    yield tree
    for child in tree.children:
        for n in preorder(child):
            yield n
    


def preorder2Tree(nodes):
    """ 
    Convierte una lista preorder de ``Tree`` con lft y rgt
    a un ``Tree``
    """
    def clearChildren(n):
        n.children = []
        return n

    assert len(nodes)>0, "Nodes must have one element at least"
    nodes = map(clearChildren, nodes)

    currentNode = nodes[0]
    currentNode.parent = None
    for n in nodes[1:]:
        while n.rgt > currentNode.rgt:
            currentNode = currentNode.parent
        currentNode.addChild(n)
        currentNode = n
    return nodes[0]
    

def sequentialGenerator(start=1):
    """ Generador secuencial de ``start`` a infinito """
    while True:
        yield start
        start +=1


def computeIndices(tree, idxGenerator=sequentialGenerator):
    """ Compute los indices ``lft`` y ``rgt`` de un ``Tree`` """
    def aux(tree, generator):
        tree.lft = generator.next()
        
        for child in tree.children:
            aux(child, generator)
        
        tree.rgt = generator.next()

    aux(tree, idxGenerator())
    





