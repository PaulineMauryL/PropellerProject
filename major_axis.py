import numpy as np
import math
from myMathFunction import normalize_vec

def get_major_axis(propeller_coords, middle_point, vect_blade):
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

	return vect_out, vect_side