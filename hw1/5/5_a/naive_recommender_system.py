"""
Name: Anirudh Kamalapuram Muralidhar
Indiana University
Date: 31th January, 2016
Objective: To build a recommender system
based on a naive algorithm
"""

from distance import *
from data_process import *
import numpy as np

def mean_absolute_difference(user_rating_dict, predict_rating_dict):
    """
    This function helps to calculate the 
    mean absolute difference on the predicted 
    and observed data and prints it
    """
    
    total_diff = 0.0
    count = 0
    for user in user_rating_dict.iterkeys():
        # iterate through each user
        available_movies = user_rating_dict[user]
        # movies "user" has already rated
        for movie in available_movies.iterkeys():
            # iterate through each movie
            try:
                total_diff += abs(predict_rating_dict[user][movie] - available_movies[movie])
                count += 1
            except KeyError:
                pass
    print total_diff, count
    return total_diff/count
     
    
def predict_user_rating(user_rating_dict, movie_dict,user_id,
                        predicted_user_rating_dict):
    """
    This function helps us to find the prediction for given 
    user ID for the movies that he has not seen
    """
    
    for movie in movie_dict.iterkeys():
        # iterate through each movie
        users_seen_movie_dict = movie_dict[movie]
        # get the users who saw the movie
        j = users_seen_movie_dict.copy()
        for seen_user in j.iterkeys():
            # iterate through each user
            if seen_user != user_id:
                # to make both of them aren't same user
                try:
                    users_seen_movie_dict.pop(user_id)
                except KeyError:
                    pass
                predicted_rating = sum(users_seen_movie_dict.values())/len(users_seen_movie_dict)
                if user_id in predicted_user_rating_dict:
                # check if user is already predicted
                    predicted_user_rating_dict[user_id][movie] = predicted_rating
                # update the predicted rating dictionary
                else:
                    predicted_user_rating_dict[user_id] = {movie:predicted_rating}
                    # add new user predicting rating  

if __name__ == '__main__':
    # start of the program
    training = ['u1.base','u2.base','u3.base','u4.base','u5.base']
    test = ['u1.test','u2.test','u3.test','u4.test','u5.test']

    mad_final = 0
    # initial value for MAD
    for i in xrange(len(training)):
        user_rating_dict, movie_dict = get_input_data(training[i])
        # function call
        predicted_user_rating_dict = {}
        # empty predicted user rating
        for user_id in user_rating_dict.iterkeys():
            print user_id
            predict_user_rating(user_rating_dict, movie_dict,user_id,
                                predicted_user_rating_dict)
            # function call
        user_rating_dict, movie_dict = get_input_data(test[i])  
        # get the user based and movie based rating
        mad = mean_absolute_difference(user_rating_dict, predicted_user_rating_dict)
        # function call
        mad_final += mad
        write_to_file(training[i], test[i], mad, "naive_recommender_op.txt")
        # function call
    write_to_file("Average of all training", "Average of all test", mad_final/len(test),
                "naive_recommender_op.txt")
    # function call