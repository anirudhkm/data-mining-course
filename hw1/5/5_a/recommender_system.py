"""
Name: Anirudh Kamalapuram Muralidhar
Indiana University
Date: 31th January, 2016
Objective: To build a recommender system
"""

from distance import *
from data_process import *
import numpy as np
from sys import argv

     
def find_top_k_sim_users(similarity_list, k):
    """
    This function returns the top "k" most 
    similar users of the similar_user_dict 
    and returns them
    """
       
    top_k_list = sorted(similarity_list, reverse = True)[:k]
    # get the top 
    return zip(*top_k_list)
    
def predict_user_rating(user_rating_dict, movie_dict, dist_dict,
                        user_id, predicted_user_rating_dict, k = 50):
    """
    This function helps us to find the prediction for given 
    user ID for the movies that he has not seen
    """
    
    for movie in movie_dict.iterkeys():
        # iterate through each movie
        similarity_list = []
        users_seen_movie_dict = movie_dict[movie]
        # get the users who saw the movie
        for seen_user in users_seen_movie_dict.iterkeys():
            # iterate through each user
            if seen_user != user_id:
                # to make both of them aren't same user
                similarity_list.append((distance_to_similarity(dist_dict[frozenset((user_id,seen_user))]), users_seen_movie_dict[seen_user]))
            else:
                pass
        similar_user_list = find_top_k_sim_users(similarity_list, k)
        # function call
        try:
            predicted_rating = sum(np.array(similar_user_list[0])*np.array(similar_user_list[1]))/sum(similar_user_list[0])
            if user_id in predicted_user_rating_dict:
                # check if user is already predicted
                predicted_user_rating_dict[user_id][movie] = predicted_rating
                # update the predicted rating dictionary
            else:
                predicted_user_rating_dict[user_id] = {movie:predicted_rating}
                # add new user predicting rating  
        except Exception:
            pass
            

if __name__ == '__main__':
    # start of the program
    
    no_of_similar_users_int = int(argv[1])
    # get the no of similar users as an sys argv
    training = ['u1.base','u2.base','u3.base','u4.base','u5.base']
    test = ['u1.base','u2.test','u3.test','u4.test','u5.test']
    
    mad_euclidean = 0
    mad_manhattan = 0
    mad_lmax = 0
    # initial value for MAD
    for i in xrange(len(training)):
        user_rating_dict, movie_dict = get_input_data(training[i])
        # function call
        euclidean_dist_dict = calcuate_distance(user_rating_dict, 'euclidean')
        # function call
        manhattan_dist_dict = calcuate_distance(user_rating_dict, 'manhattan')
        # function call
        lmax_dist_dict = calcuate_distance(user_rating_dict, 'lmax')
        # function call
        predicted_user_rating_eucl_dict = {}
        predicted_user_rating_man_dict = {}
        predicted_user_rating_lmax_dict = {}
        # empty predicted user rating
        dist = (euclidean_dist_dict, manhattan_dist_dict, lmax_dist_dict)
        predict = (predicted_user_rating_eucl_dict, predicted_user_rating_man_dict,
                    predicted_user_rating_lmax_dict)
        for user_id in user_rating_dict.iterkeys():
            print user_id
            for j in xrange(len(dist)):
                predict_user_rating(user_rating_dict, movie_dict, dist[j],
                                    user_id, predict[j], k = no_of_similar_users_int)
            # function call  
        user_rating_dict, movie_dict = get_input_data(test[i])  
        # get the user based and movie based rating
        for m in xrange(len(dist)):
            mad = mean_absolute_difference(user_rating_dict, predict[m])
            if m == 0:
                mad_euclidean += mad
                distance_type = 'Euclidean'
            elif m == 1:
                mad_manhattan += mad
                distance_type = 'Manhattan'
            elif m == 2:
                mad_lmax += mad
                distance_type = 'Lmax'
        # function call
            write_to_file(training[i], test[i], mad, "recommender_sys_op.txt", dist=distance_type)
            
    write_to_file("Average of all training", "Average of all test", mad_euclidean/len(test),
                "recommender_sys_op.txt", dist="Euclidean")
    
    write_to_file("Average of all training", "Average of all test", mad_manhattan/len(test),
                "recommender_sys_op.txt", dist="Manhattan")
    
    write_to_file("Average of all training", "Average of all test", mad_lmax/len(test),
                "recommender_sys_op.txt", dist="Lmax")