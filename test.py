from plot_prop import plot_direction, plot_pointcloud, plot_segments
from prop_info import extreme_points, blade_info
from get_segments import blade_alone, get_segments, get_planes
from major_axis import get_major_axis
import pandas as pd
import numpy as np

# read dataframe
propeller_coords = pd.read_csv('propeller_data.csv')
max_point, min_point, middle_point = extreme_points(propeller_coords)
vect_upper, vect_lower, vect_blade, dmiddle, dmax, dmin = blade_info(max_point, min_point, middle_point)
upper_blade, lower_blade = blade_alone(propeller_coords, vect_upper, middle_point, dmiddle)
vect_out, vect_side = get_major_axis(propeller_coords, middle_point, vect_blade)


#plot_direction(propeller_coords, vect_blade, vect_out, vect_side)
#plot_pointcloud(lower_blade)
#plot_eigenvectors(propeller_coords, vect_upper)
nb_seg = 5
planes = get_planes(upper_blade, dmiddle, dmax, vect_upper, nb_seg)
segments = get_segments(upper_blade, planes, nb_seg)
#print(segments)
plot_segments(segments)
#plot_pointcloud(propeller_coords)
'''
for i, array in enumerate(segments["points"]):
    print(i)
    print(array)
'''
