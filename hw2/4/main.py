"""
Name: Anirudh, Kamalapuram Muralidhar
Indiana University
Start date: 19th Feb, 2016
Objective: To construct a decision tree based on
        greedy algorithm

Dataset are taken from: http://archive.ics.uci.edu/ml/datasets.html
"""

from sys import argv, setrecursionlimit
from tree import main

if __name__ == '__main__':
    # start of the program
    input_file = argv[1]
    # get the input file as a sys argv
    impurity_measure_str = argv[2]
    # get the impurity measure as a sys argv
    setrecursionlimit(1000000)
    # set maximum recursion depth
    main(input_file, impurity_measure_str)
    # function call
