import numpy as np
import pandas as pd
import math
from prop_info import extreme_points, aerofoil_width
import scipy.linalg
from scipy.optimize import curve_fit
from myMathFunction import point_on_plane
from plot_projections import plot_projection_up_down, D2_plot #plot_interpolation_side




def points_of_plane(propeller_coords, plane):
    ''' Get the points to consider for projection on ONE plane
        INPUT: Dataframe points of blade, 
                np.array plane equation, 
                scalar delta
        OUTPUT: Dataframe points to consider
    '''
    threshold = 25
    delta = 0.1

	max_aerofoil_width = aerofoil_width(propeller_coords)

    old_plane_above = plane[:]
    old_plane_below = plane[:]
    above_plane = plane[:] + [0,0,0,delta]
    below_plane = plane[:] - [0,0,0,delta]

    points_taken = 0
    index_segment = []

    while(points_taken == 0):
        for index, point in propeller_coords.iterrows(): 
            point_mult = np.append(point, 1)   

            if(point_mult @ old_plane_above < 0 and point_mult @ above_plane >= 0):
                points_taken += 1
                index_segment.append(index) 
                break
            elif(point_mult @ old_plane_below > 0 and point_mult @ below_plane <= 0):
                points_taken += 1
                index_segment.append(index) 
                break

        delta += 0.1                                 #set a plausible delta

        old_plane_above = above_plane[:]
        above_plane = above_plane[:] + [0,0,0,delta]

        old_plane_below = below_plane[:]
        below_plane = below_plane[:] - [0,0,0,delta]
           
    taken = propeller_coords.loc[index_segment].copy()



    while(points_taken < threshold):   # while less than threshold nb of pts are added at each iteration, continue to add points
        #nb_pts_at_a_time = 0

        for index, point in propeller_coords.iterrows(): 
            point_mult = np.append(point, 1)                                #[x, y, z] to [x, y, z, 1]: to multiply with plane [a, b, c, d]

            if( (point_mult @ old_plane_above < 0 and point_mult @ above_plane >= 0) or (point_mult @ old_plane_below > 0 and point_mult @ below_plane <= 0) ): #if point between in interval delta between planes
                to_add = True

                for _, already_taken in taken.iterrows(): 
                    distance = math.sqrt( (point[0] - already_taken[0])**2 + (point[1] - already_taken[1])**2 )

                    if(  distance < (max_aerofoil_width/50)  ): #if not far enough of already taken
                        to_add = False

                if(to_add):
                    #print("upper taken {}".format(points_taken))
                    points_taken += 1
                    index_segment.append(index)
                    #index_segment_up.append(index) #DEBUG
                    taken = propeller_coords.loc[index_segment].copy()

        old_plane_above = above_plane[:]
        above_plane = above_plane[:] + [0,0,0,delta]                            #consider next interval at next iteration

        old_plane_below = below_plane[:]
        below_plane = below_plane[:] - [0,0,0,delta]                            #consider next interval at next iteration    


    # Takes both sides points
    plane_points = propeller_coords.loc[index_segment].copy()

    return plane_points.reset_index(drop=True)



def get_points(propeller_coords, planes):
    '''Get the points around EACH plane for projection
    INPUT: Dataframe points of blade, 
                np.array plane equation, 
                scalar delta
    OUTPUT: List of Dataframe, one dataframe of points for each plane 
    '''
    points = []

    for i, plane in enumerate(planes):
        if(i==0 or i == (len(planes)-1)):   #do not take into account first plane (hub) and last plane (extremity)
            pass
        else:
            points.append( points_of_plane(propeller_coords, plane) )
            print("Points of plane {}".format(i))

    return points


#################################################################################################################
#################################################################################################################
#################################################################################################################

def find_separation_plane(data):
    '''Find the parameters of least squares on aerofoil in 2d 
        INPUT: data array
        OUTPUT: optimal parameters on [1, x, x^2, x^3]
    '''
    mn = np.min(data, axis=0)
    mx = np.max(data, axis=0)
    X,Y = np.meshgrid(np.linspace(mn[0], mx[0], 20), np.linspace(mn[1], mx[1], 20))
    XX = X.flatten()
    YY = Y.flatten()

    A = np.c_[np.ones(data.shape[0]), data[:,:1], data[:,:1]**2, data[:,:1]**3]
    C,_,_,_ = scipy.linalg.lstsq(A, data[:,1])
    #plot_least_squares(X, Y, Z, data)
    return C


def ls_plane(C, X):
    '''Least square equation to find the best line to separate the data
    '''
    return C[3]*X**3 + C[2]*X**2 + C[1]*X + C[0]


def assign_points(C_up, up):
    ''' C_up has the parameters of least square of the whole aerofoil
        Use the line to differentiate points on both sides of the line
        INPUT: C_up parameters of least squares
            up Dataframe of points to separate
        OUTPUT: right_points, left_points: points assigned to right or left side
    '''
    right = []
    left = []
    y_all = []
    up = up.sort_values('X')
    for index, point in up.iterrows():
        y = ls_plane(C_up, point[0])
        y_all.append(y)
        if(y < point[1]):
            right.append(index)
        else:
            left.append(index)

    right_points = (up.loc[right]).reset_index(drop=True)
    left_points  = (up.loc[left] ).reset_index(drop=True)

    #DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG
    #plot_projection_up_down(right_points, left_points)
    #D2_plot(right_points, left_points, up, y_all, "Assign points")
    #DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG

    return right_points.sort_values('X').reset_index(drop=True), left_points.sort_values('X').reset_index(drop=True)

#################################################################################################################
#################################################################################################################
#################################################################################################################


def interpolate_points(up1):
    ''' Find the optimal parameters to fit the data of dataframe 
        It is in 2D: so only thow first columns x and y. 
        INPUT: Dataframe points to interpote
        OUTPUT: optimal parameters
    '''
    x = up1.values[:,0]
    y = up1.values[:,1]

    errors = []
    parameters = []
    #sigma = np.ones(len(x))
    #sigma[[-1, -2]] = 1  #assign more weight to border points
    #print("error of funct_{} is {}".format(i, np.sqrt( np.diag(pcov) )))
    popt_3, pcov_3 = curve_fit(func_3, x, y) 
    
    '''
    errors.append(np.sqrt( np.diag(pcov_2) ))   #compute one standard deviation errors on the parameters
    parameters.append(popt_2)
    
    popt_3, pcov_3 = curve_fit(func_3, x, y) 
    errors.append(np.sqrt( np.diag(pcov_3) ))   #compute one standard deviation errors on the parameters
    parameters.append(popt_3)

    popt_4, pcov_4 = curve_fit(func_4, x, y) 
    errors.append(np.sqrt( np.diag(pcov_4) ))   #compute one standard deviation errors on the parameters
    parameters.append(popt_4)

    popt_5, pcov_5 = curve_fit(func_5, x, y) 
    errors.append(np.sqrt( np.diag(pcov_5) ))   #compute one standard deviation errors on the parameters
    parameters.append(popt_5)

    popt_6, pcov_6 = curve_fit(func_6, x, y) 
    errors.append(np.sqrt( np.diag(pcov_6) ))   #compute one standard deviation errors on the parameters
    parameters.append(popt_6)

    popt_7, pcov_7 = curve_fit(func_7, x, y) 
    errors.append(np.sqrt( np.diag(pcov_7) ))   #compute one standard deviation errors on the parameters
    parameters.append(popt_7)

    print(errors)
    min_error = errors.index( min(errors) )
    degree = min_error + 2

    popt = parameters[min_error]
    '''
    return popt_3 #, degree


def func_2(data, a, b, c)  :    ################## CHANGE IN PLOT_PROJECTION TOO
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''
    return a*data[:]**2 + b*data[:] + c


def func_3(data, a, b, c, d):    ################## CHANGE IN PLOT_PROJECTION TOO
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''
    return a*data[:]**3 + b*data[:]**2 + c*data[:] + d

def func_4(data, a, b, c, d, e):    ################## CHANGE IN PLOT_PROJECTION TOO
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''
    return a*data[:]**4 + b*data[:]**3 + c*data[:]**2 + d*data[:] + e

def func_5(data, a, b, c, d, e, f):    ################## CHANGE IN PLOT_PROJECTION TOO
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''
    return a*data[:]**5 + b*data[:]**4 + c*data[:]**3 + d*data[:]**2 + e*data[:] + f

def func_6(data, a, b, c, d, e, f, g):    ################## CHANGE IN PLOT_PROJECTION TOO
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''
    return a*data[:]**6 + b*data[:]**5 + c*data[:]**4 + d*data[:]**3 + e*data[:]**2 + f*data[:] + g

def func_7(data, a, b, c, d, e, f, g, h):    ################## CHANGE IN PLOT_PROJECTION TOO
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''
    return a*data[:]**7 + b*data[:]**6 + c*data[:]**5 + d*data[:]**4 + e*data[:]**3 + f*data[:]**2 + g*data[:] + h

#################################################################################################################
#################################################################################################################
#################################################################################################################


def projection_results(one_plane_point):
    '''Complete function for projection on one plane
        INPUT: points selected for projection
        OUTPUT: optimal interpolation parameters and projected points
                for right and left side
    '''
    #one_plane_point.to_csv(name + 'points0.csv', index = False)

    param_sides = find_separation_plane(one_plane_point.values)
    right_points, left_points = assign_points(param_sides, one_plane_point)
    
    #right_points = add_border_points(right_points, one_plane_point)
    #left_points  = add_border_points(left_points, one_plane_point)
    
    #right_points.to_csv(name + 'right_points_1.csv', index = False)
    #left_points.to_csv(name + 'left_points_1.csv', index = False)

    right_popt = interpolate_points(right_points)
    left_popt = interpolate_points(left_points)
    
    return right_popt, right_points, left_popt, left_points #, right_func_deg, left_func_deg



def get_all_projections(planes, all_planes_points):
    ''' Get all param and points for each projections on each planes
        INPUT: planes equation
                all_plane_points : list of dataframe of selected points for each plane
        OUTPUT: right_param: list of optimal parameters for interpolation of right side (one element of list for one plane)
                right_points: list of interpolated right points on plane (one element of list for one plane)
                left_param: list of optimal parameters for interpolation of left side (one element of list for one plane)
                left_points: list of interpolated left points on plane (one element of list for one plane)
    '''
    right_param = []
    left_param = []
    right_pts = []
    left_pts = []
    right_deg = []
    left_deg = []

    for one_plane_point in all_planes_points:
        right_popt, right_points, left_popt, left_points = projection_results(one_plane_point)

        right_param.append(right_popt)
        left_param.append(left_popt)
        right_pts.append(right_points)
        left_pts.append(left_points)
        #right_deg.append(right_func_deg)
        #left_deg.append(left_func_deg)

    return right_param, left_param, right_pts, left_pts #, right_deg, left_deg