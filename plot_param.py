from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
from prop_info import extreme_points
from myMathFunction import *
import numpy as np 
import pandas as pd

#theoretical_bt = [21.11, 23.9, 24.65, 24.11, 22.78, 21.01, 19, 17.06, 15.33, 13.82, 12.51, 11.36, 10.27, 9.32, 8.36, 7.27, 6.15, 5.04] 
#theoretical_cl = [0.109, 0.132, 0.156, 0.176, 0.193, 0.206, 0.216, 0.223, 0.226, 0.225, 0.219, 0.21, 0.197, 0.179, 0.157, 0.13, 0.087, 0.042]
def plot_hub(propeller_coords, hub_points, point_outer_radius, point_inner_radius):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.scatter(propeller_coords["X"], propeller_coords["Y"], propeller_coords["Z"], s=1, c='k', label = "Point cloud")
    
    ax.scatter(hub_points["X"], hub_points["Y"], hub_points["Z"], s=20, c='g', label = "Selected points")

    ax.scatter(point_outer_radius[0], point_outer_radius[1], point_outer_radius[2], s=50, c='r', label= "Outer radius")
    ax.scatter(point_inner_radius[0], point_inner_radius[1], point_inner_radius[2], s=50, c='r', label= "Inner radius")
    downlim, uplim = findMinMaxDF(propeller_coords)

    ax.set_xlabel('X (mm)', fontsize=20)
    ax.set_ylabel('Y (mm)', fontsize=20)
    ax.set_zlabel('Z (mm)', fontsize=20)
    
    ax.set_xlim([downlim, uplim]);
    ax.set_ylim([downlim, uplim]);
    ax.set_zlim([downlim, uplim]);
    
    plt.legend(loc=0, prop={'size':20})
    plt.title('Hub radius', fontsize=30)
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
    _, highest, lowest = extreme_points(right_points)
    x = np.linspace(lowest[0], highest[0], 100)
    plt.scatter(x, y_right, color='b', label="Interpolated points (up)")
    plt.scatter(x, y_left, color ='c', label="Interpolated points (down)")

    #Plot real points
    plt.scatter(right_points["X"], right_points["Y"], color='g', marker='^', label="Real points (up)")
    plt.scatter(left_points["X"],  left_points["Y"],  color='m', marker='^', label="Real points (down)")

    plt.xlabel('x', fontsize=15)
    plt.ylabel('y', fontsize=15)

    cl = str(round(chord_length[i], 2))
    bt = str(round(blade_twist[i], 2))

    plt.text(0, -4, "Chord length " + cl + "mm", {'color': 'r', 'fontsize': 10})
    plt.text(0, -5, "Blade twist " + bt + "deg", {'color': 'k', 'fontsize': 10})

    plt.legend()
    plt.title(title)
    plt.axis([-25, 15, -6, 6])
    plt.show()
    #fig.savefig('Report/plots/' + title + '.png')



def plot_blade_twist(blade_twist, position):
    fig = plt.figure()
    plt.plot(position, blade_twist, color="blue", linewidth=2.5)  
    plt.ylabel('Angle (in degrees)', fontsize=15)
    plt.xlabel('Position in mm (from hub to tip)', fontsize=15)
    plt.title("Blade twist", fontsize=20)
    #fig.savefig('Report/plots/Blade_twist.png')
    plt.show()


def plot_chord_length(chord_length, position):
    fig = plt.figure()
    plt.plot(position, chord_length, color="red", linewidth=2.5)  
    plt.ylabel('Chord length (mm)', fontsize=15)
    plt.xlabel('Position in mm (from hub to tip)', fontsize=15)
    plt.title("Chord length", fontsize=20)
    #fig.savefig('Report/plots/chord length.png')
    plt.show()

def plot_chord_blade(chord_length, blade_twist, position):
    fig = plt.figure()
    plt.plot(position, chord_length, color="red", linewidth=2.5)
    plt.plot(position, blade_twist, color="blue", linewidth=2.5)    
    plt.xlabel('Position in mm (from hub to tip)', fontsize=15)
    plt.title("Chord length and blade twist", fontsize=20)
    #fig.savefig('Report/plots/chord_blade.png')
    plt.show()

######################################################################################
#############################     RESULT COMPARISON    ###############################
######################################################################################

def plot_blade_twist_comparison(blade_twist, theoretical_bt, positions):
    fig = plt.figure()
   
    plt.plot(positions, blade_twist, color="blue", linewidth=2.5, label = "Computed")  
    plt.plot(positions, theoretical_bt, color="green", linewidth=2.5, label = "Real")
    plt.xlabel('r/R', fontsize=15)    
    plt.ylabel('Beta (degrees)', fontsize=15)
    plt.title("Blade twist", fontsize=20)
    plt.legend()
    fig.savefig('Report/plots/Blade_twist_comparison.png')
    plt.show()

def plot_chord_length_comparison(chord_length, theoretical_cl, positions):
    fig = plt.figure()    
    plt.plot(positions, chord_length, color="blue", linewidth=2.5, label = "Computed")  
    plt.plot(positions, theoretical_cl, color="green", linewidth=2.5, label = "Real")
    plt.xlabel('r/R', fontsize=15)    
    plt.ylabel('c/R', fontsize=15)
    plt.title("Chord length", fontsize=20)
    plt.legend()
    fig.savefig('Report/plots/Chord_length_comparison.png')
    plt.show()