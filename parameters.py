import pandas as pd
import numpy as np
from myMathFunction import distance_p2p


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

def get_hub_radius(hub, middle_point, vect_side, hub_inner_radius):
    dmiddle  = - middle_point @ vect_side
    plane = np.append(vect_side, dmiddle)
    
    equation = []
    for index, point in hub.iterrows():
        point_mult = np.append(point, 1)
        equation.append(point_mult @ plane)
        
    outer_point_idx = np.argmax(equation)
    #print(outer_point_idx)
    outer_point_radius = hub.iloc[outer_point_idx]

    point_inner_radius = middle_point + [hub_inner_radius * i for i in vect_side]
    
    return outer_point_radius, point_inner_radius