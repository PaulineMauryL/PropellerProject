import numpy as np
from prop_info import extreme_points
from myMathFunction import func_4_scalar


def get_planes_xfoil(blade, d_middle, d_lowest, vect_length, positions):
	
	planes = []

	length = d_lowest - d_middle

	initial_plane = np.append(vect_length, d_middle)
	planes.append(initial_plane)

	for i in positions:
		delta = i/100*length
		new_plane = initial_plane[:] - [0,0,0,delta]
		planes.append(new_plane)

	planes.append( np.append(vect_length, -d_lowest) )
	return planes



def generate_points_xfoil(right_popt, right_points, left_popt, left_points):  #generate for X-foil
    _, highest, lowest = extreme_points(right_points)
    #x = np.linspace(lowest[0], highest[0], 100)
    scale = highest[0] - lowest[0]
    x = [1, 0.95, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.0750, 0.05, 0.025, 0.0125, 0]
    x = [a * scale + lowest[0] for a in x ] 
    x = np.array( [x] )

    if(type(right_popt) == int or type(left_popt) == int):
        #print("Plane does not have enough points for interpolation")
        return -1, -1, -1

    y_right = func_4_scalar(x, *right_popt)
    y_left  = func_4_scalar(x, *left_popt)

    y_first = (y_right[0] + y_left[0])/2                   #for continuity
    y_end   = (y_right[-1] + y_left[-1])/2

    y_right[0] = y_first
    y_left[0]  = y_first

    y_right[-1] = y_end
    y_left[-1]  = y_end

    x       = x/scale - lowest[0]
    y_right = y_right/scale
    y_left  = y_left/scale

    return x, y_right, y_left



def get_generated_points_xfoil(right_param, left_param, right_pts, left_pts):
    x_list = []
    y_right_list = []
    y_left_list = []
    removed = []

    for i in range(len(right_param)):
        x, y_right, y_left = generate_points_xfoil(right_param[i], right_pts[i], left_param[i], left_pts[i])

        if(type(x) == int):
            print("Plane {} has been removed".format(i))
            removed.append(i)
        else:
            x_list.append(x)
            y_right_list.append(y_right)
            y_left_list.append(y_left)    
            
    right = [] 
    left = []
    for i in range(len(right_param)):
        if i not in removed:
            right.append(right_pts[i])
            left.append(left_pts[i])
        else:
        	print("Warning a plane has been removed (did not have enough point during interpolation)")
            
    return x_list, y_right_list, y_left_list, right, left, len(removed)