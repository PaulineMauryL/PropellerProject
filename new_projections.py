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
        A = np.c_[np.ones(data.shape[0]), data[:,:1], data[:,:1]**2]
        C,_,_,_ = scipy.linalg.lstsq(A, data[:,1])
        #print("C\n")
        #print(C)
        # evaluate it on a grid
        #Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)
        #Z = C[4]*X**2. + C[5]*Y**2. + C[3]*X*Y + C[1]*X + C[2]*Y + C[0]
        #print("Z\n")
        #print(Z)
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
    data = np.c_[up1.values[:,0], up1.values[:,1]]
    z = up1.values[:,2]

    sigma = np.ones(len(data))
    sigma[[-1, -2]] = 0.1  #assign more weight to border points
    popt, pcov = curve_fit(model_func, data, z, sigma=sigma)    
    return popt


def ls_plane(C, X):
    return C[2]*X**2 + C[1]*X + C[0]

def model_func(data, a, b, c, d, e, f, g, h):    
    return a*data[:,0]**3 + b*data[:,1]**3 + c*data[:,0]**2 + d*data[:,1]**2 + e*data[:,0]*data[:,1] + f*data[:,0] + g*data[:,1] + h * np.ones([data[:,0].shape[0],])
    #return a*(data[:,0]**3) + b*(data[:,1]**3) + c * np.ones([data[:,0].shape[0],])

def points_from_curve(up_right_border, up_left_border, nb_points, up_right_popt):

    range_X_up_r = np.linspace(up_right_border[0], up_left_border[0], nb_points)
    range_Y_up_r = np.linspace(up_right_border[1], up_left_border[1], nb_points)
    
    interpolated_pts_up = np.zeros((len(range_X_up_r), 3))
    #interpolated_pts_dn = np.zeros((len(range_X_up_r), 3))

    #for x in range_X_up_r:
    #    for y in range_Y_up_r:
    data = np.c_[range_X_up_r, range_Y_up_r]
    z_up = model_func(data, *up_right_popt)
    #z_dn = model_func(data, *dn_right_popt)

    interpolated_pts_up[:, 0] = range_X_up_r
    interpolated_pts_up[:, 1] = range_Y_up_r
    interpolated_pts_up[:, 2] = z_up

    #interpolated_pts_dn[:, 0] = range_X_up_r
    #interpolated_pts_dn[:, 1] = range_Y_up_r
    #interpolated_pts_dn[:, 2] = z_dn   

    return interpolated_pts_up #, interpolated_pts_dn #np.asarray([range_X_up_r, range_Y_up_r, z])  #TO DO: retourner tableaux nb_points * 3. Zip ?


#projections = proj_right
#projections.extend(proj_left)
#labels = ['X', 'Y', 'Z']
#pd.DataFrame(projections, columns = labels)

def project_points_on_plane(up_right_pts, dn_right_pts, up_left_pts, dn_left_pts, plan1):
    proj_right = []
    proj_left = []
    labels = ['X', 'Y', 'Z']
    
    for i in range(0, up_right_pts.shape[0]):
        proj_right.append(point_on_plane(up_right_pts[i], dn_right_pts[i], plan1))
        proj_left.append( point_on_plane(up_left_pts[i],  dn_left_pts[i],  plan1))
        
    proj_right_df = pd.DataFrame(proj_right, columns = labels)
    proj_left_df  = pd.DataFrame(proj_left,  columns = labels)
    
    return proj_right_df, proj_left_df


def add_border_points(up_right_points, up_side1_border, up_side2_border):
    up_right_points = up_right_points.append(pd.DataFrame(up_side1_border.reshape(1, 3), columns = ["X","Y","Z"]))
    up_right_points = up_right_points.append(pd.DataFrame(up_side2_border.reshape(1, 3), columns = ["X","Y","Z"]))

    return up_right_points


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


def projection_one_plane(up1, dn1, plan1, nb_points):
    # 1. Find border points
    up_side1_border, up_side2_border, _, _, _ = extreme_points(up1)
    dn_side1_border, dn_side2_border, _, _, _ = extreme_points(dn1)
    #print("up_right {}\n".format(up_right))
    
    # 2. Find separating plane
    C_up = find_separation_plane(up1.values)
    C_dn = find_separation_plane(dn1.values)
    # Z = C[4]*X**2. + C[5]*Y**2. + C[3]*X*Y + C[1]*X + C[2]*Y + C[0]
    #print("C_up {}\n".format(C_up))
    
    # 3. Assign point to side  (do it for both sides on both sides)
    up_right_points, up_left_points = assign_points(C_up, up1)
    dn_right_points, dn_left_points = assign_points(C_dn, dn1)
    #print("right_points_up_shape {}\n".format(up_right_points.shape))
    
    # Add border points to fit
    up_right_points = add_border_points(up_right_points, up_side1_border, up_side2_border)
    up_left_points  = add_border_points(up_left_points,  up_side1_border, up_side2_border)
    dn_right_points = add_border_points(dn_right_points, dn_side1_border, dn_side2_border)
    dn_left_points  = add_border_points(dn_left_points,  dn_side1_border, dn_side2_border)
    #print("up_right_points_shape {}\n".format(up_right_points.shape))


    # 4. Interpolate points
    up_right_popt = interpolate_points(up_right_points)
    up_left_popt  = interpolate_points(up_left_points)
    dn_right_popt = interpolate_points(dn_right_points)
    dn_left_popt  = interpolate_points(dn_left_points)
    
    #plot_interpolation_side(up_side1_border, up_side2_border, up_right_popt, "1")
    #plot_interpolation_side(up_side1_border, up_side2_border, up_left_popt, "2")
    #plot_interpolation_side(dn_side1_border, dn_side2_border, dn_right_popt, "3")
    #plot_interpolation_side(dn_side1_border, dn_side2_border, dn_left_popt, "4")

    # 5. Final projection # Take points on each side
    up_right_pts = points_from_curve(up_side1_border, up_side2_border, nb_points, up_right_popt)
    dn_right_pts = points_from_curve(dn_side1_border, dn_side2_border, nb_points, dn_right_popt)
    up_left_pts  = points_from_curve(up_side1_border, up_side2_border, nb_points, up_left_popt) 
    dn_left_pts  = points_from_curve(dn_side1_border, dn_side2_border, nb_points, dn_left_popt)
    
    # Projection de la ligne reliant 2 points sur le plan
    proj_right_df, proj_left_df = project_points_on_plane(up_right_pts, dn_right_pts, up_left_pts, dn_left_pts, plan1)
    
    # 6. Interpolation surfacce
    popt_right = interpolate_points(proj_right_df)
    popt_left  = interpolate_points(proj_left_df)
    

    return popt_right, popt_left

