import numpy as np

def intersection(*args):
    """
    This function performs the
    intersection operation for the input data
    given and returns them as a numpy array
    """

    return tuple(sorted(set(args[0]).intersection(*args[1:])))

def union(*args):
    """
    This function performs the union
    operation for the input data given and
    returns them as a numpy array
    """

    return tuple(sorted(set(args[0]).union(*args[1:])))
