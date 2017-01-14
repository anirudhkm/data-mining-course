# -*- coding: utf-8 -*-

def feature_extraction(inp_data, count, tfidf_transformer, data = 'train'):
    """
    This function helps to extract the
    features from the train data and returns them.
    The method of “Term Frequency times Inverse Document Frequency”
    is used for this process.
    Arguments:
        1. inp_data: The data for which the features to be extracted,
         taken as a dictionary type.
        2. data: Defaulted to "train", specifies the subset type of data.

    Return value:
        1. A sparse matrix
    """

    if data == 'train':
        train_count = count.fit_transform(inp_data.data)
        # get the occurence from for the train data
        train_tfidf = tfidf_transformer.fit_transform(train_count)
        # transform data from occurence to frequency
        return train_tfidf

    elif data == 'test':
        # if data is of test type
        test_count = count.transform(inp_data.data)
        # get the occurence from for the test data
        test_tfidf = tfidf_transformer.transform(test_count)
        # transform data from occurence to frequency
        return test_tfidf
