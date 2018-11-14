import numpy as np
import pandas as pd
import math
from prop_info import extreme_points, aerofoil_width
import scipy.linalg
from scipy.optimize import curve_fit
from myMathFunction import point_on_plane
from plot_projections import plot_projection_up_down, D2_plot #plot_interpolation_side




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
    up.sort_values('X')
    for index, point in up.iterrows():
        y = ls_plane(C_up, point[0])
        y_all.append(y)
        if(y <= point[1]):
            right.append(index)
        else:
            left.append(index)

    right_points = (up.loc[right]).reset_index(drop=True)
    left_points = (up.loc[left]).reset_index(drop=True)

    #DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG
    #plot_projection_up_down(right_points, left_points)
    D2_plot(right_points, left_points, up, y_all, "2d")
    #DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG

    return right_points, left_points

def interpolate_points(up1):
    ''' Find the optimal parameters to fit the data of dataframe 
        It is in 2D: so only thow first columns x and y. 
        INPUT: Dataframe points to interpote
        OUTPUT: optimal parameters
    '''
    x = up1.values[:,0]
    y = up1.values[:,1]

    sigma = np.ones(len(x))
    #sigma[[-1, -2]] = 1  #assign more weight to border points

    popt, pcov = curve_fit(model_func, x, y, sigma=sigma) 
    perr = np.sqrt(np.diag(pcov)) #compute one standard deviation errors on the parameters
    return popt


def ls_plane(C, X):
    '''Least square equation to find the best line to separate the data
    '''
    return C[3]*X**3 + C[2]*X**2 + C[1]*X + C[0]

def model_func(data, a, b, c, d):    ################## CHANGE IN PLOT_PROJECTION TOO
    '''Function to interpolate the edges. Polynomial. 
    INPUT: data: x values because 2d 
            a, b, c, d: parameters to optimize
    OUTPUT: results of the function y = f(x) = a*x^3 + b*x^2+ c*x + d 
    '''

    #return a*data[:,0]**3 + b*data[:,1]**3 + c*data[:,0]**2 + d*data[:,1]**2 + e*data[:,0]*data[:,1] + f*data[:,0] + g*data[:,1] + h * np.ones([data[:,0].shape[0],])
    #return a*(data[:,0]**3) + b*(data[:,1]**3) + c * np.ones([data[:,0].shape[0],])
    return a*data[:]**3 + b*data[:]**2 + c*data[:] + d

def points_from_curve(up_right_points, popt):
    '''
    INPUT: Dataframe points to plot
            popt: optimal parameters of interpolation
    OUTPUT: DataFrame of interpolated points to visualize on plot
    '''
    data = np.c_[up_right_points.values[:,0], up_right_points.values[:,1]]
    z = model_func(data, *popt)
    up_right_points["Z"] = z

    return up_right_points 



def add_border_points(right_points, one_plane_point):
    '''Add the border points to the list of points to interpolate 
    Goal: be more sure that each projection will start and end at same position
    INPUT: Dataframe points to project
            np.array coordinates of border points
    OUTPUT: DataFrame of ordered point to interpolate. (ordered important for plot)
    '''
    side1_border, side2_border, _, _, _ = extreme_points(one_plane_point)

    right_points = right_points.append(pd.DataFrame(side1_border.reshape(1, 3), columns = ["X","Y","Z"]))
    right_points = right_points.append(pd.DataFrame(side2_border.reshape(1, 3), columns = ["X","Y","Z"]))

    return right_points.sort_values('X').reset_index(drop=True)


def get_points(propeller_coords, planes, nb_point_each_side):
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
            points.append( points_of_plane_VERSION2(propeller_coords, plane, nb_point_each_side) )
            print("Points of plane {}".format(i))

    return points



def points_of_plane_VERSION2(propeller_coords, plane, threshold):
    ''' Get the points to consider for projection on ONE plane
        INPUT: Dataframe points of blade, 
                np.array plane equation, 
                scalar delta
        OUTPUT: Dataframe points to consider
    '''
    max_aerofoil_width = aerofoil_width(propeller_coords)

    index_segment = []


    print("Upper")
    index_segment_up = []
    delta = 0.1
    old_plane = plane[:]
    new_plane = plane[:] + [0,0,0,delta]
    points_taken = 0

    while(points_taken == 0):
        for index, point in propeller_coords.iterrows(): 
            point_mult = np.append(point, 1)   

            if(point_mult @ old_plane < 0 and point_mult @ new_plane >= 0):
                points_taken += 1
                index_segment.append(index) 
                index_segment_up.append(index)
                break

        print("delta not ok")
        delta += 0.1                                 #set a plausible delta
        old_plane = new_plane[:]
        new_plane = new_plane[:] + [0,0,0,delta]

    print("delta up is {}", delta)             
    taken_up = propeller_coords.loc[index_segment_up].copy()

    while(points_taken < threshold):   # while less than threshold nb of pts are added at each iteration, continue to add points
        #nb_pts_at_a_time = 0

        for index, point in propeller_coords.iterrows(): 
            point_mult = np.append(point, 1)                                #[x, y, z] to [x, y, z, 1]: to multiply with plane [a, b, c, d]

            if(point_mult @ old_plane < 0 and point_mult @ new_plane >= 0): #if point between in interval delta between planes
                to_add = True

                for _, already_taken in taken_up.iterrows(): 
                    distance = math.sqrt( (point[0] - already_taken[0])**2 + (point[1] - already_taken[1])**2 )

                    if(  distance < (max_aerofoil_width/40)  ): #if not far enough of already taken
                        to_add = False
                if(to_add):
                    print("upper taken {}".format(points_taken))
                    points_taken += 1
                    index_segment.append(index)
                    index_segment_up.append(index) #DEBUG
                    taken_up = propeller_coords.loc[index_segment_up].copy()

        old_plane = new_plane[:]
        new_plane = new_plane[:] + [0,0,0,delta]                            #consider next interval at next iteration

    print("Lower")
    index_segment_dn = []
    delta = 0.1
    ## Lower side
    old_plane = plane[:]
    new_plane = plane[:] - [0,0,0,delta]
    points_taken = 0

    while(points_taken == 0):
        for index, point in propeller_coords.iterrows(): 
            point_mult = np.append(point, 1)   

            if(point_mult @ old_plane > 0 and point_mult @ new_plane <= 0):
                points_taken += 1
                index_segment.append(index) 
                index_segment_dn.append(index)
                break

        delta += 0.1                                 #set a plausible delta
        old_plane = new_plane[:]
        new_plane = new_plane[:] - [0,0,0,delta]

    print("delta down is {}", delta)             
    taken_down = propeller_coords.loc[index_segment].copy()

    while(points_taken < threshold):   # while less than threshold nb of pts are added at each iteration, continue to add points
        #nb_pts_at_a_time = 0

        for index, point in propeller_coords.iterrows(): 
            point_mult = np.append(point, 1)                                #[x, y, z] to [x, y, z, 1]: to multiply with plane [a, b, c, d]

            if(point_mult @ old_plane > 0 and point_mult @ new_plane <= 0): #if point between in interval delta between planes
                to_add = True
                
                for _, already_taken in taken_down.iterrows(): 
                    distance = math.sqrt( (point[0] - already_taken[0])**2 + (point[1] - already_taken[1])**2 )

                    if( distance < (max_aerofoil_width/40) ): #if not far enough of already taken
                        to_add = False

                if(to_add):    
                    print("lower taken{}".format(points_taken))
                    points_taken += 1
                    index_segment.append(index)
                    index_segment_dn.append(index) #DEBUG
                    taken_down = propeller_coords.loc[index_segment_dn].copy()


        old_plane = new_plane[:]
        new_plane = new_plane[:] - [0,0,0,delta]                            #consider next interval at next iteration



    # Takes both sides points
    plane_points = propeller_coords.loc[index_segment].copy()

    return plane_points.reset_index(drop=True)




def projection_results(one_plane_point, name):
    '''Complete function for projection on one plane
        INPUT: points selected for projection
        OUTPUT: optimal interpolation parameters and projected points
                for right and left side
    '''
    #one_plane_point.to_csv(name + 'points0.csv', index = False)

    param_sides = find_separation_plane(one_plane_point.values)
    right_points, left_points = assign_points(param_sides, one_plane_point)
    
    right_points = add_border_points(right_points, one_plane_point)
    left_points  = add_border_points(left_points, one_plane_point)
    
    #right_points.to_csv(name + 'right_points_1.csv', index = False)
    #left_points.to_csv(name + 'left_points_1.csv', index = False)

    right_popt = interpolate_points(right_points)
    left_popt  = interpolate_points(left_points)
    
    return right_popt, right_points, left_popt, left_points



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

    for i, one_plane_point in enumerate(all_planes_points):
        right_popt, right_points, left_popt, left_points = projection_results(one_plane_point, "prop" + str(i))

        right_param.append(right_popt)
        left_param.append(left_popt)
        right_pts.append(right_points)
        left_pts.append(left_points)

    return right_param, left_param, right_pts, left_pts