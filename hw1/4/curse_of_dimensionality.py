"""
Name: Anirudh Kamalapuram Muralidhar
Indiana Univeristy
4th Feb, 2016
Understanding the curse of dimensionality
"""

import numpy as np
from scipy import spatial
from matplotlib import pyplot
from sys import argv


def plot_graph(r):
    """
    This function takes the r dictionary
    and plots graph with the dimensions in x-axis 
    and the r value in y-axis
    """
    
    fig = pyplot.figure()
    pyplot.plot(r.keys(), r.values())
    # plot the figure
    pyplot.xlabel('Dimensions-k')
    # add a x-label
    pyplot.ylabel('r(k) value')
    # add y-label
    pyplot.suptitle('Plot of dimension Vs r(k) value-N:{}'.format(n))
    # Add plot title
    fig.savefig('{}.jpg'.format(n))
    # save the plot
    pyplot.show()
    # show plot


def get_data_points(n, k, trails = 5):
    """
    This function helps to
    get the data points of k dimensions
    and returns them
    """
    
    data = np.array([])
    # empty nd array
    for i in xrange(n):
        # iterate n times
        point = np.random.uniform(size = k)
        # generate uniform data points of size k
        for i in xrange(trails):
            # run trail for 3 runs
            point += np.random.uniform(size = k)
            # generate again the same points
        point = point/k
        # average of generating points
        data = np.append(data, point)
        # add to data array
    return data.reshape((n, k))
        
def calculate_r(data_dict):
    """
    This function calcuates the r value
    """
    
    r = {}
    # r value dict
    for dim in data_dict:
        # iterate over each dimension
        distance = spatial.distance.pdist(data_dict[dim])
        # calculate the distance between various points
        d_max = max(distance)
        # get the max distance
        d_min = min(distance)
        # get the min distance
        r[dim] = np.log10((d_max - d_min)/d_min)
        # get the r values for each dimensions
    plot_graph(r)
    # function call

def generate_data_points(n):
    """
    Generate n data points with dimension
    k = 1, 2, 3,...100 and then calculates the 
    r values for each dimension
    """

    data_dict = {}
    # empty dict
    for i in xrange(1, 101):
        # iterate through each dimension
        print i
        data = get_data_points(n, i)
        # get the data generated
        data_dict[i] = data
    calculate_r(data_dict)
    # function call

if __name__ == '__main__':
    # start of the program
    n = 1000
    # get the no of data points as a sys argument
    generate_data_points(n)
    # function call
