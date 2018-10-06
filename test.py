from plot_prop import plot_eigenvectors, plot_pointcloud
from prop_info import extreme_points, blade_info
from get_segments import blade_alone, get_segments
import pandas as pd
import numpy as np

# read dataframe
propeller_coords = pd.read_csv('propeller_data.csv')

max_point, min_point, middle_point = extreme_points(propeller_coords)

vect_upper, vect_lower, dmiddle, dmax, dmin = blade_info(max_point, min_point, middle_point)

upper_blade, lower_blade = blade_alone(propeller_coords, vect_upper, middle_point, dmiddle)

#plot_pointcloud(propeller_coords)
plot_eigenvectors(propeller_coords, vect_upper)
'''
segments = get_segments(upper_blade, dmiddle, dmax, vect_upper, 4)

#plot_pointcloud(propeller_coords)

for i, array in enumerate(segments["points"]):
    print(i)
    print(array)
'''
