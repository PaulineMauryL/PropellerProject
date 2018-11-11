
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from plot_prop import *
from plot_projections import *
from prop_info import *
from get_segments import blade_alone, get_segments_points, get_planes
from major_axis import get_major_axis
from new_projections import *


print("Begin pre-processing")
propeller = pd.read_csv('propeller_data.csv')
#plot_pointcloud(propeller)

propeller = center_prop(propeller)
propeller = align_prop(propeller)
#plot_pointcloud(propeller)
print("Aligned")

propeller_coords = propeller.drop_duplicates(subset=None, keep='first', inplace=False)
propeller_coords = propeller_coords.reset_index(drop=True)

max_point, min_point, middle_point, highest_point, lowest_point = extreme_points(propeller_coords)
vect_length                = vect_blade(max_point, min_point) 
dmiddle, dhighest, dlowest = d_blade(vect_length, middle_point, highest_point, lowest_point)
upper_blade, lower_blade   = blade_alone(propeller_coords, vect_length, dmiddle)
vect_out, vect_side, hub_inner_radius = get_major_axis(propeller_coords, middle_point, vect_length)
print("Finish pre-processing")


print("Begin projections")
nb_seg = 3
size = 10  #propeller
#size = 3   #aerostar
planes = get_planes(upper_blade, dmiddle, dhighest, vect_length, nb_seg)
all_plane_points = get_points(propeller_coords, planes, size)




one_plane_point = all_plane_points[0]

#right_popt, right_points, left_popt, left_points = projection_results(one_plane_point)
side1_border, side2_border, _, _, _ = extreme_points(one_plane_point)
    
param_sides = find_separation_plane(one_plane_point.values)
one_plane_point.to_csv('points0.csv', index = False)

right_points, left_points = assign_points(param_sides, one_plane_point)
#right_points.to_csv('right_points_0.csv', index = False)
#left_points.to_csv('left_points_0.csv', index = False)



one_plane_point = all_plane_points[1]

#right_popt, right_points, left_popt, left_points = projection_results(one_plane_point)
side1_border, side2_border, _, _, _ = extreme_points(one_plane_point)
    
param_sides = find_separation_plane(one_plane_point.values)
one_plane_point.to_csv('points1.csv', index = False)

right_points, left_points = assign_points(param_sides, one_plane_point)
#right_points.to_csv('right_points_1.csv', index = False)
#left_points.to_csv('left_points_1.csv', index = False)



right_points = add_border_points(right_points, side1_border, side2_border)
left_points  = add_border_points(left_points,  side1_border, side2_border)
    
right_popt = interpolate_points(right_points)
left_popt  = interpolate_points(left_points)

#plot_interpolation_both_sides(right_popt, right_points, left_popt, left_points, "Aerofoil_weight0.1_cubic_interpolation")