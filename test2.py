
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from plot_prop import *
from plot_projections import *
from prop_info import *
from get_segments import blade_alone, get_segments_points, get_planes
from new_projections import *


''' Load data: choose a propeller. 
	Should have already changes it with stl_to_csv.py
'''
#propeller = pd.read_csv('aerostar_data.csv')
#delta = 0.6   #aerostar

propeller = pd.read_csv('propeller_data.csv')

''' Choose number of aerofoil wanted
'''
nb_seg = 5
# --> nbseg+1 plan 
# --> nbseg-1 projections
#plot_pointcloud(propeller)



#####################################################################################################
##########################            PRE-PROCESSING            #####################################
#####################################################################################################
print("Begin pre-processing")
propeller_coords = propeller.drop_duplicates(subset=None, keep='first', inplace=False)  #remove multiple same points 
propeller_coords = propeller_coords.reset_index(drop=True)

propeller = center_prop(propeller)  # center prop: middle in (0,0,0) coordinates
propeller = align_prop_length(propeller)   # longest axis aligned along z-axis
propeller = center_prop(propeller)  # re-center prop: slight shift in previous function
#plot_pointcloud(propeller)
#print("Aligned")

vect_length                  = vect_blade(propeller_coords)
vect_out, vect_side, _, _, _ = get_major_axis(propeller_coords, vect_length)     #main directions   #former hub_inner_radius (put in function later)
propeller_coords             = align_prop_side(propeller_coords) 

dmiddle, dhighest, dlowest   = d_blade(vect_length, propeller_coords)                     #d of plan ax+by+cx+d = 0
upper_blade, lower_blade     = blade_alone(propeller_coords, vect_length, dmiddle)        #points of each blades
print("End pre-processing")




#####################################################################################################
############################              PROJECTIONS            ####################################
#####################################################################################################
print("Begin projections")

planes = get_planes(upper_blade, dmiddle, dhighest, vect_length, nb_seg)   #get equations of planes for projection
print("Planes computed")
#print(len(planes))

all_plane_points = get_points(upper_blade, planes)                  #get points used for each projection
print("Points selected")
#print(len(all_plane_points))
#plot_projection_up_down(all_plane_points[0], all_plane_points[1])
#plot_projection_up_down(all_plane_points[2], all_plane_points[3])


right_param, left_param, right_pts, left_pts = get_all_projections(planes, all_plane_points) #get param, points of projection
#print(type(right_pts))
#print(right_pts)

for i in range(5):
	plot_interpolation_both_sides(right_param[i], right_pts[i], left_param[i], left_pts[i], "propeller_no_weight_" + str(i))


print("End projections")




#####################################################################################################
#############################            PARAMETERS            ######################################
#####################################################################################################





