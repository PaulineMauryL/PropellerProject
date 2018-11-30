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


def plot_interpolation_param(right_points, left_points, x, y_right, y_left, i, title, chord_length, blade_twist):      

    fig = plt.figure()
    fig.add_subplot(111)


    #Plot chord length
    plt.plot([x[0], x[-1]], [y_right[0], y_right[-1]], "r-", label="Chord length", linewidth = 4);

    #Plot blade twist
    '''
    direction = np.zeros([2, 1])
    direction[0] = x[-1] - x[0]  #x[-1] - x[0]
    direction[1] = y_right[-1] - y_right[0]
    angle =  math.acos( direction[0] / math.sqrt(direction[0]**2 + direction[1]**2) ) * 180 / math.pi
    '''

    #Plot interpolated points
    _, _, _, highest, lowest = extreme_points(right_points)
    x = np.linspace(lowest[0], highest[0], 100)
    plt.scatter(x, y_right, color='b', label="Interpolated points (up)")
    plt.scatter(x, y_left, color ='c', label="Interpolated points (down)")

    #Plot real points
    plt.scatter(right_points["X"], right_points["Y"], color='g', marker='^', label="Real points (up)")
    plt.scatter(left_points["X"],  left_points["Y"],  color='m', marker='^', label="Real points (down)")

    plt.xlabel('x_values', fontsize=15)
    plt.ylabel('y_values', fontsize=15)

    cl = str(round(chord_length[i], 2))
    bt = str(round(blade_twist[i], 2))

    plt.text(0, -4, "Chord length " + cl + "mm", {'color': 'r', 'fontsize': 10})
    plt.text(0, -5, "Blade twist " + bt + "mm", {'color': 'k', 'fontsize': 10})

    plt.legend()
    plt.title(title)
    plt.axis([-25, 15, -6, 6])
    plt.show()
    fig.savefig('Image/' + title + '.png')

