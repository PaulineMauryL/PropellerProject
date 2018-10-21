from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
from myMathFunction import findMinMaxDF
import numpy as np 
import pandas as pd


def plot_hub(propeller_coords, hub_points, point_outer_radius, point_inner_radius):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.plot(propeller_coords["X"], propeller_coords["Y"], propeller_coords["Z"], 'ro', markersize=0.3, alpha=0.2)
    ax.plot(hub_points["X"], hub_points["Y"], hub_points["Z"], 'co', markersize=0.3, alpha=0.2)
    

    ax.scatter(point_outer_radius[0], point_outer_radius[1], point_outer_radius[2], s=25, c='k')
    ax.scatter(point_inner_radius[0], point_inner_radius[1], point_inner_radius[2], s=25, c='k')
    downlim, uplim = findMinMaxDF(propeller_coords)

    ax.set_xlabel('x_values', fontsize=15)
    ax.set_ylabel('y_values', fontsize=15)
    ax.set_zlabel('z_values', fontsize=15)
    
    ax.set_xlim([downlim, uplim]);
    ax.set_ylim([downlim, uplim]);
    ax.set_zlim([downlim, uplim]);
    
    plt.title('Hub radius', fontsize=20)
    plt.show()
