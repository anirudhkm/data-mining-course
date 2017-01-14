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

def write_to_file(train_filename, test_filename, mad, output_file, dist = ''):
    """
    Write the MAD calculated for train and test file
    """
    
    if not dist:
        with open(output_file, "a") as f:
            f.write("Train file:{}\nTest file:{}\nMAD:{}\n\n".format(train_filename,
                                                    test_filename, mad))
    else:
        print 'eeeae'
        with open(output_file, "a") as f:
            f.write("Train file:{}\nTest file:{}\nDistance:{}\nMAD:{}\n\n".format(train_filename,
                                                    test_filename, dist, mad))
        
    
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
