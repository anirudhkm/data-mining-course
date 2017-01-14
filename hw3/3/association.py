"""
Name: Anirudh, Kamalapuram Muralidhar
Student @ Indiana University
Start date: 6th April, 2016
End date:
Objective: To implement association rule for
data mining assignment-4.
"""

import numpy as np
import pandas as pd
from sys import argv
import data
import sets
import frequent
import rule_generation
import lift
from collections import OrderedDict

def f_1_method(freq_ds, f1, df, support_count, k = 2,
               candidate_count=0,freq_count=0):
    """
    """

    freq_count += len(freq_ds)
    itemset_array = []
    # empty array creation
    for i in freq_ds:
        for j in f1:
            if i[-1] < j[0] and i != j:
                value = sets.union(i, j)
                if value not in itemset_array:
                    itemset_array.append(value)
    candidate_count += len(itemset_array)
    freq_data = data.apriori(itemset_array, df, support_count, freq_item_dict,
                          infreq_item_dict, k = k)
    if len(freq_data) == 0:
        print "Candidate count", candidate_count
        print "Freq count", freq_count
        allitems = freq_item_dict.copy()
        allitems.update(infreq_item_dict)
        closed_item = frequent.closed_freq_itemset(freq_item_dict,allitems)
        # function call
        maximal_item = frequent.maximal_freq_itemsets(freq_item_dict)
        # function call
        print "Number of maximal frequent itemset", maximal_item
        print "Number of closed frequent itemset", closed_item
        rule_generation.generate_association(freq_item_dict, confidence_threshold,
                                            len(df.index), support_threshold,"F-1",input_file)
        lift.generate_association(freq_item_dict, lift_threshold,
                                len(df.index), support_threshold,"F-1",input_file)
        return 0
    else:
        freq_ds = freq_data

    f_1_method(freq_ds, f1, df, support_count, k = k+1, candidate_count=candidate_count,
                freq_count=freq_count)
    # iterative call


def f_k_1_method(freq_ds, df, support_count, k = 2,
                 candidate_count = 0, freq_count = 0):
    """
    This function helps to perform
    combination of the freq itemset.
    """

    freq_count += len(freq_ds)
    itemset_array = []
    # empty array creation
    for i in xrange(len(freq_ds)):
        for j in xrange(i+1, len(freq_ds)):
            if freq_ds[i][:abs(k-2)] == freq_ds[j][:abs(k-2)]:
                value = sets.union(freq_ds[i], freq_ds[j])
                itemset_array.append(value)
    candidate_count += len(itemset_array)
    freq_data = data.apriori(itemset_array, df, support_count, freq_item_dict,
                          infreq_item_dict, k = k)
    if len(freq_data) == 0:
        print "Candidate count", candidate_count
        print "Freq count", freq_count
        allitems = freq_item_dict.copy()
        allitems.update(infreq_item_dict)
        closed_item = frequent.closed_freq_itemset(freq_item_dict, allitems)
        # function call
        maximal_item = frequent.maximal_freq_itemsets(freq_item_dict)
        # function call
        print "Number of maximal frequent itemset", maximal_item
        print "Number of closed frequent itemset", closed_item
        rule_generation.generate_association(freq_item_dict, confidence_threshold,
                                            len(df.index), support_threshold, "F-K-1",input_file)
        lift.generate_association(freq_item_dict, lift_threshold,
                                len(df.index), support_threshold, "F-K-1",input_file)
        return 0
    else:
        freq_ds = freq_data

    f_k_1_method(freq_ds, df, support_count, k = k+1, candidate_count = candidate_count,
                freq_count = freq_count)

def main():
    """
    This is the main function of the program.
    """

    first_level, df, support_count = data.read_data(input_file,support_threshold,
                                            freq_item_dict, infreq_item_dict)
    # read the input data set as a DF
    freq_ds = data.apriori(first_level, df, support_count,
                          freq_item_dict, infreq_item_dict)
    # generate freq itemset using the apriori algorithm
    level_one_freq = freq_item_dict.copy()
    level_one_infreq = infreq_item_dict.copy()
    # make copies of the level one freq and infreq items
    print "F-K-1 Method"
    f_k_1_method(freq_ds, df, support_count, candidate_count=len(first_level))
    # implementation of method one
    freq_item_dict.clear()
    freq_item_dict.update(level_one_freq)
    infreq_item_dict.clear()
    infreq_item_dict.update(level_one_infreq)
    # clear dictionary and update them
    print "F-1 method"
    f_1_method(freq_ds, freq_ds, df, support_count, candidate_count=len(first_level))
    # implementation of method two

if __name__ == '__main__':
    # start of the main program
    input_file = argv[1]
    # get the input file as a sys argv
    support_threshold = float(argv[2])
    # get the support threshold as a sys argv
    confidence_threshold = float(argv[3])
    # get the confidence threshold as a sys argv
    lift_threshold = float(argv[4])
    # get the lift threshold as a sys argv
    freq_item_dict = OrderedDict()
    infreq_item_dict = OrderedDict()
    # create empty Ordered dict
    f = main()
    # function call
