"""
Name: Anirudh, Kamalapuram Muralidhar
Indiana University
Start date: 19th Feb, 2016
Objective: This file helps in calculating
the measure of impurity for the various
features
"""

from __future__ import division
import numpy as np
import pandas as pd

def impurity_calc(df, impurity_measure = "gini"):
    """
    This function helps to calculate
    the gini value for the various features
    for the given pandas DF.
    Finally it returns the feature and gini value
    in a dictionary

    Arguments:
        1. df -> a pandas dataframe
    """

    gini_dict = {}
    # empty dict
    group_by_class_df = df.groupby(by = "Class").count()
    # group the data based on the class column header
    sum_df = group_by_class_df.sum()
    # aggreate sum of each column
    for i in iter(group_by_class_df.columns):
        # iterate through each feature
        agg_sum = 0.0
        for j in iter(group_by_class_df.index):
            # iterate through each class
            if impurity_measure.lower() == 'gini':
                agg_sum += (group_by_class_df.loc[j, i]/sum_df[i])**2

            elif impurity_measure.lower() == 'entropy':
                agg_sum += -(group_by_class_df.loc[j, i]/sum_df[i])*np.log2((group_by_class_df.loc[j, i]/sum_df[i]))
            else:
                pass
        if impurity_measure == 'gini':
            gini_dict[i] = round(1 - agg_sum, 4)
        else:
            gini_dict[i] = round(agg_sum, 4)
        # store the gini value in the dict
    return pd.Series(gini_dict).sort_values()
