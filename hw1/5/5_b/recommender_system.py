"""
Name: Anirudh Kamalapuram Muralidhar
Indiana University
Date: 31th January, 2016
Objective: To build a recommender system
"""

from distance import *
from data_process import *
import numpy as np

     
def find_top_k_sim_users(similarity_list, k):
    """
    This function returns the top "k" most 
    similar users of the similar_user_dict 
    and returns them
    """
       
    top_k_list = sorted(similarity_list, reverse = True)[:k]
    # get the top 
    return zip(*top_k_list)

def predict_user_rating(user_rating_dict, movie_dict, users_similarity_dict,
                        user_id, predicted_rating_dict, k = 1500):
    """
    This function helps in calculating the 
    predicting of the user based on their 
    similarity
    """
    
    for movie in movie_dict.iterkeys():
        # iterate through each movies
        total_similarity = 0
        weighted_similarity = 0
        similarity_list = []
        # similarity list
        users_who_saw_movie = movie_dict[movie]
        # Get the users who saw the movie
        for seen_user in users_who_saw_movie.iterkeys():
            # iterate through each user who saw the movie
            if user_id != seen_user:
                #similarity_list.append((distance_to_similarity(users_similarity_dict[frozenset((user_id,seen_user))]), users_who_saw_movie[seen_user]))
                similarity = users_similarity_dict[frozenset((user_id,seen_user))]
                total_similarity += similarity
                weighted_similarity += similarity*users_who_saw_movie[seen_user]
            else:
                pass
        #similar_user_list = find_top_k_sim_users(similarity_list, k)
        try:
            predicted_rating = sum(np.array(similar_user_list[0])*np.array(similar_user_list[1]))/sum(similar_user_list[0])
            if not isnan(predicted_rating):
                # get the prediction value
                if user_id in predicted_rating_dict:
                    # check if user is already predicted
                    predicted_rating_dict[user_id][movie] = predicted_rating
                    # update the predicted rating dictionary
                else:
                    predicted_rating_dict[user_id] = {movie:predicted_rating}
                    # add new user predicting rating             
        except Exception, e:
            pass
            
if __name__ == '__main__':
    # start of the program
    training = ['u1.base','u2.base','u3.base','u4.base','u5.base']
    test = ['u1.test','u2.test','u3.test','u4.test','u5.test']
    mad_final  = 0
    for i in xrange(len(training)):
        user_rating_dict, movie_dict = get_input_data(training[i])
        # get the user rating for each movie and also movie rating by users
        attribute_dict = get_attribute_dict()
        # get the various attributes to be used  
        user_information_dict = get_user_information('u.user', attribute_dict)
        # get the information of users stored in a dict
        users_similarity_dict = calcuate_similarity(user_rating_dict, user_information_dict)
        # get the similarity between users
        predicted_rating_dict = {}
        # empty dictionary
        for user_id in user_rating_dict.iterkeys():
                predict_user_rating(user_rating_dict, movie_dict, users_similarity_dict,
                                    user_id, predicted_rating_dict)
                # function call  
        user_rating_dict, movie_dict = get_input_data(test[i])  
    
        mad = mean_absolute_difference(user_rating_dict, predicted_rating_dict)
        # function call
        write_to_file(training[i], test[i], mad, "user_attr_recommend_sys.txt")
        mad_final += mad
    write_to_file("Average of training set", "Average of testing set", mad, "user_attr_recommend_sys.txt")