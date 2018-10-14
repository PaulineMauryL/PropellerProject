import numpy as np
from myMathFunction import normalize_vec

def extreme_points(propeller_coords):
    maxz = np.max(propeller_coords["Z"])
    points_maxz = propeller_coords.loc[propeller_coords["Z"] == maxz]
    maxzx = np.mean(points_maxz["X"])
    maxzy = np.mean(points_maxz["Y"])
    max_point = np.asarray([maxzx, maxzy, maxz])
    
    maxzmaxx = np.max(points_maxz["X"])
    maxzmaxy = np.max(points_maxz["Y"])
    highest_point = np.asarray([maxzmaxx, maxzmaxy, maxz])

    minz = np.min(propeller_coords["Z"])
    points_minz = propeller_coords.loc[propeller_coords["Z"] == minz]
    minzx = np.mean(points_minz["X"])
    minzy = np.mean(points_minz["Y"])
    min_point = np.asarray([minzx, minzy, minz])
    
    minzminx = np.min(points_maxz["X"])
    minzminy = np.min(points_maxz["Y"])
    lowest_point = np.asarray([minzminx, minzminy, minz])

    midx = np.mean(propeller_coords["X"])
    midy = np.mean(propeller_coords["Y"])
    midz = np.mean(propeller_coords["Z"])
    middle_point = np.asarray([midx, midy, midz])


    return max_point, min_point, middle_point, highest_point, lowest_point


def vect_blade(max_point, min_point):
    vect_length = normalize_vec(max_point - min_point)
    #print(vect_blade)
    #vect_upper = normalize_vec(max_point - middle_point)
    #vect_lower = normalize_vec(middle_point - min_point)

    return vect_length


def d_blade(vect_length, middle_point, highest_point, lowest_point):
	dmiddle  = - middle_point @ vect_length
	#dmax     = - max_point @ vect_blade
	#dmin     = - min_point @ vect_blade
	dhighest = - highest_point @ vect_length
	dlowest  = - highest_point @ vect_length

	return dmiddle, dhighest, dlowest