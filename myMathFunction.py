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


def normalize_vec(vect):
    L = math.sqrt( sum([x**2 for x in vect]) )
    return [x/L for x in vect]



def distance_point_plane(point, plane):
    return abs(point[0]*plane[0] + point[1]*plane[1] + point[2]*plane[2] + plane[3])



def distance_p2p(x1, x2):
    return math.sqrt( (x2[0] - x1[0])**2 + (x2[1] - x1[1])**2 + (x2[2] - x1[2])**2 )



def project_point(point, plane):
    t = - (point[0]*plane[0] + point[1]*plane[1] + point[2]*plane[2] + plane[3]) / (plane[0]**2 + plane[1]**2 + plane[2]**2)
    x = point[0] + plane[0]*t
    y = point[1] + plane[1]*t
    z = point[2] + plane[2]*t
    return [x, y, z]


def point_on_plane(x1, x2, plane):
    vec = x1 - x2
    
    t = - (plane[0]*x1[0] + plane[1]*x1[1] + plane[2]*x1[2] + plane[3]) / (plane[0]*vec[0] + plane[1]*vec[1] + plane[2]*vec[2])
    #t = - plane[3] / (plane[0]*vec[0] + plane[1]*vec[1] + plane[2]*vec[2])

    x = x1[0] + t*vec[0]
    y = x1[1] + t*vec[1]
    z = x1[2] + t*vec[2]
    
    return np.asarray([x, y, z]),