from plot_projections import plot_all_projections, plot_final_projections, plot_point_for_couple
from prop_info import extreme_points, vect_blade, d_blade
from get_segments import blade_alone, get_segments_points, get_planes
from major_axis import get_major_axis
from projections import couple_all_planes, project_all_couples, projections_by_side, project_couple
from parameters import get_hub_points, get_hub_radius
from plot_param import plot_hub

import pandas as pd
import numpy as np

# read dataframe

print("Begin pre-processing")
propeller = pd.read_csv('aerostar_data.csv')

propeller_coords = propeller.drop_duplicates(subset=None, keep='first', inplace=False)
propeller_coords = propeller_coords.reset_index(drop=True)
print(propeller_coords.shape)


max_point, min_point, middle_point, highest_point, lowest_point = extreme_points(propeller_coords)

vect_length = vect_blade(max_point, min_point) 

dmiddle, dhighest, dlowest = d_blade(vect_length, middle_point, highest_point, lowest_point)

upper_blade, lower_blade = blade_alone(propeller_coords, vect_length, dmiddle)

vect_out, vect_side, hub_inner_radius = get_major_axis(propeller_coords, middle_point, vect_length)
print("Finish pre-processing")
#plot_direction(propeller_coords, vect_length, vect_out, vect_side)
#plot_pointcloud(propeller_coords)
#plot_eigenvectors(propeller_coords, vect_upper)

print("Begin projections")

nb_seg = 3
planes = get_planes(upper_blade, dmiddle, dhighest, vect_length, nb_seg)

segments = get_segments_points(upper_blade, planes, nb_seg)

nb_point = 200
proj_up, proj_down, point_down, point_up = projections_by_side(nb_seg, planes, segments, nb_point)

#plot_all_projections(proj_up, proj_down)

#plot_point_for_couple(point_up, point_down)

down, up = couple_all_planes(proj_down, proj_up, nb_seg)

#plot_point_for_couple(up, up)
#plot_point_for_couple(down, down)


projections_df = project_all_couples(planes, up, down)

plot_final_projections(projections_df)
'''
couples, down, up = couple_all_planes(proj_down, proj_up, nb_seg)

projections_df = project_all_couples(couples, planes, up, down)

plot_final_projections(projections_df)
'''
print("Finish projection")

## Parameters part
'''
hub_points = get_hub_points(propeller_coords, dmiddle, vect_length)

hub_outer_radius, hub_inner_radius = get_hub_radius(hub_points, middle_point, vect_side, hub_inner_radius)

hub_radius = hub_outer_radius - middle_point  #from center to exterior radius
hub_radius_norm = np.linalg.norm(hub_radius)

plot_hub(propeller_coords, hub_points, hub_outer_radius, hub_inner_radius)
'''
