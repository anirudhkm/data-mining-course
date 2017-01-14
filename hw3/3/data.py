import numpy as np
import pandas as pd
import itertools

def read_data(input_file, support,
             freq_item_list, infreq_item_dict):
    """
    This function helps to read the input
    file and returns them as a dataframe.
    """

    df = pd.read_csv(input_file)
    # load the data in a dataframe
    support_count = int(support*len(df.index))
    first_level = []
    for i in df.columns:
        # iterate through each column header
        first_level.append(tuple((i,)))
        if sum(df[i]) >= support_count:
            freq_item_list[tuple((i,))] = sum(df[i])
        else:
            infreq_item_dict[tuple((i,))] = sum(df[i])

    return first_level, df, support_count

def apriori(item_list, df, support_count, freq_item_dict, infreq_item_dict, k = 1):
    """
    Apriori algo implementation
    """

    freq_item_list = []
    # empty freq item list
    for item in iter(item_list):
        # iterate through the candidate itemset
        if k < 3:
            if sum(df[list(item)].prod(axis=1)) >= support_count:
                freq_item_list.append(item)
                freq_item_dict[item] = sum(df[list(item)].prod(axis=1))
            else:
                infreq_item_dict[item] = sum(df[list(item)].prod(axis=1))
        else:
            if sum(df[list(item)].prod(axis=1)) < support_count:
                infreq_item_dict[item] = sum(df[list(item)].prod(axis=1))
            else:
                for subset in itertools.combinations(item, k-1):
                    # iterate over the possible combinations of the items
                    if subset in freq_item_dict:
                        # check for pruning
                        #freq_item_dict.pop(subset)
                        pass
                    else:
                        infreq_item_dict[item] = sum(df[list(item)].prod(axis=1))
                        break
                else:
                    freq_item_list.append(item)
                    freq_item_dict[item] = sum(df[list(item)].prod(axis=1))

    return sorted(freq_item_list)
