# -*- coding: utf-8 -*-

"""
Name: Anirudh, Kamalapuram Muralidhar
Indiana University
Start date: 24th April, 2016
End date: 26th April, 2016
Objective: To build a classifier models based on
various algorithms.
"""

import numpy as np
import data
import features
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation
from sklearn import metrics



def naive_bayes(train_data, tfidf):
    """
    This function helps to build the Naive Bayes
    classifier based on the user input of Bernoulli
    and Multinomial model and returns them.
    Arguments:
        1. train_data: The training data for which the classifier
        will be fit, as a dictionary.
        2. tfidf: The TFIDF sparse matrix.
        3. method: Defaulted to None, specifies the type
        of the Naive Bayes classifier, either Bernoulli or
        Multinomial.

    Return values:
        1. The classifier object.
    """

    clf = MultinomialNB().fit(tfidf, train_data.target)
    # The Multinomial classifier model
    return clf

def svm_classifier(train_data, tfidf):
    """
    This function helps to build
    the Support Vector Machine model
    for the data and returns them.

    Arguments:
        1. train_data: The input train data as a dict
        with features and class labels.
        2. tfidf: The TFIDF sparse matrix data.

    Return values:
        1. clf: The classifier model build.
    """

    clf = SGDClassifier().fit(tfidf, train_data.target)
    return clf

def random_forest_classifier(train_data, tfidf):
    """
    This function helps to build a Random forest
    model for the text classification task and returns
    the model.

    Arguments:
        1. train_data: The input train data as a dict
        with features and class labels.
        2. tfidf: The TFIDF sparse matrix data.

    Return values:
        1. clf: The classifier model build.
    """

    clf = RandomForestClassifier().fit(tfidf, train_data.target)
    # build a random forest classifier
    return clf

def logistic_regression_classifier(train_data, tfidf):
    """
    This function helps to build a Logistic regression
    classifier model and returns them.

    Arguments:
        1. train_data: The input train data as a dict
        with features and class labels.
        2. tfidf: The TFIDF sparse matrix data.

    Return values:
        1. clf: The classifier model.
    """

    clf = LogisticRegression().fit(tfidf, train_data.target)
    # build a logistic regression classifier
    return clf

def decision_tree_classifier(train_data, tfidf):
    """
    This function helps to build a decision tree classifier
    classifier model and returns them.

    Arguments:
        1. train_data: The input train data as a dict
        with features and class labels.
        2. tfidf: The TFIDF sparse matrix data.

    Return values:
        1. clf: The classifier model.
    """

    clf = DecisionTreeClassifier().fit(tfidf, train_data.target)
    # build a decision tree classifier
    return clf

def print_results(test_data, predicted, accuracy, model):
    """
    This function helps to print out the results to screen.
    Arguments:
        1. test_data: The test data with data, classes and few more
        attributes in a dict format.
        2. predicted: The predicted rating for the test data in an array.
        3. accuracy: The accuracy of the classifier.
        4. model: Type of the model as a string.

    Return values:
        1. None
    """

    print "{1}{0}{1}\n".format(model, '-'*len(model))
    print "Accuracy: {0}\n".format(accuracy)
    print metrics.classification_report(test_data.target, predicted,
                                        target_names = test_data.target_names)
    print metrics.confusion_matrix(test_data.target, predicted)
    # print out the performance measure values


def predict_test_data(train_data, test_data, models_dict,
                      count, tfidf_transformer, train_tfidf):
    """
    This function helps to predict the class labels
    for the test data based on the models.
    Arguments:
        1. train_data: Train data which is a dictionary with features and
        class labels.
        2. test_data: Test data which is a dictionary with features
        and class labels.
        3. models_dict: The models object for Bernoulli and multinomial
        given in a dictionary.
    """

    for model in models_dict:
        # iterate through each model
        print model
        test_tfidf = features.feature_extraction(test_data, count,
                                tfidf_transformer, data = 'test')
        # function call to get TFIDF for test data
        predicted = models_dict[model].predict(test_tfidf)
        # get the predicted values for the test data
        predicted_cv = cross_validation.cross_val_predict(models_dict[model],
                                        train_tfidf, train_data.target,cv=10)
        # value prediction using cross validation
        accuracy_cv = np.mean(predicted_cv == train_data.target)*100
        # calculate accuracy with cross validation
        accuracy = np.mean(predicted == test_data.target)*100
        # accuracy calculation
        print_results(test_data, predicted, accuracy, model)
        # function call to print results
        print_results(train_data, predicted_cv, accuracy_cv, model+' with cv')
        # function call to print results

def main():
    """
    The main function.
    Arguments:
        1. Takes no arguments.
    """

    train_data = data.load_training_data()
    # function call to load training data
    test_data = data.load_test_data()
    # function call to load test data
    count = CountVectorizer()
    # initialize the count vector
    tfidf_transformer = TfidfTransformer()
    # initialize a tfidf transformer
    models_dict = {}
    # empty dict
    train_tfidf = features.feature_extraction(train_data, count,
                                             tfidf_transformer)
    # function call for feature extraction
    bayes = naive_bayes(train_data, train_tfidf)
    # function call to fit the Naive Bayes classifier
    models_dict['Naive Bayes'] = bayes
    # add models to dictionary
    svm = svm_classifier(train_data, train_tfidf)
    # function call to fit SVM Classifier
    models_dict['SVM'] = svm
    # add models to a dictionary
    rand_forest = random_forest_classifier(train_data, train_tfidf)
    # function to build random forest classifier
    models_dict['Random Forest'] = rand_forest
    # add models to dictionary
    logistic = logistic_regression_classifier(train_data, train_tfidf)
    # function call to build logistic regression
    models_dict['Logistic Regression'] = logistic
    # add models to dictionary
    decision_tree = decision_tree_classifier(train_data, train_tfidf)
    # function call for decision tree classifier
    models_dict['Decision Tree'] = decision_tree
    # add model to the dictionary
    predict_test_data(train_data, test_data, models_dict,
                      count, tfidf_transformer, train_tfidf)
    # function call to predict test data

if __name__ == '__main__':
    # start of the program
    main()
    # function call - main
