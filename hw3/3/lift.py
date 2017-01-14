from __future__ import division
from itertools import combinations

def confidence_based_pruning(freq_item_dict, item,
                            possible_list, lift,
                            pruning_list, count_list,
                            association_dict,n):
    """
    Confidence based pruning for association rule
    generation
    """

    for x in possible_list:
        # iterate through possible subset
        y = set(item) - set(x)
        flag = False
        for each in pruning_list:
            if each.issubset(y):
                flag = True
                break
        if flag: continue
        lift_value = (freq_item_dict[item]/n)/((freq_item_dict[x]/n)*(freq_item_dict[tuple(sorted(y))]/n))
        count_list[1] += 1
        if lift_value >= lift:
            # check for threshold pass
            pass
        else:
            pruning_list.append(y)

def find_rules(freq_item_dict, item, possible_list, lift, count_list,
               n,association_dict):
    """
    """

    for x in possible_list:
        # iterate through possible subset
        y = set(item) - set(x)
        lift_value = (freq_item_dict[item]/n)/((freq_item_dict[x]/n)*(freq_item_dict[tuple(sorted(y))]/n))
        count_list[0] += 1
        if lift_value >= lift:
            # check for threshold pass
            association_dict[x,tuple(y)] = lift_value
        else:
            pass


def generate_association(freq_item_dict, lift, n,support_threshold,method,input_file):
    """
    Generate association rules from the
    frequent itemsets
    """

    rules_count_list = [0,0]
    # empty list
    association_dict = {}
    # empty dict
    for item in freq_item_dict.keys()[::-1]:
        # iterate through each item
        possible_set_list = []
        pruning_list = []
        # empty list's
        for i in xrange(len(item)-2, -1,-1):
            # iterate through the length
            possible_set_list.extend(list(combinations(item, i+1)))

        find_rules(freq_item_dict, item, possible_set_list,
                   lift, rules_count_list,n,association_dict)
        # finding rules based on brute force method
        confidence_based_pruning(freq_item_dict, item,
                               possible_set_list,
                               lift,pruning_list,
                               rules_count_list, association_dict,n)
        # finding rules based on association rules
    print "Brute force rules generated, Lift", rules_count_list[0]
    print "Pruning rules generated, Lift", rules_count_list[1]
    association_dict = sorted(association_dict.items(),key = lambda x : x[1],
                              reverse=True)
    output_file = open(method+"RulesByLiftMeasure.txt", "a")
    output_file.write("Input file:{}\nSupport:{}\nLift:{}\nTop 10 rules\n".format(input_file,
                                                                        support_threshold,
                                                                        lift))
    # open a file in append mode
    for rule in association_dict[:10]:
        x = rule[0][0]
        y = rule[0][1]
        measure = rule[1]
        asso = "{} -> {} with a lift measure of {}\n".format(",".join(x),",".join(y),measure)
        output_file.write(asso)
    output_file.write("\n\n\n")
    output_file.close()
