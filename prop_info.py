import numpy as np
import pandas as pd
import math
from myMathFunction import normalize_vec


def prepare_propeller(propeller):
    
    propeller = propeller.drop_duplicates(subset=None, keep='first', inplace=False)  #remove multiple same points 
    propeller = propeller.reset_index(drop=True)
    
    propeller = center_prop(propeller)     # center prop: middle in (0,0,0) coordinates
    propeller = align_prop_length(propeller)      # longest axis aligned along z-axis
    propeller = center_prop(propeller)     # re-center prop: slight shift in previous function

    vect_out, vect_side, vect_length = principal_direction()
    #vect_length         = vect_blade(propeller)
    #vect_out, vect_side = get_major_axis(propeller, vect_length)     #main directions   #former hub_inner_radius (put in function later)
    propeller           = align_prop_side(propeller, vect_side) 

    return propeller, vect_length, vect_out, vect_side

def principal_direction():
    vect_length = [0,0,1]
    vect_side   = [0,1,0]
    vect_out    = [1,0,0]
    return vect_out, vect_side, vect_length

def center_prop(propeller_coords):
	'''Center the propeller in (0,0,0) coordinates
	'''
	midx = np.mean(propeller_coords["X"])
	midy = np.mean(propeller_coords["Y"])
	midz = np.mean(propeller_coords["Z"])
	middle_point = np.asarray([midx, midy, midz])

	propeller_coords = propeller_coords - middle_point

	return propeller_coords


def align_prop_length(propeller_coords):
	''' Align the propeller: the longest length aligned on the z axis
		INPUT: dataframe of points
		OUTPUT: dataframe of aligned points
	'''
	_, highest_point, _ = extreme_points(propeller_coords)
	#print(type(highest_point))
	rotation_point = highest_point.copy()
	rotation_point[2] = 0

	theta =  np.arccos( (rotation_point @ [0,1,0]) / (np.linalg.norm(rotation_point) * np.linalg.norm([0,1,0]))) #* 180/np.pi
	ct, st = np.cos(theta), np.sin(theta)
	rotz = np.array([[ct,-st, 0], [st, ct, 0], [0,0,1]])

	rot_proj = rotz @ highest_point
	phi =  - np.arccos( (rot_proj @ [0,0,1]) / (np.linalg.norm(rot_proj) * np.linalg.norm([0,0,1]))) #* 180/np.pi
	cp, sp = np.cos(phi), np.sin(phi)
	rotx = np.array([[1, 0, 0], [0, cp, -sp], [0,sp,cp]])

	#print(type(propeller_coords))
	propeller_coords = propeller_coords.apply(rotate_length, rx = rotx, rz = rotz, axis = 1, result_type = 'broadcast')
	#print(type(propeller_coords))
	return propeller_coords


def align_prop_side(propeller, vect_side):
	''' Align the propeller with the side on x and the vect through the hub on y
		INPUT: dataframe of points aligned in z, vect on side of prop
		OUTPUT: dataframe of aligned points aligned everywhere
	'''	
	rotation_point = np.asarray(vect_side)
	rotation_point[2] = 0

	theta = np.arccos( (rotation_point @ [1,0,0]) / (np.linalg.norm(rotation_point) * np.linalg.norm([1,0,0])))
	ct, st = np.cos(theta), np.sin(theta)
	rotz = np.array([[ct,-st, 0], [st, ct, 0], [0,0,1]])

	propeller = propeller.apply(rotate_side, rz = rotz, axis = 1, result_type = 'broadcast')

	return propeller


def rotate_length(row, rx, rz):
	return rx @ rz @ np.array([row['X'], row['Y'], row['Z']])


def rotate_side(row, rz):
	return rz @ np.array([row['X'], row['Y'], row['Z']])


def extreme_points(propeller_coords):
	''' Find points at extremities of propeller
		INPUT: DataFrame propeller_coords: points of propeller
		OUTPUT: array of coordinates [x, y, z] for:
		max_point: points with all maximum coordinates
		min_point: points with all minimum coordinates
		middle_point: points at the middle of propeller
		highest_point: points with highest coordinates in main direction and mean in others
		lowest_point: points with lowest coordinates in main direction and mean in others
	'''
	maxx = np.max(propeller_coords["X"])
	minx = np.min(propeller_coords["X"])
	delta_x = maxx - minx

	maxy = np.max(propeller_coords["Y"])
	miny = np.min(propeller_coords["Y"])
	delta_y = maxy - miny

	maxz = np.max(propeller_coords["Z"])
	minz = np.min(propeller_coords["Z"])
	delta_z = maxz - minz

	if(delta_x > delta_y and delta_x > delta_z):
		points_maxx = propeller_coords.loc[propeller_coords["X"] == maxx]
		maxxmaxz = np.max(points_maxx["Z"])
		maxxmaxy = np.max(points_maxx["Y"])
		highest_point = np.asarray([maxx, maxxmaxy, maxxmaxz])


		points_minx = propeller_coords.loc[propeller_coords["X"] == minx]
		minxminz = np.min(points_minx["Z"])
		minxminy = np.min(points_minx["Y"])
		lowest_point = np.asarray([minx, minxminy, minxminz])


	elif(delta_y > delta_x and delta_y > delta_z):
		points_maxy = propeller_coords.loc[propeller_coords["Y"] == maxy]
		maxymaxx = np.max(points_maxy["X"])
		maxymaxz = np.max(points_maxy["Z"])
		highest_point = np.asarray([maxymaxx, maxy, maxymaxz])


		points_miny = propeller_coords.loc[propeller_coords["Y"] == miny]
		minyminx = np.min(points_miny["X"])
		minyminz = np.min(points_miny["Z"])
		lowest_point = np.asarray([minyminx, miny, minyminz])


	elif(delta_z > delta_x and delta_z > delta_y):
		points_maxz = propeller_coords.loc[propeller_coords["Z"] == maxz]
		maxzmaxx = np.max(points_maxz["X"])
		maxzmaxy = np.max(points_maxz["Y"])
		highest_point = np.asarray([maxzmaxx, maxzmaxy, maxz])

		points_minz = propeller_coords.loc[propeller_coords["Z"] == minz]
		minzminx = np.min(points_minz["X"])
		minzminy = np.min(points_minz["Y"])
		lowest_point = np.asarray([minzminx, minzminy, minz])

	else:
		print("Error in extreme_point of max_info")

	# Point in middle of blade
	midx = np.mean(propeller_coords["X"])
	midy = np.mean(propeller_coords["Y"])
	midz = np.mean(propeller_coords["Z"])
	middle_point = np.asarray([midx, midy, midz])

	return middle_point, highest_point, lowest_point


def vect_blade(propeller_coords):

    middle_point, highest_point, lowest_point = extreme_points(propeller_coords)

    vect_length = normalize_vec(highest_point - middle_point)
    #print(vect_blade)
    #vect_upper = normalize_vec(max_point - middle_point)
    #vect_lower = normalize_vec(middle_point - min_point)

    return vect_length


def d_blade(vect_length, propeller_coords):

	middle_point, highest_point, lowest_point = extreme_points(propeller_coords)

	dmiddle  = - middle_point @ vect_length
	dhighest = - highest_point @ vect_length
	dlowest  = - lowest_point @ vect_length

	#dmax     = - max_point @ vect_blade
	#dmin     = - min_point @ vect_blade


	return dmiddle, dhighest, dlowest


def aerofoil_width(propeller_coords):
	minx = np.min(propeller_coords["X"])
	maxx = np.max(propeller_coords["X"])
	
	miny = np.min(propeller_coords["Y"])
	maxy = np.max(propeller_coords["Y"])

	return math.sqrt( (maxx - minx)**2 + (maxy - miny)**2  )


def get_major_axis(propeller_coords, vect_blade):
	middle_point, _, _ = extreme_points(propeller_coords)
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