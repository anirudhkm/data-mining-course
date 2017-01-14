"""
Name: Anirudh, Kamalapuram Muralidhar
Indiana University
Start date: 19th Feb, 2016
Objective: This file has functions which helps in
the data processing work for the decision_tree.py program.
"""

import pandas as pd
import numpy as np
from impurity import *
from tree import *


def cross_validation_data(df, k = 10):
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


def split_data_for_threshold(df, threshold_float, impurity_df,
                            threshold_impurity_dict,
                            impurity_measure = "gini"):
    """
    This function helps to split the data
    based on the threshold and calculates the GINI

    Arguments:
        1. df -> pandas dataframe
        2. threshold_float ->threshold value as a float
    """

    feature_data_pd = df[[impurity_df, "Class"]]
    # get the particulat feature data
    lower_threshold_pd = feature_data_pd[feature_data_pd[impurity_df] <= threshold_float]
    # get the data less than or equal to the threshold
    upper_threshold_pd = feature_data_pd[feature_data_pd[impurity_df] > threshold_float]
    # get the data greater than the threshold
    lower_threshold_gini = impurity_calc(lower_threshold_pd, impurity_measure)
    # get the gini for the lower set of data
    upper_threshold_gini = impurity_calc(upper_threshold_pd, impurity_measure)
    # get the gini for the upper set of the data
    impurity_value = (len(lower_threshold_pd)*lower_threshold_gini[impurity_df]/len(feature_data_pd)
              + len(upper_threshold_pd)*upper_threshold_gini[impurity_df]/len(feature_data_pd))
    # gini for the particular threshold
    threshold_impurity_dict[threshold_float] = impurity_value

def calc_threshold(df, feature, threshold_gini,
                  impurity_measure = "gini"):
    """
    This function gets the
    data of the given feature and
    returns them in a sorted order

    Arguments:
        1. df <- a pandas dataframe.
        2. feature <- the gini of the overall features
    """

    threshold_impurity_dict = {}
    # empty dict
    percentile_values = np.array([])
    # empty numpy array
    unique_value_df = df[feature].unique()
    # get the unique values for the feature
    for percent in iter(xrange(0, 101, 10)):
        # iterate through each percentile value
        percentile_values = np.append(percentile_values,
                            np.percentile(unique_value_df, percent))
        # append the percentile values in the array
    for percent in iter(percentile_values):
        split_data_for_threshold(df, percent, feature, threshold_impurity_dict,
                                impurity_measure = impurity_measure)
        # function call to split data
    final_threshold = round(min(threshold_impurity_dict,
                      key = threshold_impurity_dict.get),4)
    # find the threshold on which the data will be split
    low_data_df = df[df[feature] <= final_threshold][[feature, "Class"]]
    # get the lower end of the data
    low_gini = impurity_calc(low_data_df, impurity_measure = impurity_measure)
    # calculate gini for the lower data
    high_data_df = df[df[feature] > final_threshold][[feature, "Class"]]
    # get the higher data based on the threshold
    high_gini = impurity_calc(high_data_df, impurity_measure = impurity_measure)
    # get the gini for the higher data
    weighted_gini = round(len(low_data_df)*low_gini/len(df) + len(high_data_df)*high_gini/len(df),4)
    threshold_gini[feature] = (float(weighted_gini), final_threshold)

def read_input_file(input_file):
    """
    This function helps to read the
    input file as a pandas DF
    and returns it
    """
    header_list = list()
    # empty list
    return pd.read_csv(input_file)
    """
    for i in df.columns[:-1]:
        # iterate through each column header
        header_list.append("f"+str(i))
        # add headers for the features
    header_list.append("class")
    # add the header for the class
    df.columns = header_list
    """
    return df
