This is a README file which corresponds to the decision tree algorithm.

1. This program is called by calling the main.py function with sys arguments as the input data in a comma separated formated file along with the impurity measure, which is gini or entropy.

2. Then, inorder to construct the decision tree, we find the best feature and the best splitting value based on the impurity measure. We then grow the tree based on this and finally construct the tree using recursion.

3. After this we display the tree.

4. Then we perform k-fold cross validation on the model that we built with the input data.

5. Finally the accuracy measure is printed out to screen.