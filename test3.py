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

#####################################################################################################
##########################            PRE-PROCESSING            #####################################
#####################################################################################################
propeller_coords, vect_length, vect_out, vect_side = prepare_propeller(propeller)



hub_inner_radius = get_hub_inner_radius(propeller_coords, vect_length)

middle_point, highest_point, lowest_point = extreme_points(propeller_coords)
dmiddle  = - middle_point @ vect_length
hub_points = get_hub_points(propeller_coords, dmiddle, vect_length)

point_outer_radius, point_inner_radius = get_hub_radius(hub_points, middle_point, hub_inner_radius, vect_side)

#plot_hub(propeller_coords, hub_points, point_outer_radius, point_inner_radius)


'''
#plot_pointcloud(propeller_coords)
#plot_direction(propeller_coords, vect_length, vect_out, vect_side)

dmiddle, dlowest, dhighest   = d_blade(vect_length, propeller_coords)                     #d of plan ax+by+cx+d = 0
upper_blade, lower_blade     = blade_alone(propeller_coords, vect_length, dmiddle)        #points of each blades

#plot_pointcloud(upper_blade)




nb_seg = 2
planes, delta_d = get_planes(upper_blade, dmiddle, dlowest, vect_length, nb_seg)   #get equations of planes for projection
#segments = get_segments(upper_blade, planes, nb_seg)
#plot_segments(segments)

all_plane_points = get_points(upper_blade, planes)                                 #get points used for each projection

right_param, left_param, right_pts, left_pts = get_all_projections(planes, all_plane_points)

x_list, y_right_list, y_left_list, right_pts, left_pts, position, rm = get_generated_points(right_param, left_param, right_pts, left_pts, delta_d)


plot_interpolation_both_sides(right_pts[0], left_pts[0], x_list[0], y_right_list[0], y_left_list[0], 1, "Generated points")

'''