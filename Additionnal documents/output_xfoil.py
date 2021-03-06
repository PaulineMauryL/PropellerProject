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
    filename = "XFOIL6.99/xf" + str(position) + "_r.txt"

    np.savetxt(filename, xy)


def xfoil_inputs(x_r_rotated, y_r_flipped, x_l_rotated, y_l_flipped, positions):
	for i in range(len(x_r_rotated)):
		xfoil_input_data(x_r_rotated[i], y_r_flipped[i], x_l_rotated[i], y_l_flipped[i], positions[i])


def plot_xfoil_scaled(x_r_rotated, y_r_rotated, x_l_rotated, y_l_rotated, position):      

    fig = plt.figure()
    fig.add_subplot(111)

    scale = max(x_r_rotated) - min(x_r_rotated)

    x_r_rotated = (x_r_rotated - min(x_r_rotated))/scale
    x_l_rotated = (x_l_rotated - min(x_l_rotated))/scale

    y_r_rotated = y_r_rotated/scale
    y_l_rotated = y_l_rotated/scale

    plt.scatter(x_r_rotated, y_r_rotated, s=100, color='b', marker='.', label="Upper surface")
    plt.scatter(x_l_rotated, y_l_rotated, s=100, color='g', marker='.', label="Lower surface") 

    plt.xlabel('X (mm)', fontsize=15)
    plt.ylabel('Y (mm)', fontsize=15)

    plt.title("X-foil input points  (" + str(position) + "% r/R)", fontsize = 30)
    plt.axis([-0.15, 1.15, -0.25, 0.25])
    plt.legend(loc=2, prop={'size':20})
    plt.show()
    fig.savefig('Image/' + str(position) + '_scaled.png')
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
def plot_xfoil(x, y_right, y_left, position):      

    fig = plt.figure()
    fig.add_subplot(111)

    plt.scatter(x, y_right, s=170, color='b', marker='.', label="Upper surface")
    plt.scatter(x, y_left,  s=170, color='g', marker='.', label="Lower surface") 

    plt.xlabel('X (mm)', fontsize=15)
    plt.ylabel('Y (mm)', fontsize=15)

    plt.title("Interpolated points (" + str(position) + "% r/R)", fontsize = 20)
    plt.axis([-20, 15, -8, 8])
    plt.legend(loc=2, prop={'size':20})
    plt.show()
    fig.savefig('Image/xfoil/' + str(position) + '_computed.png')


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


def reynold_number(radius, rpm, chord_length):
    kinematic_viscosity = 14.88 * math.pow(10,-6) #[m^2/s]  https://www.engineeringtoolbox.com/air-absolute-kinematic-viscosity-d_601.html at 18°
    kinematic_viscosity = kinematic_viscosity*60*math.pow(10,6)   # *60 -> [m^2/min]  *10^6 -> [mm^2/min]
    u = radius * rpm  #[mm] * [/min] 
    reynold = (u * chord_length)/kinematic_viscosity    # [mm/min] * [mm] / [mm^2/min] -> [X]
    return reynold

def get_reynold_numbers(radius, rpm, chord_length):
    reynold = []
    for rad, cl in zip(radius, chord_length):
        reynold.append( reynold_number(rad, rpm, cl) )
    return reynold

def mach_number(radius, rpm):  
    c =  20580000 #v_sound = 343[m/s] = 343*60[m/min] = 343*60*1000 [mm/min]
    u = radius * rpm  #[mm] * [/min] 
    mach = u/c     # [min/mmm] / [mm/min] -> [X]
    return mach

def get_mach_numbers(radius, rpm):
    mach = []
    for rad in radius:
        mach.append( mach_number(rad, rpm) )
    return mach

def output_reynold_mach(positions, radius, reynold, mach, filename):
    df = pd.DataFrame({'Percentage': positions, 'Radius': radius,  'Reynold': reynold, 'Mach':mach})
    df.to_csv(filename)
    return df
    

def plot_xfoil_aligned(x_r_rotated, y_r_rotated, x_l_rotated, y_l_rotated, position):      

    fig = plt.figure()
    fig.add_subplot(111)

    plt.scatter(x_r_rotated, y_r_rotated, s=170, color='b', marker='.', label="Upper surface")
    plt.scatter(x_l_rotated, y_l_rotated,  s=170, color='g', marker='.', label="Lower surface") 

    plt.xlabel('X (mm)', fontsize=15)
    plt.ylabel('Y (mm)', fontsize=15)

    plt.title("Aligned (" + str(position) + "% r/R)", fontsize = 20)
    plt.axis([-20, 15, -8, 8])
    plt.legend(loc=2, prop={'size':20})
    plt.show()
    fig.savefig('Image/xfoil/' + str(position) + '_align.png')

def plot_xfoil_mirror(x_r_rotated, y_r_rotated, x_l_rotated, y_l_rotated, position):      

    fig = plt.figure()
    fig.add_subplot(111)

    plt.scatter(x_r_rotated, y_r_rotated, s=170, color='b', marker='.', label="Upper surface")
    plt.scatter(x_l_rotated, y_l_rotated,  s=170, color='g', marker='.', label="Lower surface") 

    plt.xlabel('X (mm)', fontsize=15)
    plt.ylabel('Y (mm)', fontsize=15)

    plt.title("Mirrored (" + str(position) + "% r/R)", fontsize = 20)
    plt.axis([-20, 15, -8, 8])
    plt.legend(loc=2, prop={'size':20})
    plt.show()
    fig.savefig('Image/xfoil/' + str(position) + '_input1.png')



def plot_xfoil_pptx(x_r_rotated, y_r_rotated, x_l_rotated, y_l_rotated, position):      

    fig = plt.figure()
    fig.add_subplot(111)

    plt.scatter(x_r_rotated, y_r_rotated, s=170, color='b', marker='.', label="Upper surface")
    plt.scatter(x_l_rotated, y_l_rotated,  s=170, color='g', marker='.', label="Lower surface") 

    plt.xlabel('X (mm)', fontsize=15)
    plt.ylabel('Y (mm)', fontsize=15)

    plt.title("Output (" + str(position) + "% r/R)", fontsize = 20)
    plt.axis([-20, 15, -8, 8])
    plt.legend(loc=2, prop={'size':20})
    plt.show()
    fig.savefig('Image/xfoil/' + str(position) + '_input2.png')