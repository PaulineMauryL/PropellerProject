from plot_projections import plot_all_projections, plot_final_projections, plot_point_for_couple, plot_projection_up_down, plot_border
from prop_info import extreme_points, vect_blade, d_blade, center_prop
from get_segments import blade_alone, get_segments_points, get_planes
from major_axis import get_major_axis
#from projections import couple_all_planes, project_all_couples, projections_by_side, project_couple
from new_projections import assign_points, get_all_points_for_projections, interpolations, find_separation_plane
from parameters import get_hub_points, get_hub_radius
from plot_param import plot_hub
from plot_prop import plot_pointcloud, plot_direction, plot_segments
from myMathFunction import least_squares

import pandas as pd
import numpy as np

# read dataframe

print("Begin pre-processing")
propeller = pd.read_csv('aerostar_data.csv')
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
resolution = 3

planes = get_planes(upper_blade, dmiddle, dhighest, vect_length, nb_seg)
segments = get_segments_points(upper_blade, planes, nb_seg)
#plot_segments(segments)

up, down = get_all_points_for_projections(planes, segments, nb_seg, resolution)

### DO for one plane here, then will do for all
up1 = up[0]
dn1 = down[0]

# 1. Find border points
up_right, up_left, _, _, _ = extreme_points(up1)
dn_right, dn_left, _, _, _ = extreme_points(dn1)
#print("up_right {}\n".format(up_right))

# 2. Find separating plane
C_up = find_separation_plane(up1.values)
C_dn = find_separation_plane(dn1.values)
#print("C_up {}\n".format(C_up))


# 3. Assign point to side
right_points_up, left_points_up = assign_points(C_up, up1)
right_points_dn, left_points_dn = assign_points(C_dn, dn1)
print("right_points_up_shape {}\n".format(right_points_up.shape))

plot_projection_up_down(right_points_up, right_points_up)
'''
# 4. Interpolate points
from scipy.optimize import curve_fit
print(right_points_up)
print(right_points_up.shape)
'''
'''
def model_func(x, a, b, c, d):    
    return a*x**3 + b*x**2 + c*x + d

sigma = np.ones(len(x))
sigma[[0, -1]] = 0.01
popt, pcov = curve_fit(model_func, x, y, p0=(0.1 ,1e-3, 0.1), sigma=sigma)
'''


# 5. Projection




'''
print("X_up\n")
print(X_up)
print("Y_up\n")
print(Y_up)
print("Z_up\n")
print(Z_up)
'''

# plot points and fitted surface

# 2. Least squares approximation
#w_up_right = least_squares(up_right)




#print(up_right)

#plot_border(up_right, up_left, dn_right, dn_left)
#proj_up, proj_down, point_down, point_up = projections_by_side(nb_seg, planes, segments, nb_point)
#plot_projection_up_down(proj_up[1], proj_down[1])
#plot_all_projections(up, down)

#down, up = couple_all_planes(proj_down, proj_up, nb_seg)
#plot_point_for_couple(up, up)
#plot_point_for_couple(down, down)
#projections_df = project_all_couples(planes, up, down)
#plot_final_projections(projections_df)
#couples, down, up = couple_all_planes(proj_down, proj_up, nb_seg)
#projections_df = project_all_couples(couples, planes, up, down)
#plot_final_projections(projections_df)


print("Finish projection")





## Parameters part
'''
hub_points = get_hub_points(propeller_coords, dmiddle, vect_length)

hub_outer_radius, hub_inner_radius = get_hub_radius(hub_points, middle_point, vect_side, hub_inner_radius)

hub_radius = hub_outer_radius - middle_point  #from center to exterior radius
hub_radius_norm = np.linalg.norm(hub_radius)

plot_hub(propeller_coords, hub_points, hub_outer_radius, hub_inner_radius)
'''
