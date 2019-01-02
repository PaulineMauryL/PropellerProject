import numpy as np
import pandas as pd
import math

def align_aerofoil(x_list, y_right_list, y_left_list, blade_twist):
	 #Align aerofoil such that blade twîst = 0
		#INPUT: dataframe of points aligned in z, vect on side of prop
		#OUTPUT: dataframe of aligned points aligned everywhere
	x_r_rotated = []
	y_r_rotated = []
	x_l_rotated = []
	y_l_rotated = []

	i = 0
	blade_twist = [bt * math.pi / 180 for bt in blade_twist]
	ct = np.cos(blade_twist)
	st = np.sin(blade_twist)

	for x, y_r, y_l in zip(x_list, y_right_list, y_left_list):

		x_r_rotated.append(  x*ct[i] + y_r*st[i])
		y_r_rotated.append( -x*st[i] + y_r*ct[i])

		x_l_rotated.append(  x*ct[i] + y_l*st[i])
		y_l_rotated.append( -x*st[i] + y_l*ct[i])

		i = i+1

	return x_r_rotated, y_r_rotated, x_l_rotated, y_l_rotated


def mirror_aerofoil(y_r_rotated, y_l_rotated):
    y_r_flipped = [-x for x in y_r_rotated]
    y_l_flipped = [-x for x in y_l_rotated]
    
    return y_r_flipped, y_l_flipped


# This contains only the X,Y coordinates, which run from the trailing edge, round the leading edge, 
# back to the trailing edge in either direction
def xfoil_input_data(x_r_rotated, y_r_flipped, x_l_rotated, y_l_flipped, position):
    #fichier avec x et y dans l'ordre puis x et y_left reversed
    length = len(x_r_rotated)
    scale = max(max(x_r_rotated) - min(x_r_rotated), max(x_l_rotated) - min(x_l_rotated))
    #print(x_r[::-1])
    right = np.zeros([length, 2])    
    right[:, 0] = ((x_l_rotated - min(x_l_rotated))/scale)[::-1]
    right[:, 1] = (y_l_flipped/scale)[::-1]    
    #print(right)
    #print("\n")

    left  = np.zeros([length, 2])
    left[:, 0] = (x_r_rotated - min(x_r_rotated))/scale
    left[:, 1] = y_r_flipped/scale
    #print(left)
    #print("\n")    
    xy = np.vstack((right, left))
    #print(xy)
    filename = "output/aerofoil_" + str(position) + "_.txt"

    np.savetxt(filename, xy)


def xfoil_inputs(x_r_rotated, y_r_flipped, x_l_rotated, y_l_flipped, positions):
	for i in range(len(x_r_rotated)):
		xfoil_input_data(x_r_rotated[i], y_r_flipped[i], x_l_rotated[i], y_l_flipped[i], positions[i])