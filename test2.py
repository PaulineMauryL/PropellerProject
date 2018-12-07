import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from plot_prop import *
from plot_projections import *
from plot_param import *
from prop_info import *
from get_segments import blade_alone, get_segments_points, get_planes
from new_projections import *
from parameters import *


propeller = pd.read_csv('propeller_data.csv')

''' Choose number of aerofoil wanted
'''
nb_seg = 10




#####################################################################################################
##########################            PRE-PROCESSING            #####################################
#####################################################################################################
propeller_coords, vect_length, vect_out, vect_side = prepare_propeller(propeller)

dmiddle, dlowest, dhighest   = d_blade(vect_length, propeller_coords)                     #d of plan ax+by+cx+d = 0
upper_blade, lower_blade     = blade_alone(propeller_coords, vect_length, dmiddle)        #points of each blades


print("Begin projections")
planes, delta_d = get_planes(upper_blade, dmiddle, dlowest, vect_length, nb_seg)   #get equations of planes for projection  #get equations of planes for projection
all_plane_points = get_points(upper_blade, planes)                  #get points used for each projection

#####################################################################################################
##########################              PROJECTION              #####################################
#####################################################################################################
right_param, left_param, right_pts, left_pts = get_all_projections(planes, all_plane_points)
x_list, y_right_list, y_left_list, right_pts, left_pts, position, rm = get_generated_points(right_param, left_param, right_pts, left_pts, delta_d)

for i in range(len(all_plane_points) - rm):
    plot_interpolation_both_sides( right_pts[i], left_pts[i], x_list[i], y_right_list[i], y_left_list[i], i, "Aerofoil at " + str(round(position[i], 2)) + "mm from hub")

print("End projections")




#####################################################################################################
#############################            PARAMETERS            ######################################
#####################################################################################################

# Hub
hub_inner_radius = get_hub_inner_radius(propeller_coords, vect_length)
hub_radius = param_hub_radius(propeller_coords)
print("Hub radius: " + str(hub_radius))

# Tip radius
tip_radius = get_tip_radius(propeller_coords)
print("Tip radius:" + str(tip_radius))

# Blade twist
blade_twist = get_blade_twist(x_list, y_right_list, y_left_list)
plot_blade_twist(blade_twist, position)

#Chord length
chord_length = get_chord_length(x_list, y_right_list, y_left_list)
plot_chord_length(chord_length, position)


for i in range(len(all_plane_points) - rm):
    plot_interpolation_param(right_pts[i], left_pts[i], x_list[i], y_right_list[i], y_left_list[i], i, "Aerofoil at " + str(round(position[i], 2)) + "mm from hub", chord_length, blade_twist)