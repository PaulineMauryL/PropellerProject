from plot_projections import *
from prop_info import extreme_points, vect_blade, d_blade, center_prop
from get_segments import blade_alone, get_segments_points, get_planes
from major_axis import get_major_axis
#from projections import couple_all_planes, project_all_couples, projections_by_side, project_couple
from new_projections import *
#from parameters import get_hub_points, get_hub_radius
#from plot_param import plot_hub
#from plot_prop import plot_pointcloud, plot_direction, plot_segments
from myMathFunction import least_squares

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# read dataframe

print("Begin pre-processing")
propeller = pd.read_csv('propeller_data.csv')
propeller = center_prop(propeller)
#propeller = align_prop(propeller)

propeller_coords = propeller.drop_duplicates(subset=None, keep='first', inplace=False)
propeller_coords = propeller_coords.reset_index(drop=True)
#propeller_coords['Z'] = propeller_coords['Z'] - 200
#propeller_coords = propeller_coords.sub(propeller_coords.mean(axis=1), axis=0)
#print(propeller_coords.shape)

max_point, min_point, middle_point, highest_point, lowest_point = extreme_points(propeller_coords)
#TODO Put it in 0,0,0 coordinates

#plot_pointcloud(propeller_coords)
vect_length = vect_blade(max_point, min_point) 
dmiddle, dhighest, dlowest = d_blade(vect_length, middle_point, highest_point, lowest_point)
upper_blade, lower_blade = blade_alone(propeller_coords, vect_length, dmiddle)
vect_out, vect_side, hub_inner_radius = get_major_axis(propeller_coords, middle_point, vect_length)
print("Finish pre-processing")

#plot_direction(propeller_coords, vect_length, vect_out, vect_side)

#plot_pointcloud(propeller_coords)
#plot_eigenvectors(propeller_coords, vect_upper)

## Projection part



print("Begin projections")
nb_seg = 3
resolution = 10

planes = get_planes(upper_blade, dmiddle, dhighest, vect_length, nb_seg)
segments = get_segments_points(upper_blade, planes, nb_seg)
#plot_segments(segments)

up, down = get_all_points_for_projections(planes, segments, nb_seg, resolution)

### DO for one plane here, then will do for all
up1 = up[0]
dn1 = down[0]
plan1 = planes[0]
#print(up1.shape)

# 1. Find border points
up_side1_border, up_side2_border, _, _, _ = extreme_points(up1)
dn_side1_border, dn_side2_border, _, _, _ = extreme_points(dn1)
#print("up_right {}\n".format(up_right))

# 2. Find separating plane
C_up = find_separation_plane(up1.values)
C_dn = find_separation_plane(dn1.values)
# Z = C[4]*X**2. + C[5]*Y**2. + C[3]*X*Y + C[1]*X + C[2]*Y + C[0]
#print("C_up {}\n".format(C_up))




# 3. Assign point to side  (do it for both sides on both sides)
up_right_points, up_left_points = assign_points(C_up, up1)
dn_right_points, dn_left_points = assign_points(C_dn, dn1)
#print("right_points_up_shape {}\n".format(up_right_points.shape))
#plot_projection_up_down(right_points_up, right_points_up)

# Add border points to fit
up_right_points = add_border_points(up_right_points, up_side1_border, up_side2_border)
up_left_points  = add_border_points(up_left_points,  up_side1_border, up_side2_border)
dn_right_points = add_border_points(dn_right_points, dn_side1_border, dn_side2_border)
dn_left_points  = add_border_points(dn_left_points,  dn_side1_border, dn_side2_border)
#print("up_right_points_shape {}\n".format(up_right_points.shape))
plot_projection_up_down(up_right_points, up_left_points)
plot_projection_up_down(dn_right_points, dn_left_points)




# 4. Interpolate points
up_right_popt = interpolate_points(up_right_points)
up_left_popt  = interpolate_points(up_left_points)
dn_right_popt = interpolate_points(dn_right_points)
dn_left_popt  = interpolate_points(dn_left_points)

plot_interpolation_side(up_side1_border, up_side2_border, up_right_popt, "1")
plot_interpolation_side(up_side1_border, up_side2_border, up_left_popt, "2")
plot_interpolation_side(dn_side1_border, dn_side2_border, dn_right_popt, "3")
plot_interpolation_side(dn_side1_border, dn_side2_border, dn_left_popt, "4")

nb_points = 100

# 5. Projection
up_right_pts = points_from_curve(up_side1_border, up_side2_border, nb_points, up_right_popt)
dn_right_pts = points_from_curve(dn_side1_border, dn_side2_border, nb_points, dn_right_popt)

up_left_pts = points_from_curve(up_side1_border, up_side2_border, nb_points, up_left_popt) 
dn_left_pts = points_from_curve(dn_side1_border, dn_side2_border, nb_points, dn_left_popt)

# Projection de la ligne reliant 2 points sur le plan
proj_right_df, proj_left_df = project_points_on_plane(up_right_pts, dn_right_pts, up_left_pts, dn_left_pts, plan1)
plot_projection_up_down(proj_right_df, proj_left_df)
# 6. Interpolation surfacce
popt_right = interpolate_points(proj_right_df)
popt_left  = interpolate_points(proj_left_df)
print("Finish projection")





## Parameters part
'''
hub_points = get_hub_points(propeller_coords, dmiddle, vect_length)

hub_outer_radius, hub_inner_radius = get_hub_radius(hub_points, middle_point, vect_side, hub_inner_radius)

hub_radius = hub_outer_radius - middle_point  #from center to exterior radius
hub_radius_norm = np.linalg.norm(hub_radius)

plot_hub(propeller_coords, hub_points, hub_outer_radius, hub_inner_radius)
'''
