import numpy as np
import pandas as pd
from prop_info import extreme_points
import scipy.linalg
from scipy.optimize import curve_fit
from myMathFunction import point_on_plane
from plot_projections import * #plot_interpolation_side



def get_all_points_for_projections(planes, segments, nb_seg, resolution):
    '''Get the points next to each planes on both sides'''
    up = []
    down = []
    labels = ['X', 'Y', 'Z']


    for proj in range(1, nb_seg):
        up_i, down_i = get_points_to_project_on_plane(planes[proj], segments['points'][proj-1], segments['points'][proj], resolution)
        up.append(pd.DataFrame(up_i, columns = labels))
        down.append(pd.DataFrame(down_i, columns = labels))

    return up, down


def get_points_to_project_on_plane(plane, segment_down, segment_up, resolution):
    '''Get points in a range 'resolution' around the plan'''
        #print(segment_down.shape)
    upper_plane = plane[:] + [0,0,0,resolution]
    lower_plane = plane[:] - [0,0,0,resolution]
    
    idx_up = []
    for index, point in enumerate(segment_up):
        point_mult = np.append(point, 1)
        if(point_mult @ lower_plane < 0 and point_mult @ plane >= 0):
            idx_up.append(index)
            #print("here")
    idx_down = []
    for index, point in enumerate(segment_down):
        point_mult = np.append(point, 1)
        if(point_mult @ plane < 0 and point_mult @ upper_plane >= 0):
            idx_down.append(index)
            #print("here")

    up = segment_up[idx_up]
    down = segment_down[idx_down]

    return up, down



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

    for index, point in up.iterrows():
        y = ls_plane(C_up, point[0])
        if(y <= point[1]):
            right.append(index)
        else:
            left.append(index)

    right_points = (up.loc[right]).reset_index(drop=True)
    left_points = (up.loc[left]).reset_index(drop=True)

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

    popt, _ = curve_fit(model_func, x, y, sigma=sigma) 

    return popt


def ls_plane(C, X):
    '''Least square equation to find the best line to separate the data
    '''
    return C[3]*X**3 + C[2]*X**2 + C[1]*X + C[0]

def model_func(data, a, b, c, d):    
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


def project_points_on_plane(up_right_pts, dn_right_pts, up_left_pts, dn_left_pts, plan1):
    proj_right = []
    proj_left = []
    labels = ['X', 'Y', 'Z']
    
    for i, _ in up_right_pts.iterrows():
        #print(up_right_pts.iloc[i])
        proj_right.append(point_on_plane(up_right_pts.iloc[i], dn_right_pts.iloc[i], plan1))
        proj_left.append( point_on_plane(up_left_pts.iloc[i],  dn_left_pts.iloc[i],  plan1))
        
    proj_right_df = pd.DataFrame(proj_right, columns = labels)
    proj_left_df  = pd.DataFrame(proj_left,  columns = labels)
    
    return proj_right_df, proj_left_df


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






def get_points(propeller_coords, planes, delta):
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
            points.append( points_of_plane(propeller_coords, plane, delta) )

    return points


def points_delta(propeller_coords, plane, delta):
    ''' Get the points to consider for projection on A SIDE of A plane
        INPUT: Dataframe points of blade, 
                np.array plane equation, 
                scalar delta
        OUTPUT: indexes of selected points to consider
    '''    
    index_segment = []
    old_plane = plane[:]
    new_plane = plane[:] + [0,0,0,delta]
    threshold = 5
    nb_pts_at_a_time = 0

    while(nb_pts_at_a_time < threshold):   # while less than threshold nb of pts are added at each iteration, continue to add points
        nb_pts_at_a_time = 0

        for index, point in propeller_coords.iterrows(): 
            point_mult = np.append(point, 1)                                #[x, y, z] to [x, y, z, 1]: to multiply with plane [a, b, c, d]

            if(point_mult @ old_plane < 0 and point_mult @ new_plane >= 0): #if point between in interval delta between planes
                nb_pts_at_a_time = nb_pts_at_a_time + 1
                index_segment.append(index)                                 #take index of point

        old_plane = new_plane[:]
        new_plane = new_plane[:] + [0,0,0,delta]                            #consider next interval at next iteration


    for index, point in propeller_coords.iterrows(): #take a last one in case last iteration was in between a row of pts
        point_mult = np.append(point, 1)
        if(point_mult @ old_plane < 0 and point_mult @ new_plane >= 0):
            index_segment.append(index)

    return index_segment

def points_of_plane(propeller_coords, plane, delta):
    ''' Get the points to consider for projection on ONE plane
        INPUT: Dataframe points of blade, 
                np.array plane equation, 
                scalar delta
        OUTPUT: Datafreme points to consider
    '''
    index_segment = []
    old_plane = plane[:]
    threshold = 5
    nb_pts_at_a_time = 0

    ## Upper side
    new_plane = plane[:] + [0,0,0,delta]
    
    while(nb_pts_at_a_time < threshold):   # while less than threshold nb of pts are added at each iteration, continue to add points
        nb_pts_at_a_time = 0

        for index, point in propeller_coords.iterrows(): 
            point_mult = np.append(point, 1)                                #[x, y, z] to [x, y, z, 1]: to multiply with plane [a, b, c, d]

            if(point_mult @ old_plane < 0 and point_mult @ new_plane >= 0): #if point between in interval delta between planes
                nb_pts_at_a_time = nb_pts_at_a_time + 1
                index_segment.append(index)                                 #take index of point

        old_plane = new_plane[:]
        new_plane = new_plane[:] + [0,0,0,delta]                            #consider next interval at next iteration


    for index, point in propeller_coords.iterrows(): #take a last one in case last iteration was in between a row of pts
        point_mult = np.append(point, 1)
        if(point_mult @ old_plane < 0 and point_mult @ new_plane >= 0):
            index_segment.append(index)


    ## Lower side


    plane_points = propeller_coords.loc[index].copy()
    
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



def get_all_projections(planes, all_plane_points):
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

    for i, one_plane_point in enumerate(all_planes_point):
        right_popt, right_points, left_popt, left_points = projection_results(one_plane_point, "prop" + i)
        plot_interpolation_both_sides(right_popt, right_points, left_popt, left_points, "propeller_no_weight")

        right_param.append(right_popt)
        left_param.append(left_popt)
        right_pts.append(right_pts)
        left_pts.append(left_pts)

    return right_param, left_param, right_pts, left_pts