This is a README file corresponding to the program wine_data_analysis.py. 

1. The program takes the file wine.data and wine.headers.data as a system argument. 

2. After loading the data as a dataframe, the correlation between all the features are calculated.

3. From this the top 4 and least 4 correlations are taken and plotted.

4. Then, distance between all the data points are found and the closet neighbor is found for each data.

5. Based on this we calculate the percentage of nearest neighbor with the same class is calculated.

6. The above step is repeated for the data with 0-1 normalization and z-score normalization.