"""
Name: Anirudh, Kamalapuram Muralidhar
Indiana University
Date: 15th Feb, 2016
Objective: Analysis of iris dataset which can be
downloaded from http://archive.ics.uci.edu/ml/datasets/iris
"""

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sys import argv

def sep_data_by_class_labels(df):
    """
    This function helps to subset
    data based on the class label
    and from there on calculates the
    mean and SD
    """

    unique_labels = frozenset(df.iloc[:,-1])
    # get the unique labels from the data
    for label in unique_labels:
        # iterate through each label
        subset_df = df.loc[df.iloc[:, -1] == label]
        # subset the data based on the label
        calc_mean_and_sd(subset_df, label)
        # function call

def boxplot_data(df):
    """
    This function plots the boxplot
    of the data based on the
    class label and saves the plot
    """

    for feature in (df.columns[:-1]):
        # iterate through each feature
        box_plot = df.boxplot(column = feature, by = df.columns[-1], sym = 'bs',
                    return_type = 'dict', patch_artist = True, fontsize=20,
                    figsize = (22, 10))
        # plot the boxplot for the data
        box_object = box_plot[feature]['boxes']
        # get the box plot objects
        color_list = ['lightgreen','lightblue','pink']
        # list of colors
        for i in xrange(len(box_object)):
            # iterate through each boxplot object
            box_object[i].set(color = 'black', linewidth = 1)
            # set the border color and line width
            box_object[i].set(facecolor = color_list[i])
            # set the face color of the plot
        plt.xlabel("Flower type", fontsize = 25, color='black')
        # set x-axis label
        plt.ylabel("Value", fontsize = 25, color = 'black')
        # set y-axis label
        plt.ylim((0, round(max(df[feature])+0.6)))
        # set the range for the y-axis
        plt.title("Boxplot for feature: {}".format(feature), fontsize=25)
        # set the title of the boxplot
        plt.savefig(feature + '.png')
        # save the plot to directory

def calc_mean_and_sd(df, flower_type = "all"):
    """
    This function takes a pandas DF
    as an input and calculates the
    mean and SD for each of its columns
    and prints the value
    """

    if flower_type == "all":
        # this includes all flower types
        boxplot_data(df)
        # function call to plot boxplot
        state = "Results which includes all flower types"
        print state,'\n','='*len(state)
    else:
        state = "Result for flower type: {0}".format(flower_type)
        print state, '\n', '='*len(state)
    del state
    # delete the variable 'state'
    for feature in df.columns[0:-1]:
        # iterate over all the features
        print("Feature: {0}".format(feature))
        print("Mean: {0:4f}".format(np.mean(df[feature])))
        # calculate the mean and print its value
        print("SD: {0:4f}\n".format(np.var(df[feature])**(0.5)))
        # calculate the SD and print its value
    return df

def read_input_file(inp_file, headers_file):
    """
    This function reads the input file
    and returns the data in a pandas data frame
    form
    """

    with open(headers_file) as col_names:
        # read the headers file
        col_names_list = col_names.read().split(",")
        # get the col headers in a list by splitting with ","

    return pd.read_csv(inp_file, header = None,
                        names = col_names_list)
    # return the data in a pandas dataframe


if __name__ == '__main__':
    # start of the program
    inp_file = argv[1]
    # get the input file as a sys argv
    header_file = argv[2]
    # header file for iris dataset
    matplotlib.style.use('ggplot')
    # define the style of plot which we will be using
    iris_df = read_input_file(inp_file, header_file)
    # function call to get the data as a pandas DF
    calc_mean_and_sd(iris_df)
    # function call to calculate mean and SD
    sep_data_by_class_labels(iris_df)
    # function call
