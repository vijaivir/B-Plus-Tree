# Implementation of B+ tree functionality.

from ctypes import pointer
from turtle import up
from index import *

# Takes a node as input
def height(index, root):
    pointers = root.pointers.pointers
    h = 1
    if pointers[0] != 0:
        h += 1
        height(index, index.nodes[pointers[0]])
    return h
    

def IsEmpty(index):
    return len(index.nodes) == 0

def IsLeaf(node):
    pointers = node.pointers.pointers
    if pointers[0] == 0:
        return True

# This method changes the keyset for leaf nodes that have space
# call it if IsLeaf() and keyset[1] == -1
def SimpleInsert(node, key):
    keyset = node.keys.keys
    if key < keyset[0]:
        node.keys = KeySet((key, keyset[0]))
    else:
        node.keys = KeySet((keyset[0], key))
    return node

def FullInsert(index, key, i):
    keyset = index.nodes[i].keys.keys
    size = len(index.nodes)
    lc = (3*i)+1
    mc = (3*i)+2
    rc = (3*i)+3
    if size <= (3*i) + size:
        temp = Index([Node()]*((3 * size) + size))
        keys = [keyset[0], keyset[1], key]
        keys.sort()
        temp.nodes[i] = Node(KeySet((keys[1], -1)), PointerSet((lc, mc, 0)))
        temp.nodes[lc] = Node(KeySet((keys[0], -1)), PointerSet((0, 0, mc)))
        temp.nodes[mc] = Node(KeySet((keys[1], keys[2])), PointerSet((0, 0, 0)))
        index = temp
    return index

# This will only be called if the index is not empty and key does not exist
def InsertKey(index, key):
    i = FirstLeaf(index, key, index.nodes[0], 0)
    keyset = index.nodes[i].keys.keys
    if keyset[1] == -1:
        SimpleInsert(index.nodes[i], key)
        return index
    else: #its a full node 
        index = FullInsert(index, key, i)
        return index


def KeyExists(index, key, root):
    i = FirstLeaf(index, key, root, 0)
    keyset = index.nodes[i].keys.keys
    return keyset[0] == key or keyset[1] == key


def FirstLeaf(index, key, root, i):
    if IsLeaf(root):
        return i
    keyset = root.keys.keys
    pointers = root.pointers.pointers
    if key < keyset[0]:
        return FirstLeaf(index, key, index.nodes[pointers[0]], pointers[0])
    if key >= keyset[0] and key < keyset[1]:
        return FirstLeaf(index, key, index.nodes[pointers[1]], pointers[1])
    if key >= keyset[1]:
        return FirstLeaf(index, key, index.nodes[pointers[2]], pointers[2])

# You should implement all of the static functions declared
# in the ImplementMe class and submit this (and only this!) file.
class ImplementMe:

    # Returns a B+-tree obtained by inserting a key into a pre-existing
    # B+-tree index if the key is not already there. If it already exists,
    # the return value is equivalent to the original, input tree.
    #
    # Complexity: Guaranteed to be asymptotically linear in the height of the tree
    # Because the tree is balanced, it is also asymptotically logarithmic in the
    # number of keys that already exist in the index.
    @staticmethod
    def InsertIntoIndex( index, key ):
        if(IsEmpty(index)):
            index = Index([Node(KeySet((key, -1)), PointerSet((0,0,0)))]*1)
            return index
        root = index.nodes[0]
        if(KeyExists(index, key, root)):
            return index
        index = InsertKey(index, key)
        return index

    # Returns a boolean that indicates whether a given key
    # is found among the leaves of a B+-tree index.
    #
    # Complexity: Guaranteed not to touch more nodes than the
    # height of the tree
    @staticmethod
    def LookupKeyInIndex( index, key ):
        if len(index.nodes) == 0:
            return False
        return KeyExists(index, key, index.nodes[0])

    # Returns a list of keys in a B+-tree index within the half-open
    # interval [lower_bound, upper_bound)
    #
    # Complexity: Guaranteed not to touch more nodes than the height
    # of the tree and the number of leaves overlapping the interval.
    @staticmethod
    def RangeSearchInIndex( index, lower_bound, upper_bound ):
        keys_in_range = []
        if IsEmpty(index):
            return keys_in_range
        i = FirstLeaf(index, lower_bound, index.nodes[0], 0)
        keyset = index.nodes[i].keys.keys
        pointers = index.nodes[i].pointers.pointers
        if keyset[0] >= lower_bound and keyset[0] < upper_bound:
            keys_in_range.append(keyset[0])
        if keyset[1] >= lower_bound and keyset[1] < upper_bound:
            keys_in_range.append(keyset[1])
        i = pointers[2]
        while(keyset[1] < upper_bound and pointers[2] != 0):
            keyset = index.nodes[i].keys.keys
            pointers = index.nodes[i].pointers.pointers
            if keyset[0] >= lower_bound and keyset[0] < upper_bound:
                keys_in_range.append(keyset[0])
            if keyset[1] >= lower_bound and keyset[1] < upper_bound:
                keys_in_range.append(keyset[1])
            i = pointers[2]
        return keys_in_range

    
