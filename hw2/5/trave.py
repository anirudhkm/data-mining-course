import pandas as pd
from collections import OrderedDict

def test_data_on_tree(tree, test):
    """
    """

    if isinstance(tree, set):
        return tree

    for i in tree:
        if float(test[i[0]]) <= i[1][1]:
            tree = tree[i]['Left']
        else:
            tree = tree[i]['Right']

    return test_data_on_tree(tree, test)


def cross_validation_test(tree_dict, test_df):
    """
    """

    correct_count = 0
    total_count = 0
    for i in test_df.index:
        test = test_df.loc[i]
        result = test_data_on_tree(tree_dict, test)
        total_count += 1
        if test['class'] in result:
            correct_count += 1
        else:
            pass
    return total_count, correct_count
