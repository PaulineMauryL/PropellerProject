from plot_prop import plot_direction, plot_pointcloud, plot_segments, plot_all_projections
from prop_info import extreme_points, vect_blade, d_blade
from get_segments import blade_alone, get_segments_points, get_planes
from major_axis import get_major_axis
from projections import all_projections, couple_all_planes, project_all_couples
import pandas as pd
import numpy as np

# read dataframe
propeller_coords = pd.read_csv('aerostar_data.csv')

max_point, min_point, middle_point, highest_point, lowest_point = extreme_points(propeller_coords)

vect_length = vect_blade(max_point, min_point) 

dmiddle, dhighest, dlowest = d_blade(vect_length, middle_point, highest_point, lowest_point)

upper_blade, lower_blade = blade_alone(propeller_coords, vect_length, dmiddle)

vect_out, vect_side = get_major_axis(propeller_coords, middle_point, vect_length)


#plot_direction(propeller_coords, vect_length, vect_out, vect_side)
#plot_pointcloud(propeller_coords)
#plot_eigenvectors(propeller_coords, vect_upper)


nb_seg = 5
planes = get_planes(upper_blade, dmiddle, dhighest, vect_length, nb_seg)

segments = get_segments_points(upper_blade, planes, nb_seg)

nb_point = 1000
proj_up, proj_down = all_projections(nb_seg, planes, segments, nb_point)


#plot_projection(proj_up[2], proj_down[2])
#plot_all_projections(proj_up, proj_down)


couples = couple_all_planes(proj_down, proj_up, nb_seg)

projections_df = project_all_couples(couples, planes, proj_up, proj_down)


from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt

def plot_final_projections(projections_df):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for plan in projections_df["points"]:
        #print(plan)
        ax.plot(plan['X'], plan['Y'], plan['Z'], 'co', markersize=3, alpha=0.2)
        #for elem in plan.iterrows():
         #   ax.plot(elem[0], elem[1], elem[2], 'co', markersize=3, alpha=0.2)
    ax.set_xlabel('x_values', fontsize=15)
    ax.set_ylabel('y_values', fontsize=15)
    ax.set_zlabel('z_values', fontsize=15)
    plt.title('Projections on plane', fontsize=20)
    plt.show()

plot_final_projections(projections_df)