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



def distance_p2p_3d(x1, x2):
    return math.sqrt( (x2[0] - x1[0])**2 + (x2[1] - x1[1])**2 + (x2[2] - x1[2])**2 )

def distance_p2p(x1, x2):
    return math.sqrt( (x2[0] - x1[0])**2 + (x2[1] - x1[1])**2 )


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
    
    return np.asarray([x, y, z])

def least_squares(y, tx):
    """calculate the least squares solution."""
    a = tx.T.dot(tx)
    b = tx.T.dot(y)
    return np.linalg.solve(a, b)



def ls_plane(C, X):
    '''Least square equation to find the best line to separate the data
    '''
    return C[3]*X**3 + C[2]*X**2 + C[1]*X + C[0]
    


def func_2(data, a, b, c)  :   
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''
    return a*data[:]**2 + b*data[:] + c


def func_3(data, a, b, c, d):   
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''
    return a*data[:]**3 + b*data[:]**2 + c*data[:] + d




def func_4(data, a, b, c, d, e):   
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''
    return a*data[:]**4 + b*data[:]**3 + c*data[:]**2 + d*data[:] + e

def func_4_scalar(data, a, b, c, d, e):    
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''
    return a*data**4 + b*data**3 + c*data**2 + d*data + e




def func_5(data, a, b, c, d, e, f):  
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''
    return a*data[:]**5 + b*data[:]**4 + c*data[:]**3 + d*data[:]**2 + e*data[:] + f

def func_6(data, a, b, c, d, e, f, g):   
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''
    return a*data[:]**6 + b*data[:]**5 + c*data[:]**4 + d*data[:]**3 + e*data[:]**2 + f*data[:] + g

def func_7(data, a, b, c, d, e, f, g, h):   
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''
    return a*data[:]**7 + b*data[:]**6 + c*data[:]**5 + d*data[:]**4 + e*data[:]**3 + f*data[:]**2 + g*data[:] + h