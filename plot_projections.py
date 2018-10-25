from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt
from myMathFunction import findMinMaxDF
import numpy as np 
import pandas as pd


def plot_projection_up_down(df_u, df_d):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(df_d["X"], df_d["Y"], df_d["Z"], 'co', markersize=3, alpha=0.2)
    ax.plot(df_u["X"], df_u["Y"], df_u["Z"], 'ro', markersize=3, alpha=0.2)
    ax.set_xlabel('x_values', fontsize=15)
    ax.set_ylabel('y_values', fontsize=15)
    ax.set_zlabel('z_values', fontsize=15)

    downlim, uplim = findMinMaxDF(df_u)

    ax.set_xlim([downlim, uplim]);
    ax.set_ylim([downlim, uplim]);
    ax.set_zlim([downlim, uplim]);

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
        ax.plot(proj_down[i]["X"], proj_down[i]["Y"], proj_down[i]["Z"], 'go', markersize=3, alpha=0.2)
    for i, elem in enumerate(proj_up):
        ax.plot(proj_up[i]["X"], proj_up[i]["Y"], proj_up[i]["Z"], 'ro', markersize=3, alpha=0.2)
    ax.set_xlabel('x_values', fontsize=15)
    ax.set_ylabel('y_values', fontsize=15)
    ax.set_zlabel('z_values', fontsize=15)
    plt.title('Projections on plane', fontsize=20)
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