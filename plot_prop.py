# Arrows found in https://sebastianraschka.com/Articles/2014_pca_step_by_step.html

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
from myMathFunction import findMinMaxDF
import numpy as np 
import pandas as pd

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

def plot_direction(propeller_coords, vect_blade, vect_out, vect_side):
	#print("plot with blade {}\n out {}\n side{}".format(vect_blade, vect_out, vect_side))
	vect_blade = [x *100 for x in vect_blade]
	vect_out = [x *100 for x in vect_out]
	vect_side = [x *100 for x in vect_side]
	
	fig = plt.figure()

	ax = fig.add_subplot(111, projection = '3d')
	#ax.scatter(x_coord, y_coord, z_coord) # marche aussi

	#ax.scatter(propeller_coords["X"], propeller_coords["Y"], propeller_coords["Z"])

	# markersize et alpha contrôlent la taille des points, i.e. le rendering de l'objet
	ax.plot(propeller_coords["X"], propeller_coords["Y"], propeller_coords["Z"], 'o', markersize=3, alpha=0.2)

	downlim, uplim = findMinMaxDF(propeller_coords)

	ax.plot([np.mean(propeller_coords["X"])], [np.mean(propeller_coords["Y"])], [np.mean(propeller_coords["Z"])],
	        'o', markersize=10, color='red', alpha=0.5)

	a = Arrow3D([np.mean(propeller_coords["X"]), np.mean(propeller_coords["X"]) + vect_blade[0]], 
            [np.mean(propeller_coords["Y"]), np.mean(propeller_coords["Y"]) + vect_blade[1]], 
            [np.mean(propeller_coords["Z"]), np.mean(propeller_coords["Z"]) + vect_blade[2]], 
            mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
	ax.add_artist(a)

	b = Arrow3D([np.mean(propeller_coords["X"]), np.mean(propeller_coords["X"]) + vect_out[0]], 
            [np.mean(propeller_coords["Y"]), np.mean(propeller_coords["Y"]) + vect_out[1]], 
            [np.mean(propeller_coords["Z"]), np.mean(propeller_coords["Z"]) + vect_out[2]], 
            mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
	ax.add_artist(b)

	c = Arrow3D([np.mean(propeller_coords["X"]), np.mean(propeller_coords["X"]) + vect_side[0]], 
            [np.mean(propeller_coords["Y"]), np.mean(propeller_coords["Y"]) + vect_side[1]], 
            [np.mean(propeller_coords["Z"]), np.mean(propeller_coords["Z"]) + vect_side[2]], 
            mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
	ax.add_artist(c)		

	#plt.axes().set_aspect('equal')
	ax.set_xlabel('x_values', fontsize=15)
	ax.set_ylabel('y_values', fontsize=15)
	ax.set_zlabel('z_values', fontsize=15)

	#plt.axis([0, 100, 0, 50, 0, uplim])
	
	ax.set_xlim([downlim, uplim]);
	ax.set_ylim([downlim, uplim]);
	ax.set_zlim([downlim, uplim]);

	plt.title('Main directions', fontsize=20)

	plt.show()






def plot_pointcloud(propeller_coords):
	fig = plt.figure()

	ax = fig.add_subplot(111, projection = '3d')
	ax.plot(propeller_coords["X"], propeller_coords["Y"], propeller_coords["Z"], 'o', markersize=3, alpha=0.2)

	downlim, uplim = findMinMaxDF(propeller_coords)

	#ax.plot([np.mean(propeller_coords["X"])], [np.mean(propeller_coords["Y"])], [np.mean(propeller_coords["Z"])],
	#        'o', markersize=10, color='red', alpha=0.5)

	ax.set_xlabel('x_values', fontsize=15)
	ax.set_ylabel('y_values', fontsize=15)
	ax.set_zlabel('z_values', fontsize=15)


	ax.set_xlim([downlim, uplim]);
	ax.set_ylim([downlim, uplim]);
	ax.set_zlim([downlim, uplim]);

	plt.title('Point cloud of lower blade', fontsize=20)

	plt.show()



def plot_segments(segments):
	segment_0 = segments["points"][0]
	segment_1 = segments["points"][1]
	segment_2 = segments["points"][2]
	segment_3 = segments["points"][3]
	segment_4 = segments["points"][4]

	seg_df_0 = pd.DataFrame(segment_0, columns = ['X','Y','Z'])
	seg_df_1 = pd.DataFrame(segment_1, columns = ['X','Y','Z'])
	seg_df_2 = pd.DataFrame(segment_2, columns = ['X','Y','Z'])
	seg_df_3 = pd.DataFrame(segment_3, columns = ['X','Y','Z'])
	seg_df_4 = pd.DataFrame(segment_4, columns = ['X','Y','Z'])

	fig = plt.figure()

	ax = fig.add_subplot(111, projection = '3d')

	ax.plot(seg_df_0["X"], seg_df_0["Y"], seg_df_0["Z"], 'co', markersize=2, alpha=0.2)
	ax.plot(seg_df_1["X"], seg_df_1["Y"], seg_df_1["Z"], 'bo', markersize=2, alpha=0.2)
	ax.plot(seg_df_2["X"], seg_df_2["Y"], seg_df_2["Z"], 'go', markersize=2, alpha=0.2)
	ax.plot(seg_df_3["X"], seg_df_3["Y"], seg_df_3["Z"], 'ro', markersize=2, alpha=0.2)
	ax.plot(seg_df_4["X"], seg_df_4["Y"], seg_df_4["Z"], 'mo', markersize=2, alpha=0.2)

	downlim, uplim = findMinMaxDF(seg_df_0)

	ax.set_xlabel('x_values', fontsize=15)
	ax.set_ylabel('y_values', fontsize=15)
	ax.set_zlabel('z_values', fontsize=15)

	ax.set_xlim([downlim, uplim]);
	ax.set_ylim([downlim, uplim]);
	ax.set_zlim([downlim, uplim]);

	plt.title('Segment', fontsize=20)

	plt.show()

def plot_projection(df_u, df_d):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(df_d["X"], df_d["Y"], df_d["Z"], 'co', markersize=3, alpha=0.2)
    ax.plot(df_u["X"], df_u["Y"], df_u["Z"], 'ro', markersize=3, alpha=0.2)
    ax.set_xlabel('x_values', fontsize=15)
    ax.set_ylabel('y_values', fontsize=15)
    ax.set_zlabel('z_values', fontsize=15)
    plt.title('Projection on plane', fontsize=20)
    plt.show()