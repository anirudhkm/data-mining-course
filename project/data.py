# -*- coding: utf-8 -*-

from sklearn.datasets import fetch_20newsgroups

def load_training_data(categories_list = None):
    """
    This function helps to load the
    training data from the twenty news group data
    and returns them.

    Arguments:
        1. categories_list: Defaulted to None, when given
        retrieves only mentioned categories.
    """

    train_data = fetch_20newsgroups(subset = 'train', shuffle = True,
                                    categories = categories_list)
    # load the training data set
    return train_data

def load_test_data(categories_list = None):
    """
    This function helps to load the
    test data from the twenty news group data
    and returns them.

    Arguments:
        1. categories_list: Defaulted to None, when given
        retrieves only mentioned categories.
    """

    test_data = fetch_20newsgroups(subset = 'test', shuffle = True,
                                    categories = categories_list)
    # load the training data set
    return test_data
