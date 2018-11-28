from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
from prop_info import extreme_points
from myMathFunction import *
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


def plot_interpolation_param(right_popt, right_points, left_popt, left_points, x, y_right, y_left, i, title):      

    if(type(right_popt) == int or type(left_popt) == int):
        print("Plane {} does not have enough points for interpolation".format(i))

    else:
        fig = plt.figure()
        fig.add_subplot(111)
        
        maxx = max(x)
        minx = min(x)
        y_right_max = func_4_scalar(maxx, *right_popt)
        y_right_min = func_4_scalar(minx, *right_popt)

        plt.plot([minx, maxx], [y_right_min, y_right_max]);

        _, _, _, highest, lowest = extreme_points(right_points)
        x = np.linspace(lowest[0], highest[0], 100)

        #data_right = right_points.values[:,0]
        y_right = func_4_scalar(x, *right_popt)
        plt.scatter(x, y_right)
        plt.scatter(right_points["X"], right_points["Y"])
        
        #data_left = left_points.values[:,0]
        y_left = func_4_scalar(x, *left_popt)
        plt.scatter(x, y_left)
        plt.scatter(left_points["X"], left_points["Y"])

        plt.xlabel('x_values', fontsize=15)
        plt.ylabel('y_values', fontsize=15)

        plt.title(title)
        plt.axis([-25, 15, -6, 6])
        plt.show()
        fig.savefig('Image/' + title + '.png')
