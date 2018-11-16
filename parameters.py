import pandas as pd
import numpy as np
import math
from myMathFunction import distance_p2p, normalize_vec
from prop_info import extreme_points
from plot_param import *


######################################################################################
#################################    CHORD LENGTH   ##################################
######################################################################################
def get_chord_length(all_planes_points):
    chord_length = []
    for one_plane_point in all_planes_points:
        _, _, _, highest_point, lowest_point = extreme_points(one_plane_point)
        distance = distance_p2p(highest_point, lowest_point)
        chord_length.append(distance)
    return chord_length


######################################################################################
################################      BLADE TWIST   ##################################
######################################################################################
def get_blade_twist(all_planes_points):
    blade_twist = []
    for one_plane_point in all_planes_points:
        _, _, _, highest_point, lowest_point = extreme_points(one_plane_point)
        direction = highest_point[:2] - lowest_point[:2]
        #print(direction)
        angle =  math.acos( direction[0]/ math.sqrt(direction[0]**2 + direction[1]**2) ) * 180 / math.pi
        #print(angle)
        blade_twist.append(angle)
    return blade_twist


######################################################################################
#################################     TIP RADIUS    ##################################
######################################################################################

def get_tip_radius(propeller_coords):
    
    _, _, middle_point, highest_point, _ = extreme_points(propeller_coords)
    tip_radius = np.linalg.norm(highest_point - middle_point)
    
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

def get_major_axis(propeller_coords, vect_blade):
    # Search for closest point around middle, make cross products, find max
	_, _, middle_point, _, _ = extreme_points(propeller_coords)
	dist = (propeller_coords.add(-middle_point)).copy()

	distance = np.zeros( (len(dist),1) ) 
	for i, elem in dist.iterrows():
	    #print(math.sqrt(elem['X']**2 + elem['Y']**2 + elem['Z']**2))
	    distance[i] = math.sqrt(elem['X']**2 + elem['Y']**2 + elem['Z']**2)
	#print(distance)
	#distance.shape

	#Find closest points to center
	values, index = np.unique(distance, return_index=True)
	#index
	#index.shape

	a_point = np.asarray(propeller_coords.loc[index[0]])
	b_point = np.asarray(propeller_coords.loc[index[1]])
	c_point = np.asarray(propeller_coords.loc[index[2]])

	#Get vector in plane         #check they are not colinear
	ab_vec = b_point - a_point
	ac_vec = c_point - a_point

	# Get normal plane to propeller (goes through hub)
	vect_out = np.cross(ab_vec, ac_vec)
	#print(vect_out)
	vect_out = normalize_vec(vect_out)
	#print(vect_out)

	# Get last direction
	vect_side = np.cross(vect_out, vect_blade)
	#print(vect_side)
	vect_side = normalize_vec(vect_side)
	#print(vect_side)

	hub_inner_radius = (middle_point - a_point) + (middle_point - b_point) + (middle_point - c_point)
	hub_inner_radius = [i/3 for i in hub_inner_radius]
	hub_inner_radius = np.linalg.norm(hub_inner_radius)

	return vect_out, vect_side, hub_inner_radius



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


def param_hub_radius(propeller_coords, dmiddle, vect_length):
    
    _, _, middle_point, _, _ = extreme_points(propeller_coords)
    vect_out, vect_side, hub_inner_radius = get_major_axis(propeller_coords, vect_length)   #main directions

    hub_points = get_hub_points(propeller_coords, dmiddle, vect_length)
    
    outer_point, inner_point = get_hub_radius(hub_points, middle_point, hub_inner_radius, vect_side)
    
    #hub_radius = hub_outer_radius[2] - middle_point[2]  #from center to exterior radius
    hub_radius_width = distance_p2p(outer_point, inner_point)
    hub_radius = distance_p2p(middle_point, outer_point)
    #plot_hub(propeller_coords, hub_points, outer_point_radius, inner_point_radius)
    
    return hub_radius










