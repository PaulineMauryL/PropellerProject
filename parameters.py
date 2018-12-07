import pandas as pd
import numpy as np
import math
from myMathFunction import distance_p2p, normalize_vec, func_4_scalar
from prop_info import extreme_points, get_principal_direction
from plot_param import *



######################################################################################
#################################    CHORD LENGTH   ##################################
######################################################################################
def get_chord_length(x_list, y_right_list, y_left_list):
    chord_length = []

    for x, y_right, y_left in zip(x_list, y_right_list, y_left_list):
	    lowest_point = np.zeros([2, 1])
	    lowest_point[0] = x[0]
	    lowest_point[1] = (y_right[0] + y_left[0])/2

	    highest_point = np.zeros([2, 1])
	    highest_point[0] = x[-1]
	    highest_point[1] = (y_right[-1] + y_left[-1])/2
	    
	    chord_length.append( distance_p2p(highest_point, lowest_point) ) 

    return chord_length


######################################################################################
################################      BLADE TWIST   ##################################
######################################################################################

def get_blade_twist(x_list, y_right_list, y_left_list):
	blade_twist = []

	for x, y_right, y_left in zip(x_list, y_right_list, y_left_list):
		lowest_point = np.zeros([2, 1])
		lowest_point[0] = x[0]
		lowest_point[1] = (y_right[0] + y_left[0])/2

		highest_point = np.zeros([2, 1])
		highest_point[0] = x[-1]
		highest_point[1] = (y_right[-1] + y_left[-1])/2

		direction = np.zeros([2, 1])
		direction[0] = highest_point[0] - lowest_point[0]  #x[-1] - x[0]
		direction[1] = highest_point[1] - lowest_point[1]  #y_right[-1] - y_right[0]

		angle =  math.acos( direction[0] / math.sqrt(direction[0]**2 + direction[1]**2) ) * 180 / math.pi
		blade_twist.append(angle)

	return blade_twist


######################################################################################
#################################     TIP RADIUS    ##################################
######################################################################################

def get_tip_radius(propeller_coords):  # say in report that mean with lowest
    
    middle_point, highest_point, lowest_point = extreme_points(propeller_coords)
    tip_radius = ( np.linalg.norm(highest_point - middle_point) + np.linalg.norm(lowest_point - middle_point) )/2
    
    return tip_radius


######################################################################################
#################################     HUB RADIUS    ##################################
######################################################################################

def get_hub_points(propeller_coords, dmiddle, vect_length):
    size = 4
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



def get_hub_inner_radius(propeller_coords, vect_length):
	middle_point, _, _= extreme_points(propeller_coords)

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


def param_hub_radius(propeller_coords):
	middle_point, _, _ = extreme_points(propeller_coords)
	vect_length, _, vect_side = get_principal_direction(propeller_coords)   #main directions
	dmiddle     = - middle_point @ vect_length
	hub_points  = get_hub_points(propeller_coords, dmiddle, vect_length)
	hub_inner_radius = get_hub_inner_radius(propeller_coords, vect_length)
	outer_point, inner_point = get_hub_radius(hub_points, middle_point, hub_inner_radius, vect_side)
	hub_radius_width = distance_p2p(outer_point, inner_point)
	hub_radius = distance_p2p(middle_point, outer_point)
	return hub_radius