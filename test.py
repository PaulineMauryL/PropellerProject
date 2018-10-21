from plot_prop import plot_direction, plot_pointcloud, plot_segments, plot_all_projections
from prop_info import extreme_points, vect_blade, d_blade
from get_segments import blade_alone, get_segments_points, get_planes
from major_axis import get_major_axis
#from projections import couple_all_planes, project_all_couples, points_to_project, projections_by_side
from parameters import get_hub_points, get_hub_radius
from plot_param import plot_hub

import pandas as pd
import numpy as np

# read dataframe
propeller_coords = pd.read_csv('aerostar_data.csv')

max_point, min_point, middle_point, highest_point, lowest_point = extreme_points(propeller_coords)

vect_length = vect_blade(max_point, min_point) 

dmiddle, dhighest, dlowest = d_blade(vect_length, middle_point, highest_point, lowest_point)

upper_blade, lower_blade = blade_alone(propeller_coords, vect_length, dmiddle)

vect_out, vect_side, hub_inner_radius = get_major_axis(propeller_coords, middle_point, vect_length)
print("Finish pre-processing")
#plot_direction(propeller_coords, vect_length, vect_out, vect_side)
#plot_pointcloud(propeller_coords)
#plot_eigenvectors(propeller_coords, vect_upper)

## Projection part
'''
nb_seg = 5
planes = get_planes(upper_blade, dmiddle, dhighest, vect_length, nb_seg)
segments = get_segments_points(upper_blade, planes, nb_seg)
nb_point = 500
proj_up, proj_down, idx_up, idx_down = projections_by_side(nb_seg, planes, segments, nb_point)
couples = couple_all_planes(proj_down, proj_up, nb_seg)
down, up = points_to_project(segments, idx_up, idx_down, couples, nb_seg)
projections_df = project_all_couples(couples, planes, up, down)
#print("Finished projections")
plot_final_projections(projections_df)
'''

## Parameters part

hub_points = get_hub_points(propeller_coords, dmiddle, vect_length)

hub_outer_radius, hub_inner_radius = get_hub_radius(hub_points, middle_point, vect_side, hub_inner_radius)

hub_radius = hub_outer_radius - middle_point  #from center to exterior radius
hub_radius_norm = np.linalg.norm(hub_radius)

plot_hub(propeller_coords, hub_points, hub_outer_radius, hub_inner_radius)