from collections import OrderedDict

def maximal_freq_itemsets(freq_item_dict):
    """
    This function helps to find the maximal
    frequent items in the dataset and returns
    them as a sequence.
    """

    maximal_freq_count = 0
    # initial value
    for i in freq_item_dict:
        # iterate through each item
        flag = True
        for j in freq_item_dict:
            # iterate again
            if len(i) + 1 == len(j) and set(i).issubset(set(j)):
                flag = False
            elif len(i) + 2 == len(j):
                break
        if flag:
            maximal_freq_count += 1

    return maximal_freq_count

def closed_freq_itemset(freq_item_dict, all_item):
    """
    Compute closed frequency itemsets
    """

    closed_item_count = 0
    # initial value
    for i in freq_item_dict:
        # iterate through each items
        flag = True
        for j in all_item:
            # iterate through all items
            if len(i) + 1 == len(j) and set(i).issubset(set(j)):
                # check for immediate super set
                if freq_item_dict[i] == all_item[j]:
                    flag = False
                    break
        if flag:
            closed_item_count += 1

    return closed_item_count
