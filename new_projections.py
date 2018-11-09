import numpy as np
import pandas as pd
from prop_info import extreme_points
import scipy.linalg
from scipy.optimize import curve_fit
from myMathFunction import point_on_plane
from plot_projections import * #plot_interpolation_side

def edges_projection(up, dn, planes):
    '''Project the line of each side'''
    
    up_edges, dn_edges = edges_projection(up, dn)
    ##############################################################
    #Project upper and lower edge on plan
    edge_on_plane = 0
    ##############################################################
    return edge_on_plane


def interpolations(up, dn):
    '''Get all interpolated edges'''
    up_edges = []
    dn_edges = []
    for i, _ in enumerate(up):
        up_edges.append( interpolation_edge(up[i]) )
        dn_edges.append( interpolation_edge(dn[i]) )

    return up_edges, dn_edges


def interpolation_edge(up):
    '''Get edge on one side linking right to left side'''
    up_right, up_left = find_border_points(up)
    ##############################################################
    #Line that goes from right to left through the points of up
    interp_line = 0
    ##############################################################

    return interp_line




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
    #https://gist.github.com/amroamroamro/1db8d69b4b65e8bc66a6
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
    #data = np.c_[up1.values[:,0], up1.values[:,1]]
    x = up1.values[:,0]
    y = up1.values[:,1]
    #z = up1.values[:,2]
    sigma = np.ones(len(x))
    sigma[[-1, -2]] = 1  #assign more weight to border points
    #print("data0 is {} of type {}".format(data[:,1], type(data[:,1])))
    popt, _ = curve_fit(model_func, x, y, sigma=sigma) 
    #print("done")  
    return popt

def function_poly2d(data, A, B, C, D, E, F):
    x = data[:,0]
    y = data[:,1]
    return A * x ** 2  + B * y ** 2 + C * x * y + D * x + E * y + F

def ls_plane(C, X):
    return C[3]*X**3 + C[2]*X**2 + C[1]*X + C[0]

def model_func(data, a, b, c, d):    
    #return a*data[:,0]**3 + b*data[:,1]**3 + c*data[:,0]**2 + d*data[:,1]**2 + e*data[:,0]*data[:,1] + f*data[:,0] + g*data[:,1] + h * np.ones([data[:,0].shape[0],])
    #return a*(data[:,0]**3) + b*(data[:,1]**3) + c * np.ones([data[:,0].shape[0],])
    return a*data[:]**3 + b*data[:]**2 + c*data[:] + d

def points_from_curve(up_right_points, popt):

    data = np.c_[up_right_points.values[:,0], up_right_points.values[:,1]]
    z = model_func(data, *popt)
    up_right_points["Z"] = z
    '''
    range_X_up_r = np.linspace(up_right_border[0], up_left_border[0], nb_points)
    range_Y_up_r = np.linspace(up_right_border[1], up_left_border[1], nb_points)
    
    interpolated_pts_up = np.zeros((len(range_X_up_r), 3))
    #interpolated_pts_dn = np.zeros((len(range_X_up_r), 3))

    #for x in range_X_up_r:
    #    for y in range_Y_up_r:
    data = np.c_[range_X_up_r, range_Y_up_r]
    z_up = function_poly2d(data, *up_right_popt)
    #z_dn = model_func(data, *dn_right_popt)

    interpolated_pts_up[:, 0] = range_X_up_r
    interpolated_pts_up[:, 1] = range_Y_up_r
    interpolated_pts_up[:, 2] = z_up

    #interpolated_pts_dn[:, 0] = range_X_up_r
    #interpolated_pts_dn[:, 1] = range_Y_up_r
    #interpolated_pts_dn[:, 2] = z_dn   
    '''
    return up_right_points #interpolated_pts_up #, interpolated_pts_dn #np.asarray([range_X_up_r, range_Y_up_r, z])  #TO DO: retourner tableaux nb_points * 3. Zip ?


#projections = proj_right
#projections.extend(proj_left)
#labels = ['X', 'Y', 'Z']
#pd.DataFrame(projections, columns = labels)

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


def add_border_points(up_right_points, up_side1_border, up_side2_border):
    up_right_points = up_right_points.append(pd.DataFrame(up_side1_border.reshape(1, 3), columns = ["X","Y","Z"]))
    up_right_points = up_right_points.append(pd.DataFrame(up_side2_border.reshape(1, 3), columns = ["X","Y","Z"]))

    return up_right_points.sort_values('X').reset_index(drop=True)


def all_border(up_side1_border, up_side2_border, dn_side1_border, dn_side2_border):
    borders_tb = np.zeros([4,3])
    
    borders_tb[0][:] = up_side1_border
    borders_tb[1][:] = up_side2_border
    borders_tb[2][:] = dn_side1_border
    borders_tb[3][:] = dn_side2_border
    
    xmin = min(borders_tb[:,0])
    xmax = max(borders_tb[:,0])
    ymin = min(borders_tb[:,1])
    ymax = max(borders_tb[:,1])
    
    return xmin, xmax, ymin, ymax


def get_points(propeller_coords, planes, size):
    '''Get the points around EACH plane within size distance'''
    points = []

    for i, plane in enumerate(planes):
        if(i==0 or i == (len(planes)-1)):   #do not take into account first plane (hub) and last plane (extremity)
            pass
        else:
            points.append( points_of_plane(propeller_coords, plane, size) )

    return points


def points_of_plane(propeller_coords, plane, size):
    '''Get the points around ONE plane within size distance'''
    upper_plane = plane[:] + [0,0,0,size/2]
    lower_plane = plane[:] - [0,0,0,size/2]
    
    index_segment = []
    for index, point in propeller_coords.iterrows():
        point_mult = np.append(point, 1)

        if(point_mult @ lower_plane < 0 and point_mult @ upper_plane >= 0):
            index_segment.append(index)
            #print("here")
    plane_points = propeller_coords.loc[index_segment].copy()
    
    return plane_points.reset_index(drop=True)

def projection_results(one_plane_point):
    
    side1_border, side2_border, _, _, _ = extreme_points(one_plane_point)
    
    param_sides = find_separation_plane(one_plane_point.values)
    
    right_points, left_points = assign_points(param_sides, one_plane_point)
    
    right_points = add_border_points(right_points, side1_border, side2_border)
    left_points  = add_border_points(left_points,  side1_border, side2_border)
    
    right_popt = interpolate_points(right_points)
    left_popt  = interpolate_points(left_points)
    
    return right_popt, right_points, left_popt, left_points