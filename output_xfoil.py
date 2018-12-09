import numpy as np
import pandas as pd
import math
from prop_info import extreme_points
from myMathFunction import func_4_scalar
import matplotlib.pyplot as plt
from new_projections import generate_points

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


'''
def generate_points_xfoil(x, right_popt, right_points, left_popt, left_points):  #generate for X-foil
    _, highest, lowest = extreme_points(right_points)
    #x = np.linspace(lowest[0], highest[0], 100)
    scale = highest[0] - lowest[0]

    #print(right_popt)
    #print(left_popt)

    x = [a * scale + lowest[0] for a in x ] 
    x = np.array( [x] )

    if(type(right_popt) == int or type(left_popt) == int):
        #print("Plane does not have enough points for interpolation")
        return -1, -1, -1

    y_right = func_4_scalar(x, *right_popt)
    y_left  = func_4_scalar(x, *left_popt)

    
    y_first = (y_right[0, 0] + y_left[0, 0])/2            #for continuity
    y_end   = (y_right[0,-1] + y_left[0,-1])/2

    y_right[0, 0] = y_first
    y_left[0, 0]  = y_first

    y_right[0,-1] = y_end
    y_left[0,-1]  = y_end

    #print(y_right - y_left)

    #x       = (x - lowest[0])/scale 
    y_right = y_right/scale
    y_left  = y_left/scale

    #print(y_right - y_left)

    return y_right, y_left
'''


def get_generated_points_xfoil(right_param, left_param, right_pts, left_pts):
    x_list = []
    y_right_list = []
    y_left_list = []
    removed = []

    for i in range(len(right_param)):
        x, y_right, y_left = generate_points(right_param[i], right_pts[i], left_param[i], left_pts[i])

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
            
    return x_list, y_right_list, y_left_list, len(removed)


def plot_xfoil(x, y_right, y_left, position):      

    fig = plt.figure()
    fig.add_subplot(111)

    plt.scatter(x, y_right, s=170, color='r', marker='.', label="Upper edge")
    plt.scatter(x, y_left,  s=170, color='c', marker='.', label="Lower edge") 

    plt.xlabel('X (mm)', fontsize=15)
    plt.ylabel('Y (mm)', fontsize=15)

    plt.title("X-foil input points at " + str(position) + "% from hub", fontsize = 30)
    plt.axis([-20, 20, -8, 8])
    plt.legend(loc=2, prop={'size':20})
    plt.show()
    #fig.savefig('Image/' + title + '.png')



def xfoil_input_data(x_r, y_right, x_l, y_left, position):
    #fichier avec x et y dans l'ordre puis x et y_left reversed
    length = len(x_r)
    scale = max(x_r) - min(x_r)

    right = np.zeros([length, 2])    
    right[:, 0] = x_r - min(x_r)
    right[:, 1] = y_right
    right = right/scale
    #right[0,1] = 0
    #right[length-1, 1] = 0

    left  = np.zeros([length, 2])
    left[:, 0] = x_l[::-1] - min(x_l)
    left[:, 1] = y_left[::-1]
    left = left/scale
    #left[0, 1] = 0
    #left[length-1,1] = 0

    xy = np.vstack((right, left))
    print(xy)
    filename = "XFOIL6.99/xfoil" + str(position) + ".txt"

    np.savetxt(filename, xy)


'''
def xfoil_get_blade_twist(x, y_right_list, y_left_list):
	blade_twist = []

	for y_right, y_left in zip(y_right_list, y_left_list):
		lowest_point = np.zeros([2, 1])
		lowest_point[0] = x[0]
		lowest_point[1] = (y_right[0, 0] + y_left[0, 0])/2

		highest_point = np.zeros([2, 1])
		highest_point[0] = x[-1]
		highest_point[1] = (y_right[0,-1] + y_left[0,-1])/2

		direction = np.zeros([2, 1])
		direction[0] = highest_point[0] - lowest_point[0]  #x[-1] - x[0]
		direction[1] = highest_point[1] - lowest_point[1]  #y_right[-1] - y_right[0]

		angle =  math.acos( direction[0] / math.sqrt(direction[0]**2 + direction[1]**2) ) * 180 / math.pi
		blade_twist.append(angle)

	return blade_twist
'''

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


def plot_xfoil_aligned(x_r_rotated, y_r_rotated, x_l_rotated, y_l_rotated, position):      

    fig = plt.figure()
    fig.add_subplot(111)

    plt.scatter(x_r_rotated, y_r_rotated, s=170, color='r', marker='.', label="Upper edge")
    plt.scatter(x_l_rotated, y_l_rotated,  s=170, color='c', marker='.', label="Lower edge") 

    plt.xlabel('X (mm)', fontsize=15)
    plt.ylabel('Y (mm)', fontsize=15)

    plt.title("X-foil input points at " + str(position) + "% from hub", fontsize = 30)
    plt.axis([-20, 20, -8, 8])
    plt.legend(loc=2, prop={'size':20})
    plt.show()
    fig.savefig('Image/' + str(position) + '_raw.png')


def plot_xfoil_scaled(x_r_rotated, y_r_rotated, x_l_rotated, y_l_rotated, position):      

    fig = plt.figure()
    fig.add_subplot(111)

    scale = max(x_r_rotated) - min(x_r_rotated)

    x_r_rotated = (x_r_rotated - min(x_r_rotated))/scale
    x_l_rotated = (x_l_rotated - min(x_l_rotated))/scale

    y_r_rotated = y_r_rotated/scale
    y_l_rotated = y_l_rotated/scale

    plt.scatter(x_r_rotated, y_r_rotated, s=100, color='r', marker='.', label="Upper edge")
    plt.scatter(x_l_rotated, y_l_rotated, s=100, color='c', marker='.', label="Lower edge") 

    plt.xlabel('X (mm)', fontsize=15)
    plt.ylabel('Y (mm)', fontsize=15)

    plt.title("X-foil input points at " + str(position) + "% from hub", fontsize = 30)
    plt.axis([-0.15, 1.15, -0.25, 0.25])
    plt.legend(loc=2, prop={'size':20})
    plt.show()
    fig.savefig('Image/' + str(position) + '_scaled.png')