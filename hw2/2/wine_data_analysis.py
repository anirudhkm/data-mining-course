"""
Name: Anirudh, Kamalapuram Muralidhar
Indiana University
Date: 20th Feb, 2016
Objective:
    Analysis of the wine data set.
    a) Provide scatter plots for four most and
    least correlated features.
    b)
    c)

Dataset: The wine dataset can be downloaded from
         http://archive.ics.uci.edu/ml/datasets/wine
"""


from __future__ import division
import numpy as np
import pandas as pd
from itertools import product
import matplotlib.pyplot as plt
from scipy import spatial
from sys import argv

def pearson_correlation_cacl(x, y):
    """
    This function calculates the pearson
    correlation coefficient between the two vectors
    and returns the value as a float.

    Arguments:
        1. x -> sequence of type np array.
        2. y -> sequence of type np array.
    """

    numerator = sum(x*y) - sum(x)*sum(y)/len(x)
    # calculate the numerator part of the formula
    denominator = ((sum(x**2) - sum(x)**2/len(x))*(sum(y**2) - sum(y)**2/len(x)))**(0.5)
    # calculate the denominator part of the formula
    return round(numerator/denominator, 4)
    # return the correlation by rounding it to 4 decimal places

def read_input_data_file(input_file, headers = None):
    """
    This function reads the input file and
    reads them and stores it in a Pandas dataframe.
    It also adds headers if additional headers file is given.
    Finally, it returns the data frame.

    Arguments:
        1. input_file -> input file to be read.

    Default Argument:
        1. headers (None)  -> additional header file is any
    """
    if headers:
        with open(headers) as h:
            # read the headers data file
            col_names = h.read().split(',')
            # get the names of the column headers
    else:
        pass

    return pd.read_csv(input_file, header = None, names = col_names)
    # return the data stored in a pandas data frame format

def find_correlation_btw_features(df):
    """
    This function helps to find the correlation
    between various features and returns them in a dict

    Arguments:
        1. df -> data in a dataframe.
    """

    corr_btw_headers_dict = {}
    # empty dict
    headers_pair = product(df.columns, df.columns)
    # get the header pair indices
    for head_one, head_two in headers_pair:
        # iterate through various pairs of headers
        if head_one != head_two:
            corr_btw_headers_dict[frozenset((head_one,head_two))] = pearson_correlation_cacl(df[head_one],
                                                                df[head_two])
            # calculate the correlation btw various features and store them in a dict
        else:
            pass

    return corr_btw_headers_dict


def plot_data(df, corr_dict):
    """
    This function plots the scatter plot
    between the top 4 and least 4 correlated
    feature
    """

    sorted_header_pairs_by_corr = sorted(corr_dict, key = corr_dict.get)
    # sort based on the correlation
    for head_one, head_two in sorted_header_pairs_by_corr[-4:] + sorted_header_pairs_by_corr[:4]:
        # iterate through each pair of low and high 4 correlated header
        plt.figure()
        # new figure
        plt.scatter(df[head_one], df[head_two], c = 'r', s = 40)
        # plot the scatter plot
        plt.xlabel(head_one)
        # xlabel
        plt.ylabel(head_two)
        # ylabel
        plt.title("{} Vs {} Correlation".format(head_two,head_one))
        # add title to plot
        plt.show()
        # show the plot

def calc_percent_close_points(dist_dict, df):
    """
    Calculate the percentage of close data
    points.
    """

    count = 0
    for i in dist_dict:
        # iterate through each point
        try:
            if df.loc[i]["Class"] == df.loc[dist_dict[i][0]]["Class"]:
                count += 1
        except Exception:
            pass
    print "Percentage of points with class neighbors is {}%".format(round(float(count)*100/len(df),4))

def find_closest_neighbour(df):
    """
    This function helps to find the closest
    neighbor of each row
    """

    distance_dict = {}
    for i in df.index:
        dist_list = []
        for j in df.index:
            if i != j:
                distance = spatial.distance.euclidean(df.loc[i], df.loc[j])
                dist_list.append((j, distance))
        closest_neighbor = sorted(dist_list, key = lambda x:x[1])[0]
        distance_dict[i] = closest_neighbor
    #return distance_dict
    calc_percent_close_points(distance_dict, df)
    for each in df['Class'].unique():
        print 'For class {}'.format(each)
        data = df[df['Class'] == each]
        calc_percent_close_points(distance_dict, data)
        # function call

def zero_one_normalization(df):
    """
    perform 0-1 normalization on the data
    """

    class_column = df["Class"]
    df = df.drop("Class", axis = 1)
    df = (df - df.min())/(df.max() - df.min())
    df["Class"] = class_column
    return df

def z_score_normalization(df):
    """
    Perform z-score normalization
    """
    class_column = df["Class"]
    df = df.drop("Class", axis = 1)
    df = (df - df.mean())/df.std()
    df["Class"] = class_column
    return df

if __name__ == '__main__':
    # start of the main program
    input_file = argv[1]
    # get the input file as a sys argv
    header_file = argv[2]
    # get the header file as sys argv
    data_pd = read_input_data_file(input_file, headers = header_file)
    # function call to read the input data and store them in a pandas DF
    data_without_class = data_pd.drop('Class', axis = 1)
    # remove the class column
    #corr_btw_headers_dict = find_correlation_btw_features(data_without_class)
    # function call to find correlation btw features
    #plot_data(data_pd.copy(), corr_btw_headers_dict)
    # function call to plot data based on correlation
    print "Actual data"
    a = find_closest_neighbour(data_pd)
    # find the closest neighbor to each data
    zero_one_df = zero_one_normalization(data_pd)
    # function call
    print "\n\n0-1 normalized data"
    find_closest_neighbour(zero_one_df)
    # function call
    print "\nz-score normalized data"
    z_score_norm = z_score_normalization(data_pd)
    # function call
    find_closest_neighbour(z_score_norm)
    # function call
