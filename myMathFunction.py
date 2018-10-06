import math
import numpy as np 

def roundup(x):
    '''
    Round up to closest 10th
    '''
    return float(int(math.ceil(x / 10.0)) * 10)

def rounddown(x):
    '''
    Round down to closest 10th
    '''
    return float(int(math.floor(x / 10.0)) * 10)

def findMinMaxDF(data):
    '''
    Find the minimum and maximum values of a dataframe
    '''
    
    min_df = rounddown(np.min(np.min(data)))
    max_df = roundup(np.max(np.max(data)))
    
    return min_df, max_df