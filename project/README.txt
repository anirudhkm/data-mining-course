This file represents the README for the final_classifier.py python program.

This is the main to kic off the scripts for the text classification process.

The srcipts uses the files data.py to load the data and features.py for feature selection process.

The twenty newsgroup data is available within the python scikit-learn package itself, for reference the data can be downloaded from http://qwone.com/~jason/20Newsgroups/.


How to run
==========

1. Just run the final_classifier.py file without any system arguments.


Outline
=======

1. First, the scripts loads the train and test data.

2. Next, the feature selection proceedure happens using the TFIDF. 

3. Next, the classifier models are built for various algorithms discussed in the report.

4. Next model is tested using cross validation and test data.

5. Finally, the accuracy, precision, recall, F-1 score along with confusion matrix are reported.