import numpy as np 
import pandas as pd


def blade_alone(propeller_coords, vect_upper, middle_point, dmiddle):
    upper = []
    lower = []
    for index, point in propeller_coords.iterrows():
        if(point @ vect_upper + dmiddle > 0):
            upper.append(index)
        else:
            lower.append(index)
    upper_blade = propeller_coords.iloc[upper].copy()
    lower_blade = propeller_coords.iloc[lower].copy()
    
    return upper_blade, lower_blade


def get_planes(blade, dmiddle, d_max, vect, nb_seg):
	delta_d = (d_max - dmiddle)/nb_seg
	last_plane = np.append(vect, dmiddle)
	planes = [last_plane]

	for i in range(nb_seg):
		new_plane = last_plane[:] + [0,0,0,delta_d]
		planes.append(new_plane)
		last_plane = new_plane

	return planes



def get_segments(blade, planes, nb_seg):
	segments = {}
	segments["points"] = []

	for i in range(nb_seg):
		index_segment = []

		for index, point in blade.iterrows():
			point_mult = np.append(point, 1)

			if(point_mult @ planes[i] > 0 and point_mult @ planes[i+1] <= 0):
				index_segment.append(index)
        
		segments["points"].append(blade.loc[index_segment].copy().as_matrix())

	for index, point in blade.iterrows():
		point_mult = np.append(point, 1)

		if(point_mult @ planes[nb_seg] > 0):
			index_segment.append(index) 
			
	segments["points"].append(blade.loc[index_segment].copy().as_matrix())
	
	return segments
