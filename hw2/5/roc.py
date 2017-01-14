from __future__ import division
import dtree
from validation_test import *
import matplotlib.pyplot as plt

def convert_to_binary_classifier(df, classifier):
    """
    Make the data as a one vs all classifier based on the
    classifier given
    """

    df.ix[df.Class == classifier, 'Class'] = 1
    df.ix[df.Class != 1, 'Class'] = 0
    return df

def calculate_tp_fp(tree, test_df):
    """
    This function calculates the
    true positive rate and false positive rate
    and returns them
    """

    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for i in test_df.index:
        test = test_df.loc[i]
        result = test_data_on_tree(tree, test)
        if test["Class"] == 1 and result == {1}:
            tp += 1
        elif test["Class"] == 0 and result == {1}:
            fp += 1
        elif test["Class"] == 0 and result == {0}:
            tn += 1
        elif test["Class"] == 1 and result == {0}:
            fn += 1

    return tp, fn, fp, tn

def plot_roc(x1, y1, xlabel='', ylabel = '', title = '',scatter=True):
    """
    Plot the curve for the given value
    """

    plt.figure()
    if scatter:
        plt.scatter(x1,y1,c='g')
    else:
        plt.plot(x1, y1, c = 'r')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(title+'.png')

def cross_validation_roc(df, impurity_measure, k = 10):
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
    for var in iter(set(df.Class)):
        # iterate over each class
        tpr = []
        fpr = []
        recall = precision = f_measure = []
        balance_accuracy = []
        accuracy = []
        for train_data, test_data in k_fold_data:
            # iterate over the train and test data
            tree_dict = dict()
            # create an empty ordered dict
            train_data = convert_to_binary_classifier(train_data.copy(), var)
            test_data = convert_to_binary_classifier(test_data.copy(), var)
            dtree.decision_tree(train_data, tree_dict, {},
                        impurity_measure = impurity_measure)
            # function call to construct the tree
            tp, fn, fp, tn = calculate_tp_fp(tree_dict, test_data)
            r = tp/(tp+fn)
            recall.append(r)
            p = tp/(tp+fp)
            precision.append(p)
            f_measure.append((2*r*p/(r+p)))
            tpr_value = (tp/(tp + fn))
            tpr.append(tpr_value)
            fpr_value = fp/(fp + tn)
            fpr.append(fpr_value)
            balance_accuracy.append(0.5*(tpr_value+fpr_value))
            accuracy.append((tp+tn)/(tp+fn+fp+tn))
        print "\n\nResults for {0} Vs Non-{0} classifier".format(var)
        print "Simple accuracy: {}".format(np.mean(accuracy))
        print "Balanced accuracy: {}".format(np.mean(balance_accuracy))
        print "F1 measure: {}".format(np.mean(f_measure))
        plot_roc(fpr,tpr,"False Positive Rate","True Positive Rate",
                "ROC Curve for " + str(var) + "Vs not " + str(var))
        # plot the roc data
        plot_roc(recall,precision,"Recall","Precision",
                "Precision Vs Recall Curve for " + str(var) + "Vs not " + str(var),scatter=False)
