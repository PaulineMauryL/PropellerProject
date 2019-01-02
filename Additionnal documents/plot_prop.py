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
	vect_out   = [x *100 for x in vect_out]
	vect_side  = [x *100 for x in vect_side]
	
	fig = plt.figure()

	ax = fig.add_subplot(111, projection = '3d')
	#ax.scatter(x_coord, y_coord, z_coord) # marche aussi

	#ax.scatter(propeller_coords["X"], propeller_coords["Y"], propeller_coords["Z"])

	# markersize et alpha contrôlent la taille des points, i.e. le rendering de l'objet
	pc, = ax.plot(propeller_coords["X"], propeller_coords["Y"], propeller_coords["Z"], 'k.', markersize=5, alpha=0.6, label = "Point cloud")

	downlim, uplim = findMinMaxDF(propeller_coords)

	mp, = ax.plot([np.mean(propeller_coords["X"])], [np.mean(propeller_coords["Y"])], [np.mean(propeller_coords["Z"])],
	        '*', markersize=20, color='red', alpha=1, label = "Middle point")

	a = Arrow3D([np.mean(propeller_coords["X"]), np.mean(propeller_coords["X"]) + vect_blade[0]], 
            [np.mean(propeller_coords["Y"]), np.mean(propeller_coords["Y"]) + vect_blade[1]], 
            [np.mean(propeller_coords["Z"]), np.mean(propeller_coords["Z"]) + vect_blade[2]], 
            mutation_scale=20, lw=5, arrowstyle="-|>", color="green", label = "Point cloud")
	ax.add_artist(a)

	b = Arrow3D([np.mean(propeller_coords["X"]), np.mean(propeller_coords["X"]) + vect_out[0]], 
            [np.mean(propeller_coords["Y"]), np.mean(propeller_coords["Y"]) + vect_out[1]], 
            [np.mean(propeller_coords["Z"]), np.mean(propeller_coords["Z"]) + vect_out[2]], 
            mutation_scale=20, lw=5, arrowstyle="-|>", color="blue")
	ax.add_artist(b)

	c = Arrow3D([np.mean(propeller_coords["X"]), np.mean(propeller_coords["X"]) + vect_side[0]], 
            [np.mean(propeller_coords["Y"]), np.mean(propeller_coords["Y"]) + vect_side[1]], 
            [np.mean(propeller_coords["Z"]), np.mean(propeller_coords["Z"]) + vect_side[2]], 
            mutation_scale=20, lw=5, arrowstyle="-|>", color="red")
	ax.add_artist(c)		

	# Define an arbitrary legend handle with a proxy:
	#rec1 = plt.Rectangle((0, 0), 1, 1, fc='blue', lw=0, alpha=0.25)

	# Generate the legend:
	handles = [pc, mp, a, b, c]
	labels = ["Point cloud", "Middle point", "n", "v", "w"]
	ax.legend(handles, labels, loc=4, prop={'size': 25})

	#plt.axes().set_aspect('equal')
	ax.set_xlabel('X (mm)', fontsize=20)
	ax.set_ylabel('Y (mm)', fontsize=20)
	ax.set_zlabel('Z (mm)', fontsize=20)

	#plt.axis([0, 100, 0, 50, 0, uplim])
	
	ax.set_xlim([downlim, uplim]);
	ax.set_ylim([downlim, uplim]);
	ax.set_zlim([downlim, uplim]);

	plt.tight_layout()
	plt.title('Principal directions of propeller', fontsize=30)

	plt.show()




def plot_pointcloud(propeller_coords):
	fig = plt.figure()

	ax = fig.add_subplot(111, projection = '3d')
	ax.plot(propeller_coords["X"], propeller_coords["Y"], propeller_coords["Z"], 'k.', markersize=5, alpha=0.6)

	downlim, uplim = findMinMaxDF(propeller_coords)

	#ax.plot([np.mean(propeller_coords["X"])], [np.mean(propeller_coords["Y"])], [np.mean(propeller_coords["Z"])],
	#        'o', markersize=10, color='red', alpha=0.5)

	ax.set_xlabel('X (mm)', fontsize=20)
	ax.set_ylabel('Y (mm)', fontsize=20)
	ax.set_zlabel('Z (mm)', fontsize=20)


	ax.set_xlim([-75, 75]);
	ax.set_ylim([-75, 75]);
	ax.set_zlim([0, 130]);

	plt.tight_layout()
	plt.title('Upper blade point cloud', fontsize=30)

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

	ax.plot(seg_df_0["X"], seg_df_0["Y"], seg_df_0["Z"], 'k.', markersize=8, alpha=1, label = "Points of segment 0")
	ax.plot(seg_df_1["X"], seg_df_1["Y"], seg_df_1["Z"], 'b.', markersize=8, alpha=1, label = "Points of segment 1")
	ax.plot(seg_df_2["X"], seg_df_2["Y"], seg_df_2["Z"], 'g.', markersize=8, alpha=1, label = "Points of segment 2")
	ax.plot(seg_df_3["X"], seg_df_3["Y"], seg_df_3["Z"], 'r.', markersize=8, alpha=1, label = "Points of segment 3")
	ax.plot(seg_df_4["X"], seg_df_4["Y"], seg_df_4["Z"], 'm.', markersize=8, alpha=1, label = "Points of segment 4")

	downlim, uplim = findMinMaxDF(seg_df_0)

	ax.set_xlabel('X (mm)', fontsize=20)
	ax.set_ylabel('Y (mm)', fontsize=20)
	ax.set_zlabel('Z (mm)', fontsize=20)

	ax.set_xlim([-75, 75]);
	ax.set_ylim([-75, 75]);
	ax.set_zlim([0, 130]);

	plt.title('Segments of points between planes', fontsize=30)
	plt.legend(loc=0, prop={'size':20})

	plt.show()

    
    
