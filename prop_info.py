import numpy as np

def extreme_points(propeller_coords):
    maxz = np.max(propeller_coords["Z"])
    points_maxz = propeller_coords.loc[propeller_coords["Z"] == maxz]
    maxzx = np.mean(points_maxz["X"])
    maxzy = np.mean(points_maxz["Y"])
    max_point = np.asarray([maxzx, maxzy, maxz])
    
    minz = np.min(propeller_coords["Z"])
    points_minz = propeller_coords.loc[propeller_coords["Z"] == minz]
    minzx = np.mean(points_minz["X"])
    minzy = np.mean(points_minz["Y"])
    min_point = np.asarray([minzx, minzy, minz])
    
    midx = np.mean(propeller_coords["X"])
    midy = np.mean(propeller_coords["Y"])
    midz = np.mean(propeller_coords["Z"])
    middle_point = np.asarray([midx, midy, midz])
    
    return max_point, min_point, middle_point

def blade_info(max_point, min_point, middle_point):
    vect_upper = max_point - middle_point
    vect_lower = middle_point - min_point
    dmiddle = - middle_point @ vect_upper
    dmax = - max_point @ vect_upper
    dmin = - min_point @ vect_lower
    return vect_upper, vect_lower, dmiddle, dmax, dmin