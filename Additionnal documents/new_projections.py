import numpy as np
import pandas as pd
import math
from prop_info import extreme_points, aerofoil_width
import scipy.linalg
from scipy.optimize import curve_fit
from myMathFunction import *
from plot_projections import plot_projection_up_down, D2_plot, plot_least_squares_latex, plot_interpolation_both_sides_no_generation #plot_interpolation_side




def points_of_plane(propeller_coords, plane, nb_projections, plane_nb):
    ''' Get the points to consider for projection on ONE plane
        INPUT: Dataframe points of blade, 
                np.array plane equation, 
                scalar delta
        OUTPUT: Dataframe points to consider
    '''
    delta = 0.05
    count=0
    max_aerofoil_width = aerofoil_width(propeller_coords)

    threshold = 30

    old_plane_above = plane[:]
    old_plane_below = plane[:]
    above_plane = plane[:] + [0,0,0,delta]
    below_plane = plane[:] - [0,0,0,delta]

    points_taken = 0
    index_segment = []

    update_plane = True

    while(points_taken == 0):
        count = count + 1

        for index, point in propeller_coords.iterrows(): 
            point_mult = np.append(point, 1)   

            if(point_mult @ old_plane_above < 0 and point_mult @ above_plane >= 0):
                points_taken += 1
                index_segment.append(index) 
                update_plane = False
                break
            elif(point_mult @ old_plane_below > 0 and point_mult @ below_plane <= 0):
                points_taken += 1
                index_segment.append(index) 
                update_plane = False
                break

        if(update_plane):
            old_plane_above = above_plane[:]
            above_plane = above_plane[:] + [0,0,0,delta]

            old_plane_below = below_plane[:]
            below_plane = below_plane[:] - [0,0,0,delta]

    taken = propeller_coords.loc[index_segment].copy()

    #print("init")
    #print(count)

    #print(delta)

    while(points_taken < threshold):   # while less than threshold nb of pts are added at each iteration, continue to add points
        #nb_pts_at_a_time = 0
        count += 1
        if(count > 100):  #farther than 100*0,05 = 5mm then stop
            break
        for index, point in propeller_coords.iterrows(): 
            point_mult = np.append(point, 1)                                #[x, y, z] to [x, y, z, 1]: to multiply with plane [a, b, c, d]

            if( (point_mult @ old_plane_above < 0 and point_mult @ above_plane >= 0) or (point_mult @ old_plane_below > 0 and point_mult @ below_plane <= 0) ): #if point between in interval delta between planes
                to_add = True

                for _, already_taken in taken.iterrows(): 
                    distance = math.sqrt( (point[0] - already_taken[0])**2 + (point[1] - already_taken[1])**2 )
                    #100:à l'assitant. #50 bien. #40 mieux. #33: moins bien. #25: pas assez (forme bizarres)
                    if(  distance < (max_aerofoil_width/40)  ): #if not far enough of already taken  
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

        #threshold -= 1
    #print("count")
    #print(count)

    #print("points_taken")
    #print(points_taken)
    #print(threshold)  # --> around 19 to 21 taken instead of 30
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
    nb_projections = len(planes) - 2

    for i, plane in enumerate(planes):
        if(i==0 or i == (len(planes)-1)):   #do not take into account first plane (hub) and last plane (extremity)
            pass
        else:
            points.append( points_of_plane(propeller_coords, plane, nb_projections, i) )
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

    x_l = np.linspace(-20,10, 100)
    y_l = []
    for x in x_l:
        y_l.append( ls_plane(C_up, x) )

    #plot_least_squares_latex(right_points, left_points, x_l, y_l)

    return right_points, left_points

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
    
    #print("length of x")
    #print(len(x))
    #errors = []
    #parameters = []
    #sigma = np.ones(len(x))
    #sigma[[-1, -2]] = 1  #assign more weight to border points
    #print("error of funct_{} is {}".format(i, np.sqrt( np.diag(pcov) )))
    popt_4, _ = curve_fit(func_4, x, y) 
    
    return popt_4 #, degree

#################################################################################################################
#################################################################################################################
#################################################################################################################
def add_border_points(right_points, left_points):     #report for contuity
    #add extreme points to have same extremity on both sides
    #print(len(right_points))
    #print(len(left_points))
    
    _, high_right, low_right = extreme_points(right_points)
    _, high_left,  low_left  = extreme_points(left_points)
    #minx_r = np.min(right_points[0])
    #maxx_r = np.max(right_points[0])
    #minx_l = np.min(left_points[0])
    #maxx_l = np.max(left_points[0])

    if(high_right[0] > high_left[0]):
        left_points.loc[len(left_points)] = high_right
    else:
        right_points.loc[len(right_points)] = high_left

    if(low_right[0] < low_left[0]):
        left_points.loc[len(left_points)] = low_right
    else:
        right_points.loc[len(right_points)] = low_left

    return right_points.sort_values('X').reset_index(drop=True), left_points.sort_values('X').reset_index(drop=True) #sort for plot


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
    
    right_points, left_points = add_border_points(right_points, left_points) #for continuity
    
    #right_points.to_csv(name + 'right_points_1.csv', index = False)
    #left_points.to_csv(name + 'left_points_1.csv', index = False)
    if(len(right_points)> 5):
        right_popt = interpolate_points(right_points)
    else:
        #print("Plane does not have enough points for interpolation")
        right_popt = -1

    if(len(left_points)> 5):
        left_popt = interpolate_points(left_points)
    else:
        #print("Plane does not have enough points for interpolation")
        left_popt = -1
    
    #plot_interpolation_both_sides_no_generation(right_popt, right_points, left_popt, left_points)

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

    i=0
    for one_plane_point in all_planes_points:
        #print("Number "+str(i))
        i=i+1
        right_popt, right_points, left_popt, left_points = projection_results(one_plane_point)
        #print(" \n")

        right_param.append(right_popt)
        left_param.append(left_popt)
        right_pts.append(right_points)
        left_pts.append(left_points)


    return right_param, left_param, right_pts, left_pts


#################################################################################################################
#################################################################################################################
#################################################################################################################

def generate_points(right_popt, right_points, left_popt, left_points):  #generate for X-foil
    _, highest, lowest = extreme_points(right_points)
    
    a = np.linspace(lowest[0], highest[0], 16)
    range_x = highest[0] - lowest[0]

    b = np.linspace(lowest[0] + 0.01,        lowest[0] + range_x/10, 5)
    c = np.linspace(lowest[0] + range_x*0.9, highest[0] - 0.01     , 5)

    x = np.sort(np.hstack((a, b, c)))
    
    #x = np.linspace(lowest[0], highest[0], 100)

    #print(x)
    if(type(right_popt) == int or type(left_popt) == int):
        #print("Plane does not have enough points for interpolation")
        return -1, -1, -1
    else:
        y_right = func_4(x, *right_popt)
        y_left = func_4(x, *left_popt)

        y_first = (y_right[0] + y_left[0])/2                   #for continuity
        y_end  = (y_right[-1] + y_left[-1])/2

        y_right[0] = y_first
        y_left[0] = y_first

        y_right[-1] = y_end
        y_left[-1] = y_end

    return x, y_right, y_left

def get_generated_points(right_param, left_param, right_pts, left_pts, delta_d):
    x_list = []
    y_right_list = []
    y_left_list = []
    removed = []
    position = []

    delta_d = abs(delta_d)
    delta_tot = 0
    print("here")
    plot_interpolation_both_sides_no_generation(right_param[1], right_pts[1], left_param[1], left_pts[1])

    for i in range(len(right_param)):
        x, y_right, y_left = generate_points(right_param[i], right_pts[i], left_param[i], left_pts[i])
        delta_tot += delta_d

        if(type(x) == int):
            print("Plane {} has been removed".format(i))
            removed.append(i)
        else:
            x_list.append(x)
            y_right_list.append(y_right)
            y_left_list.append(y_left)    
            position.append(delta_tot)
            
    right = [] 
    left = []
    for i in range(len(right_param)):
        if i not in removed:
            right.append(right_pts[i])
            left.append(left_pts[i])
            
    return x_list, y_right_list, y_left_list, right, left, position, len(removed)


