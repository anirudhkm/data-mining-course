from __future__ import division
import dtree
import numpy as np
from prune import *
from mld import *
from collections import OrderedDict

def test_data_on_tree(tree, test):
    """
    This function performs the classification
    for the data passed for based on the tree model.
    Finally, this returns the class which it predicts.

    Arguments:
        1. tree -> the tree model which on which the data
        will be tested.
        2. test -> the test data which is a pandas series data.
    """

    if isinstance(tree, set):
        # check if we reached a leaf node
        return tree

    for i in tree:
        # iterate through the nodes
        if float(test[i[0]]) <= i[1][1]:
            # compare the value with the node threshold
            tree = tree[i]['Left']
            # traverse the left tree
        else:
            tree = tree[i]['Right']
            # traverse the right tree

    return test_data_on_tree(tree, test)
    # recursive call of the function.

def calc_cv_accuracy(tree_dict, test_df, error_count = False):
    """
    This function helps to test the
    accuracy of the cross validation and
    returns the value.

    Arguments:
        1. tree_dict -> the tree model that we developed which is
        stored in a dictionary.
        2. test_df -> the test data as a pandas dataframe.
    """

    correct_count = 0
    # initial value of correct predicted value
    for i in test_df.index:
        # iterate through each of the row
        test = test_df.loc[i]
        # get the particular row data
        result = test_data_on_tree(tree_dict, test)
        # test the data on the tree model
        if test['Class'] in result:
            # check for correct prediction
            correct_count += 1
            # increment correct_count for correct prediction
        else:
            pass
    if error_count:
        len(test_df.index) - correct_count
    return correct_count/len(test_df.index)
    # return the error count


def split_data_for_cv(df, k = 10):
    """
    This function helps to split the data
    for the 'k-fold' cross validation that needs to
    be performed on the data and finally returns
    the data in a list of tuples format

    Arguments:
        1. df -> data as a pandas dataframe.
        2. k = 10 -> default argument stating how many
        cross validation that needs to be done.
    """

    k_fold_data_list = []
    # empty list
    intervals_np = np.linspace(0, len(df), num = k+1, dtype = int)
    # get the various intervals on which the data will be split
    for i in xrange(len(intervals_np) - 1):
        # iterate through each of the intervals
        start = intervals_np[i]
        # start index
        end = intervals_np[i+1]
        # stop index
        test_data = df.iloc[start:end+1,]
        # get the test data
        train_data = df.drop(test_data.index)
        # get the train data
        k_fold_data_list.append((train_data, test_data))
        # append the train and test data to the list
    return k_fold_data_list


def cross_validation(df, impurity_measure, k = 10):
    """
    This function initiates the cross validation
    procedure for the dataset set that we have.
    It finally prints out the accuracy of the
    k-fold cross validation performed.
    """

    df = df.iloc[np.random.permutation(len(df))]
    # shuffle the input dataframe
    k_fold_data = split_data_for_cv(df)
    # func call to get train and test for cross validation
    cum_accuracy = 0
    # initial value
    cost_tree_dict = OrderedDict()
    # empty dict
    for train_data, test_data in k_fold_data:
        # iterate over the train and test data
        tree_dict = dict()
        # create an empty ordered dict
        prune_dict = {}
        # empty dict
        dtree.decision_tree(train_data, tree_dict, {},
                      impurity_measure = impurity_measure,
                      prune_dict = prune_dict)
        # function call to construct the tree
        cum_accuracy += calc_cv_accuracy(tree_dict, test_data)
        error_count = calc_cv_accuracy(tree_dict, train_data.head(int(0.25*len(train_data))),
                                       error_count = True)
        # get the count of the correcty predicted value
        prune_tree(tree_dict, prune_dict)
        # perform pruning on the tree
        node_count, class_count = get_node_class_count(tree_dict, first_call=True)
        cost_of_tree = find_tree_cost(len(train_data.columns[:-1]),
                                     len(train_data["Class"].unique()),
                                     len(train_data.index), error_count,
                                     node_count, class_count)
        # function call
        cost_of_tree = round(cost_of_tree,4)
        cost_tree_dict[cost_of_tree] = tree_dict
        # update the dictionary
    print "The cost of the trees based on 10 fold CV are\n", cost_tree_dict.keys()
    print "The best tree of the 10 trees obtained is\n ", dtree.display_tree(cost_tree_dict[min(cost_tree_dict)])
    print "\nThe cost of the above tree is ", min(cost_tree_dict)
