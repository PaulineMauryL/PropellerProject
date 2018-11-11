import numpy as np
import pandas as pd
from myMathFunction import normalize_vec



def center_prop(propeller_coords):
	midx = np.mean(propeller_coords["X"])
	midy = np.mean(propeller_coords["Y"])
	midz = np.mean(propeller_coords["Z"])
	middle_point = np.asarray([midx, midy, midz])

	propeller_coords = propeller_coords - middle_point

	return propeller_coords


def align_prop(propeller_coords):
	''' Align the propeller: the longest length aligned on the z axis
		INPUT: dataframe of points
		OUTPUT: dataframe of aligned points
	'''
	_, _, _, highest_point, _ = extreme_points(propeller_coords)
	print(type(highest_point))
	rotation_point = highest_point.copy()
	rotation_point[2] = 0

	theta =  np.arccos( (rotation_point @ [0,1,0]) / (np.linalg.norm(rotation_point) * np.linalg.norm([0,1,0]))) #* 180/np.pi
	ct, st = np.cos(theta), np.sin(theta)
	rotz = np.array([[ct,-st, 0], [st, ct, 0], [0,0,1]])

	rot_proj = rotz @ highest_point
	phi =  - np.arccos( (rot_proj @ [0,0,1]) / (np.linalg.norm(rot_proj) * np.linalg.norm([0,0,1]))) #* 180/np.pi
	cp, sp = np.cos(phi), np.sin(phi)
	rotx = np.array([[1, 0, 0], [0, cp, -sp], [0,sp,cp]])

	print(type(propeller_coords))
	propeller_coords = propeller_coords.apply(rotate, rx = rotx, rz = rotz, axis = 1, result_type = 'broadcast')
	print(type(propeller_coords))
	return propeller_coords


def rotate(row, rx, rz):
	return rx @ rz @ np.array([row['X'], row['Y'], row['Z']])


def extreme_points(propeller_coords):

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
	    maxxz = np.mean(points_maxx["Z"])
	    maxxy = np.mean(points_maxx["Y"])
	    max_point = np.asarray([maxx, maxxy, maxxz])
	    
	    maxxmaxz = np.max(points_maxx["Z"])
	    maxxmaxy = np.max(points_maxx["Y"])
	    highest_point = np.asarray([maxx, maxxmaxy, maxxmaxz])


	    points_minx = propeller_coords.loc[propeller_coords["X"] == minx]
	    minxz = np.mean(points_minx["Z"])
	    minxy = np.mean(points_minx["Y"])
	    min_point = np.asarray([minx, minxy, minxz])
	    
	    minxminz = np.min(points_minx["Z"])
	    minxminy = np.min(points_minx["Y"])
	    lowest_point = np.asarray([minx, minxminy, minxminz])


    elif(delta_y > delta_x and delta_y > delta_z):
	    points_maxy = propeller_coords.loc[propeller_coords["Y"] == maxy]
	    maxyx = np.mean(points_maxy["X"])
	    maxyz = np.mean(points_maxy["Z"])
	    max_point = np.asarray([maxyx, maxy, maxyz])
	    
	    maxymaxx = np.max(points_maxy["X"])
	    maxymaxz = np.max(points_maxy["Z"])
	    highest_point = np.asarray([maxymaxx, maxy, maxymaxz])


	    points_miny = propeller_coords.loc[propeller_coords["Y"] == miny]
	    minyx = np.mean(points_miny["X"])
	    minyz = np.mean(points_miny["Z"])
	    min_point = np.asarray([minyx, miny, minyz])
	    
	    minyminx = np.min(points_miny["X"])
	    minyminz = np.min(points_miny["Z"])
	    lowest_point = np.asarray([minyminx, miny, minyminz])



    elif(delta_z > delta_x and delta_z > delta_y):
	    points_maxz = propeller_coords.loc[propeller_coords["Z"] == maxz]
	    maxzx = np.mean(points_maxz["X"])
	    maxzy = np.mean(points_maxz["Y"])
	    max_point = np.asarray([maxzx, maxzy, maxz])
	    
	    maxzmaxx = np.max(points_maxz["X"])
	    maxzmaxy = np.max(points_maxz["Y"])
	    highest_point = np.asarray([maxzmaxx, maxzmaxy, maxz])


	    points_minz = propeller_coords.loc[propeller_coords["Z"] == minz]
	    minzx = np.mean(points_minz["X"])
	    minzy = np.mean(points_minz["Y"])
	    min_point = np.asarray([minzx, minzy, minz])
	    
	    minzminx = np.min(points_minz["X"])
	    minzminy = np.min(points_minz["Y"])
	    lowest_point = np.asarray([minzminx, minzminy, minz])


    else:
    	print("Error in extreme_point of max_info")

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
	dlowest  = - lowest_point @ vect_length

	return dmiddle, dhighest, dlowest