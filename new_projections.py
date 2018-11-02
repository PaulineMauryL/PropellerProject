import numpy as np
import pandas as pd
from prop_info import extreme_points
import scipy.linalg
from scipy.optimize import curve_fit

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


'''
def find_border_points(projection):
    #Find point at the border of the given points
    right = []
    left = []

    for elem in projection: 
        max_point, min_point, _, _, _ = extreme_points(elem)

        right.append(max_point)
        left.append(min_point)

    return right, left
'''





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



#plan = planes[i], segment_down = segments['points'][proj-1], segment_up = segments['points'][proj], nb_point)
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

    order = 2    # 1: linear, 2: quadratic
    if order == 1:
        # best-fit linear plane
        A = np.c_[data[:,0], data[:,1], np.ones(data.shape[0])]
        C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])    # coefficients
        
        # evaluate it on grid
        Z = C[0]*X + C[1]*Y + C[2]
        
        # or expressed using matrix/vector product
        #Z = np.dot(np.c_[XX, YY, np.ones(XX.shape)], C).reshape(X.shape)

    elif order == 2:
        # best-fit quadratic curve
        A = np.c_[np.ones(data.shape[0]), data[:,:2], np.prod(data[:,:2], axis=1), data[:,:2]**2]
        C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])
        #print("C\n")
        #print(C)
        # evaluate it on a grid
        #Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)
        Z = C[4]*X**2. + C[5]*Y**2. + C[3]*X*Y + C[1]*X + C[2]*Y + C[0]
        #print("Z\n")
        #print(Z)

    #plot_least_squares(X, Y, Z, data)

    return C

def assign_points(C_up, up):
    right = []
    left = []
    
    C = C_up[0:4]

    for index, point in up.iterrows():
        z = ls_plane(C_up, point[0], point[1])
        if(z <= point[2]):
            right.append(index)
        else:
            left.append(index)

    right_points = (up.loc[right]).reset_index(drop=True)
    left_points = (up.loc[left]).reset_index(drop=True)

    return right_points, left_points

def interpolate_points(up1):
    data = np.c_[up1.values[:,0], up1.values[:,1]]
    y = up1.values[:,2]

    sigma = np.ones(len(data))
    sigma[[-1, -2]] = 0.05  #assign more weight to border points
    popt, pcov = curve_fit(model_func, data, y, sigma=sigma)    
    return popt


def ls_plane(C, X, Y):
    return C[4]*X**2. + C[5]*Y**2. + C[3]*X*Y + C[1]*X + C[2]*Y + C[0]

def model_func(data, a, b, c, d, e, f, g, h):    
        return a*data[:,0]**3 + b*data[:,1]**3 + c*data[:,0]**2 + d*data[:,1]**2 + e*data[:,0]*data[:,1] + f*data[:,0] + g*data[:,1] + h * np.ones([data[:,0].shape[0],])

def points_from_curve(up_right_border, up_left_border, nb_points):
    up_right = []
    range_X_up_r = np.linspace(up_right_border[0], up_left_border[0], nb_points)
    range_Y_up_r = np.linspace(up_right_border[1], up_left_border[1], nb_points)
    
    #for x in range_X_up_r:
    #    for y in range_Y_up_r:
    data = np.c_[range_X_up_r, range_Y_up_r]
    z = model_func(data, *up_right_popt)
    
    return np.asarray([range_X_up_r, range_Y_up_r, z])