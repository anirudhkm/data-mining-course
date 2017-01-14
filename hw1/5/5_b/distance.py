"""
Name: Anirudh Kamalapuram Muralidhar
Indiana University
Date: 31th January, 2016
Objective: Supporting functions to build a recommender system
"""

from math import exp, isnan
import numpy as np
from itertools import product
from data_process import *
from scipy import spatial


def distance_to_similarity(distance):
    """
    This function takes the distance 
    as the input and converts it to a 
    similarity score and returns it
    """
    
    if distance:
        return exp(-distance)
    else:
        return 0.0


def cosine_similarity(vec1, vec2):
    """
    This function takes two vectors as 
    an input and finds the cosine similarity
    between them and returns the value
    """
    
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    # converts the input sequence to numpy arrays
    sim = 1 - spatial.distance.cosine(vec1,vec2)
    if isnan(sim):
        print 'nan found'
        return 1000000
    else:
        return sim


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

def calcuate_similarity(user_rating_dict, user_info_dict):
    """
    This function helps to calculate the 
    distance between various users based 
    on the various distance metrics such as 
    Euclidean, Manhattan and Lmax and writes the 
    data to a file
    """
    
    sim_dict = {}
    # empty dictionary
    indices = product(user_rating_dict.iterkeys(), user_rating_dict.iterkeys())
    # product of the keys
    for i, j in indices:
        # iterate over the users
        if not frozenset((i,j)) in sim_dict:
            vec1 = user_info_dict[i]
            vec2 = user_info_dict[j]
            rating_simi = distance_to_similarity(euclidean_distance(user_rating_dict[i],user_rating_dict[j]))
            sim_dict[frozenset((i,j))] = cosine_similarity(vec1.values(), vec2.values()) + rating_simi
            # euclidean distance dictionary
        else:
            pass
    return sim_dict
    
