from __future__ import division
import numpy as np


NODE_COUNT = 0
CLASS_COUNT = 0

def reset_global():
    """
    Reset the global variables
    """

    global NODE_COUNT, CLASS_COUNT
    NODE_COUNT = 0
    CLASS_COUNT = 0

def get_node_class_count(tree, first_call = False):
    """
    This function returns the count of the
    nodes and classes
    """

    if first_call:
        reset_global()

    global NODE_COUNT, CLASS_COUNT
    for i in tree:
        NODE_COUNT += 1
        #print node_count, i
        if isinstance(tree[i]["Left"], set) and not isinstance(tree[i]["Right"], set):
            CLASS_COUNT += 1
            return get_node_class_count(tree[i]["Right"])
        elif not isinstance(tree[i]["Left"], set) and isinstance(tree[i]["Right"], set):
            CLASS_COUNT += 1
            return get_node_class_count(tree[i]["Left"])
        elif not isinstance(tree[i]["Left"], set) and not isinstance(tree[i]["Right"], set):
             get_node_class_count(tree[i]["Right"])
             get_node_class_count(tree[i]["Left"])
        else:
            CLASS_COUNT += 2

    return NODE_COUNT, CLASS_COUNT

def find_tree_cost(no_feature, no_class, total, error, node_count, class_count):
    """
    Calculate the cost of the tree
    and return it.
    """

    return np.log2(no_feature)*node_count + np.log2(no_class)*class_count + np.log2(total)*error
