import pandas as pd
import numpy as np
import math
from myMathFunction import distance_p2p, normalize_vec, func_4_scalar
from prop_info import extreme_points, get_major_axis
from plot_param import *



######################## For blade twist and chord length ############################
def get_interpolated_points(right, popt):
    _, _, _, highest_point, lowest_point = extreme_points(right)
    
    highest_point[1] = func_4_scalar(highest_point[0], *popt)   #compute y value with interpolated function
    highest_point[2] = 0                                 #do not take z into account
    
    lowest_point[1] = func_4_scalar(lowest_point[0], *popt)   #compute y value with interpolated function
    lowest_point[2] = 0                                 #do not take z into account  

    return highest_point, lowest_point

def get_chord_length(x, y_right, y_left):
    chord_length = []

    lowest_point = np.zeros([2, 1])
    lowest_point[0] = x[0]
    lowest_point[1] = np.mean(y_right[0], y_left[0])

    highest_point = np.zeros([2, 1])
    highest_point[0] = x[-1]
    highest_point[1] = np.mean(y_right[-1], y_left[-1])
    
    length = distance_p2p(highest_point, lowest_point)
        

    chord_length.append( length ) 

    return chord_length

######################################################################################
#################################    CHORD LENGTH   ##################################
######################################################################################
def get_chord_length(right_param, left_param, right_pts, left_pts):
    chord_length = []

    for right, popt_right, left, popt_left in zip(right_pts, right_param, left_pts, left_param):
        
        if(type(popt_right) == int or type(popt_left) == int):
            #chord_length.append('NaN')
            pass

        else:
            highest_point_r, lowest_point_r = get_interpolated_points(right, popt_right)
            distance_r = distance_p2p(highest_point_r, lowest_point_r)
            
            highest_point_l, lowest_point_l = get_interpolated_points(left, popt_left)
            distance_l = distance_p2p(highest_point_l, lowest_point_l)

            chord_length.append( max(distance_r, distance_l) ) 

    return chord_length


######################################################################################
################################      BLADE TWIST   ##################################
######################################################################################
def get_blade_twist(right_param, left_param, right_pts, left_pts):
    blade_twist = []

    for right, popt_right, left, popt_left in zip(right_pts, right_param, left_pts, left_param):
        if(type(popt_right) == int or type(popt_left) == int):
            #blade_twist.append('NaN')
            pass

        else:
            highest_point_r, lowest_point_r = get_interpolated_points(right, popt_right)
            direction_r = highest_point_r - lowest_point_r

            highest_point_l, lowest_point_l = get_interpolated_points(left, popt_left)
            direction_l = highest_point_l - lowest_point_l

            direction = direction_l
            direction[0] = (direction_r[0] + direction_l[0]) / 2
            direction[1] = (direction_r[1] + direction_l[1]) / 2

            angle =  math.acos( direction[0] / math.sqrt(direction[0]**2 + direction[1]**2) ) * 180 / math.pi
            #print(angle)
            blade_twist.append(angle)

    return blade_twist


######################################################################################
#################################     TIP RADIUS    ##################################
######################################################################################

def get_tip_radius(propeller_coords):  # say in report that mean with lowest
    
    _, _, middle_point, highest_point, lowest_point = extreme_points(propeller_coords)
    tip_radius = ( np.linalg.norm(highest_point - middle_point) + np.linalg.norm(lowest_point - middle_point) )/2
    
    return tip_radius


######################################################################################
#################################     HUB RADIUS    ##################################
######################################################################################

def get_hub_points(propeller_coords, dmiddle, vect_length):
    size = 0.5
    plane = np.append(vect_length, dmiddle)
    upper_plane = plane[:] + [0,0,0,size]
    lower_plane = plane[:] - [0,0,0,size]
    
    index_segment = []
    for index, point in propeller_coords.iterrows():
        point_mult = np.append(point, 1)

        if(point_mult @ lower_plane < 0 and point_mult @ upper_plane >= 0):
            index_segment.append(index)
            #print("here")
    hub_points = propeller_coords.loc[index_segment].copy()
    hub = hub_points.reset_index(drop=True)
    
    return hub

'''
def find_hub_radius(middle_point, hub_inner_radius, vect_side, hub_points):
	threshold = 0.042
	alpha = threshold/2
	m = 0
	point_outer_radius = middle_point + [(hub_inner_radius + 1) * i for i in vect_side]
	c = 0

	while(m < threshold):
	    point_outer_radius = point_outer_radius + [alpha*i for i in vect_side]
	    c += 1
	    #print(c)
	    d = []
	    for i, p in hub_points.iterrows():
	        d.append( distance_p2p(point_outer_radius, p) )
	    m = min(d)

	point_inner_radius = middle_point + [hub_inner_radius * i for i in vect_side]

	return point_outer_radius, point_inner_radius
'''


def get_hub_inner_radius(propeller_coords, vect_length):
	a, b, middle_point, c, d= extreme_points(propeller_coords)

	dist = (propeller_coords.add(-middle_point)).copy()

	distance = np.zeros( (len(dist), 1) ) 

	for i, elem in dist.iterrows():
	    distance[i] = math.sqrt(elem['X']**2 + elem['Y']**2 + elem['Z']**2)

	values, index = np.unique(distance, return_index=True)

	a_point = np.asarray(propeller_coords.loc[index[0]])
	b_point = np.asarray(propeller_coords.loc[index[1]])
	c_point = np.asarray(propeller_coords.loc[index[2]])

	hub_inner_radius = (middle_point - a_point) + (middle_point - b_point) + (middle_point - c_point)
	hub_inner_radius = [i/3 for i in hub_inner_radius]
	hub_inner_radius = np.linalg.norm(hub_inner_radius)

	return hub_inner_radius


######################################################################################
#############################     HUB OUTER RADIUS    ################################
######################################################################################
def get_hub_radius(hub, middle_point, hub_inner_radius, vect_side):

    dmiddle  = - middle_point @ vect_side
    plane = np.append(vect_side, dmiddle)
    
    equation = []
    for index, point in hub.iterrows():  #calcule quel point a la plus grande valeur quand multiplie un point de hub avec plan perpendiculaire
        point_mult = np.append(point, 1)
        equation.append(point_mult @ plane)
        
    outer_point_idx = np.argmax(equation)
    #print(outer_point_idx)
    outer_point = hub.iloc[outer_point_idx]

    inner_point = middle_point + [hub_inner_radius * i for i in vect_side]  #mets le points du milieu dans la meme direction que le point max
    
    return outer_point, inner_point


def param_hub_radius(propeller_coords, vect_length):
    
    _, _, middle_point, _, _ = extreme_points(propeller_coords)

    dmiddle     = - middle_point @ vect_length
    hub_points  = get_hub_points(propeller_coords, dmiddle, vect_length)

    hub_inner_radius = get_hub_inner_radius(propeller_coords, vect_length)
    _, vect_side = get_major_axis(propeller_coords, vect_length)   #main directions   
    outer_point, inner_point = get_hub_radius(hub_points, middle_point, hub_inner_radius, vect_side)
    
    #hub_radius = hub_outer_radius[2] - middle_point[2]  #from center to exterior radius
    hub_radius_width = distance_p2p(outer_point, inner_point)
    hub_radius = distance_p2p(middle_point, outer_point)
    #plot_hub(propeller_coords, hub_points, outer_point_radius, inner_point_radius)
    
    return hub_radius