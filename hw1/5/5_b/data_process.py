import pandas as pd

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

def get_attribute_dict():
    """
    This function returns the various
    attributes to be used in a binary encoding
    format and returns it
    """
    
    attr_dict = {}
    attr_tuple = ('M','F','0+','16+','36+','60+')
    with open('u.occupation') as f:
        for line in f:
            attr_dict[line.strip()] = 0
    for attr in attr_tuple:
        attr_dict[attr] = 0
    return attr_dict


def write_to_file(train_filename, test_filename, mad, output_file, dist = ''):
    """
    Write the MAD calculated for train and test file
    """
    
    if not dist:
        with open(output_file, "a") as f:
            f.write("Train file:{}\nTest file:{}\nMAD:{}\n\n".format(train_filename,
                                                    test_filename, mad))
    else:
        with open(output_file, "a") as f:
            f.write("Train file:{}\nTest file:{}\nDistance:{}\nMAD:{}\n\n".format(train_filename,
                                                    test_filename, dist, mad))


def get_user_information(input_file, attr_dict):
    """
    This function gets thuser details
    which facilitates to find similarity 
    """
    
    user_info_dict = {}
    # empty user info dict
    with open('u.user') as f:
        for line in f:
            data = line.split('|')
            user_info_dict[data[0]] = attr_dict.copy()
            user_info_dict[data[0]][data[2]] = 1
            user_info_dict[data[0]][data[3]] = 1
            if 0 < int(data[1]) <= 15:
                user_info_dict[data[0]]['0+'] = 1
            elif 16 < int(data[1]) <= 35:
                user_info_dict[data[0]]['16+'] = 1
            elif 36 < int(data[1]) <= 60:
                user_info_dict[data[0]]['36+'] = 1
            elif 60 < int(data[1]):
                user_info_dict[data[0]]['60+'] = 1
    return user_info_dict
                    

def get_input_data(input_file):
    """
    This function helps to get the input
    data in a structured form and 
    return them as a pandas data frame
    """
    
    user_rating_dict = {}
    # empty dictionary for users
    movie_dict = {}
    # dictionary for movie
    with open(input_file) as f:
    # open the input file
        for line in f:
            # iterate through each line of the file
            data = line.split()
            # split each line with white space
            if data[0] in user_rating_dict:
                # create dictionary of user ratings
                user_rating_dict[data[0]][data[1]] = float(data[2])
            else:
                user_rating_dict[data[0]] = {data[1]:float(data[2])}
            
            if data[1] in movie_dict:
                # create dict with movie id
                movie_dict[data[1]][data[0]] = float(data[2])
            else:
                movie_dict[data[1]] = {data[0]:float(data[2])}

    return user_rating_dict, movie_dict