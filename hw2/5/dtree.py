"""
Name: Anirudh, Kamalapuram Muralidhar
Indiana University
Start date: 19th Feb, 2016
Objective: To construct a decision tree based on
        greedy algorithm and test the overfitting criteria.

Dataset are taken from: http://archive.ics.uci.edu/ml/datasets.html
"""

from __future__ import division
import numpy as np
import pandas as pd
from sys import argv
from data_process import *
from impurity import *
from validation_test import *
from prune import *
from termcolor import colored
from roc import *

def split_data(df, feature, impurity_dict, tree_dict,
              curr_node_dict, impurity_measure = "gini",prune_dict={}):
    """
    This function helps to split the dataframe based
    on the threshold given and then calls the
    'decision_tree' function to built tree based on that data.

    Arguments:
        1. df -> is a pandas dataframe with the data.
        2. feature -> the feature of string type on which the data will be split.
        3. impurity_dict -> the dict which has the threshold value for the impurity.
        4. tree_dict -> this is the decision tree which we are building on.
        5. curr_node_dict -> the current node which is a dict.
    """

    low_data_df = df[df[feature] <= impurity_dict[feature][1]]
    # get the lower side of the data
    decision_tree(low_data_df, tree_dict, curr_node_dict,
                  feature, align_str = 'Left', prune_dict=prune_dict,
                  impurity_measure = impurity_measure)
    # function call
    high_data_df = df[df[feature] > impurity_dict[feature][1]]
    # get the higher side of the data
    decision_tree(high_data_df, tree_dict, curr_node_dict,
                  feature, align_str = 'Right',prune_dict=prune_dict,
                  impurity_measure = impurity_measure)
    # function call

def check_leaf_node(df):
    """
    This function helps to check
    if we have reached the leaf node
    or not and returns True or False
    based on that.
    """

    class_node = False
    # flag to check if reached the class node
    if len(set(df["Class"])) == 1:
       # check if we have reached the class node
       class_node = True
       # change flag value, asserting we reached class node
    return class_node

def display_tree(tree, inp_file = '', tab_space = 0, header = False):

    if header:
        # print the header
        print "{}".format(inp_file)
    for i in tree:
        # structure the node
        print tab_space*'\t', i
        if isinstance(tree[i]["Right"], set):
            print (tab_space+1)*'\t', tree[i]["Right"]
        else:
            display_tree(tree[i]["Right"], tab_space = tab_space + 1)

        if isinstance(tree[i]["Left"], set):
            print (tab_space+1)*'\t', tree[i]["Left"]
        else:
            display_tree(tree[i]["Left"], tab_space = tab_space + 1)

def decision_tree(df, tree_dict, curr_node_dict,
                  prev_feature = None, align_str = None,
                  impurity_measure = "gini", prune_dict = {}):
    """
    This is the main function responsible to develop
    the decision tree.

    Arguments:
        1. df -> pandas dataframe which contains the data.
        2. tree_dict ->  this is the decision tree which we are building on
                         of dict type.
        3. curr_node_dict -> the current node of dict type which we will
                             be developing on.

    Default Arguments:
        1. prev_feature (None) -> the previous feature which was assigned.
        2. align_str (None) -> the alignment of the split, it can be 'Right'
                               or 'Left'.
    """

    class_node = check_leaf_node(df)
    # function call to check if we reach leaf node
    if class_node:
       # if we reached leaf node
       curr_node_dict[align_str] = set(df["Class"])
       # assign value to the current node based on the alignment
    else:
        impurity_by_features_df = impurity_calc(df, impurity_measure = impurity_measure)
        # function call to calculate the gini values
        threshold_impurity_dict = {}
        # empty dict
        for feature in iter(impurity_by_features_df.index):
            # iterate through each feature sorted on impurity
            calc_threshold(df, feature, threshold_impurity_dict,
                          impurity_measure = impurity_measure)
            # function call
        if impurity_measure.lower() == "entropy":
            # if impurity is entropy
            for i in iter(impurity_by_features_df.index):
                # iterate through each index
                updated_gain = round(impurity_by_features_df[i],4)-round(threshold_impurity_dict[i][0],4)
                threshold_impurity_dict[i] = (updated_gain,threshold_impurity_dict[i][1])

                # update the gain value
            best_feature = sorted(threshold_impurity_dict,
                                key = threshold_impurity_dict.get)[-1]
            # get the best feature after sorting
        else:
            best_feature = sorted(threshold_impurity_dict,
            key = threshold_impurity_dict.get)[0]
            # get the best feature after sorting

        node_key = (best_feature,threshold_impurity_dict[best_feature])
        # define the node key
        prune_dict[node_key] = df
        # add key value pair to the prune dict
        if not class_node and align_str:
            # grow the tree
            curr_node_dict[align_str] = {node_key:{}}
            curr_node_dict = curr_node_dict[align_str][node_key]
        else:
            tree_dict[node_key] = {}
            curr_node_dict = tree_dict[node_key]

        # get the best feature, on the which the data will be split
        split_data(df, best_feature, threshold_impurity_dict, tree_dict,
                    curr_node_dict, impurity_measure = impurity_measure,
                    prune_dict = prune_dict)
        # function call

def main(input_file, impurity_measure):
    """
    This is the main function which triggers
    the start of decision tree
    """

    df = read_input_file(input_file)
    # function call to read data
    cross_validation(df, impurity_measure)
    # function call
    cross_validation_roc(df, impurity_measure)
    # function call for cross validation
