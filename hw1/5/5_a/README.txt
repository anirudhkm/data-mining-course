This README is for the program files 

1. recommender_system.py
2. naive_recommender_system.py

1. recommender_system.py

a) This program is takes the training files from u1.base, u2.base,... u5.base and test files as u1.test, u2.test, ... u5.test.

b) Then based on the input we get dictionaries based on users and movies.

c) Then we proceed to calculate, the distance between users based on Euclidean, Manhattan and Lmax distances.

d) Then for each distance calculated we find the top k users who saw movie j which was not seen by user i. 

e) Based on the distance calculated, we find the similarity and find the users predicted rating based on this.

f) Then, we perform the mean absolute difference with the predicted rating and the user rating from the test data.

g) The output of the file can be seen in recommender_sys_op.txt



2. naive_recommender_system.py

a) This program is similar to recommender_system.py program.

b) But in calculating the user rating we just take the average of the ratings of the person who has seen the movies to assign to the person who has not seen the movie.

c) Then we calculate to the mean absolute difference to find the performance.

d) The output of the file can be seen in naive_recommender_op.txt.



