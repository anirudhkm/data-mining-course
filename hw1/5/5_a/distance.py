"""
Name: Anirudh Kamalapuram Muralidhar
Indiana University
Date: 31th January, 2016
Objective: Supporting functions to build a recommender system
"""

from math import exp
import numpy as np
from itertools import product
from data_process import *

def cosine_similarity(vec1, vec2):
    """
    This function takes two vectors as 
    an input and finds the cosine similarity
    between them and returns the value
    """
    
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    # converts the input sequence to numpy arrays
    return (sum(vec1*vec2))/(sum(vec1**2)**(0.5)*sum(vec2**2)**(0.5))

def distance_to_similarity(distance):
    """
    This function takes the distance 
    as the input and converts it to a 
    similarity score and returns it
    """
    
    if distance:
        return 1/(1 + distance)
    else:
        return 0.0

def euclidean_distance(vec1_dict, vec2_dict):
    """
    This function computes the Euclidean distance
    between the given two vectors as a dictionary
    and returns the value as a float
    """

    euclidean_dist_float = 0.0
    
    for key in vec1_dict:
        try:
            if key in vec2_dict:
                euclidean_dist_float += (vec1_dict[key] - vec2_dict[key])**2
        except KeyError:
            pass
    return euclidean_dist_float**(0.5)
    
def manhattan_distance(vec1_dict, vec2_dict):
    """
    This function helps to compute the manhattan
    distance between two vectors given as dictionary
    """
    
    manhattan_dist = 0.0
    for key in vec1_dict:
        try:
            if key in vec2_dict:
                manhattan_dist += abs(vec1_dict[key] - vec2_dict[key])
        except KeyError:
            pass
    return manhattan_dist

def lmax_distance(vec1_dict, vec2_dict, r = 10):
    """
    This function helps to calculate the Lmax
    distance between two vectors and returns the value
    """
    
    lmax_dist = 0.0
    for key in vec1_dict:
        try:
            if key in vec2_dict:
                lmax_dist += (vec1_dict[key] - vec2_dict[key])**r
        except KeyError:
            pass
    return lmax_dist**(1/r)
    
def calcuate_distance(user_rating_dict, distance_type = 'Euclidean'):
    """
    This function helps to calculate the 
    distance between various users based 
    on the various distance metrics such as 
    Euclidean, Manhattan and Lmax and writes the 
    data to a file
    """
    
    dist_dict = {}
    # empty dictionary
    indices = product(user_rating_dict.iterkeys(), user_rating_dict.iterkeys())
    # product of the keys
    for i, j in indices:
        # iterate over the users
        vec1_dict = user_rating_dict[i]
        # rating of user 'i'
        vec2_dict = user_rating_dict[j]
        # rating of user 'j'
        if distance_type.lower() == 'euclidean': 
            distance_float = euclidean_distance(vec1_dict, vec2_dict)
            # function call
        elif distance_type.lower() == 'manhattan':
            distance_float = manhattan_distance(vec1_dict, vec2_dict)
            # function call
        elif distance_type.lower() == 'lmax':
            distance_float = lmax_distance(vec1_dict, vec2_dict)
            # function call
        dist_dict[frozenset((i,j))] = distance_float
        # euclidean distance dictionary
    return dist_dict
