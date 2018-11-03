from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt
from myMathFunction import findMinMaxDF
from new_projections import model_func
import numpy as np 
import pandas as pd

def plot_border(up_right, up_left, dn_right, dn_left):
    fig = plt.figure()

    ax = fig.add_subplot(111, projection = '3d')
    for i in range(len(up_right)):
        ax.plot([up_right[i][0]], [up_right[i][1]], [up_right[i][2]], 'k.', markersize=8, alpha=0.6)#, label = "Upper segment, side 1")
        ax.plot([up_left[i][0]],  [up_left[i][1]],  [up_left[i][2]],  'k.', markersize=8, alpha=0.6)#, label = "Upper segment, side 2")

        ax.plot([dn_right[i][0]], [dn_right[i][1]], [dn_right[i][2]], 'r.', markersize=8, alpha=0.6)#, label = "Down segment, side 1")
        ax.plot([dn_left[i][0]],  [dn_left[i][1]],  [dn_left[i][2]],  'r.', markersize=8, alpha=0.6)#, label = "Down segment, side 2")

    ax.set_xlabel('X', fontsize=20)
    ax.set_ylabel('Y', fontsize=20)
    ax.set_zlabel('Z', fontsize=20)

    plt.title('Border points', fontsize=20)
    plt.legend()
    plt.show()

def plot_projection_up_down(df_u, df_d):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(df_d["X"], df_d["Y"], df_d["Z"], 'k.', markersize=3, alpha=0.6)
    ax.plot(df_u["X"], df_u["Y"], df_u["Z"], 'r.', markersize=3, alpha=0.6)

    ax.set_xlabel('X', fontsize=20)
    ax.set_ylabel('Y', fontsize=20)
    ax.set_zlabel('Z', fontsize=20)
    '''
    downlim, uplim = findMinMaxDF(df_u)
    
    ax.set_xlim([downlim, uplim]);
    ax.set_ylim([downlim, uplim]);
    ax.set_zlim([downlim, uplim]);
    '''   
    plt.title('Projection on plane', fontsize=20)
    plt.show()



def plot_point_for_couple(point_up, point_down):
    toplotup = []
    labels = ['X', 'Y', 'Z']
    for i in point_up:
        toplotup.append( pd.DataFrame(i, columns = labels) )
    toplotdn = []
    for i in point_down:
        toplotdn.append( pd.DataFrame(i, columns = labels) )
    plot_all_projections(toplotup, toplotdn)



def plot_all_projections(proj_up, proj_down):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i, elem in enumerate(proj_down):
        ax.plot(proj_down[i]["X"], proj_down[i]["Y"], proj_down[i]["Z"], 'k.', markersize=3, alpha=0.6)
    for i, elem in enumerate(proj_up):
        ax.plot(proj_up[i]["X"], proj_up[i]["Y"], proj_up[i]["Z"], 'r.', markersize=3, alpha=0.6)

    ax.set_xlabel('X', fontsize=20)
    ax.set_ylabel('Y', fontsize=20)
    ax.set_zlabel('Z', fontsize=20)

    #downlim, uplim = (0,100) #findMinMaxDF(proj_down)

    ax.set_xlim([15, 50]);
    ax.set_ylim([0, 35]);
    ax.set_zlim([0, 35]);

    plt.title('Projections on cross sections', fontsize=20)
    plt.show()
    
    

def plot_final_projections(projections_df):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    i = 0
    for plan in projections_df:
        #print(plan)
        ax.plot(plan['X'], plan['Y'], plan['Z'], 'x', markersize=4, alpha=0.8, label = "Plan" + str(i))
        i = i + 1
    ax.set_xlabel('x_values', fontsize=15)
    ax.set_ylabel('y_values', fontsize=15)
    ax.set_zlabel('z_values', fontsize=15)
    plt.title('Projections on plane', fontsize=20)
    plt.legend()
    plt.show()
    fig.savefig('Projections_on_plane.png')


def plot_least_squares(X, Y, Z, data):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.6)
    ax.scatter(data[:,0], data[:,1], data[:,2], c='k', s=10)

    plt.xlabel('X')
    plt.ylabel('Y')
    ax.set_zlabel('Z')

    ax.axis('equal')
    ax.axis('tight')

    plt.title('Least squares', fontsize=20)
    plt.legend()

    plt.show()


def plot_interpolation_side(up_right_border, up_left_border, popt, i):  
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    range_X_up_r = np.linspace(up_right_border[0], up_left_border[0], 100)
    range_Y_up_r = np.linspace(up_right_border[1], up_left_border[1], 100)
    
    data = np.c_[range_X_up_r, range_Y_up_r]
    z = model_func(data, *popt)

    plt.plot(range_X_up_r, range_Y_up_r, z, 'k')
    plt.title(i)
    plt.show()