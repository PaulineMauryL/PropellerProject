# Arrows found in https://sebastianraschka.com/Articles/2014_pca_step_by_step.html

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
from myMathFunction import findMinMaxDF
import numpy as np 

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

def plot_eigenvectors(propeller_coords, vect_upper):
	fig = plt.figure()

	ax = fig.add_subplot(111, projection = '3d')
	#ax.scatter(x_coord, y_coord, z_coord) # marche aussi

	#ax.scatter(propeller_coords["X"], propeller_coords["Y"], propeller_coords["Z"])

	# markersize et alpha contrôlent la taille des points, i.e. le rendering de l'objet
	ax.plot(propeller_coords["X"], propeller_coords["Y"], propeller_coords["Z"], 'o', markersize=3, alpha=0.2)

	downlim, uplim = findMinMaxDF(propeller_coords)

	ax.plot([np.mean(propeller_coords["X"])], [np.mean(propeller_coords["Y"])], [np.mean(propeller_coords["Z"])],
	        'o', markersize=10, color='red', alpha=0.5)

	a = Arrow3D([np.mean(propeller_coords["X"]), np.mean(propeller_coords["X"]) - vect_upper[0]], 
            [np.mean(propeller_coords["Y"]), np.mean(propeller_coords["Y"]) - vect_upper[1]], 
            [np.mean(propeller_coords["Z"]), np.mean(propeller_coords["Z"]) - vect_upper[2]], 
            mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
	ax.add_artist(a)

	ax.set_xlabel('x_values')
	ax.set_ylabel('y_values')
	ax.set_zlabel('z_values')

	ax.set_xlim([downlim, uplim]);
	ax.set_ylim([downlim, uplim]);
	ax.set_zlim([downlim, uplim]);

	plt.title('Main direction')

	plt.show()


def plot_pointcloud(propeller_coords):
	fig = plt.figure()

	ax = fig.add_subplot(111, projection = '3d')
	ax.plot(propeller_coords["X"], propeller_coords["Y"], propeller_coords["Z"], 'o', markersize=3, alpha=0.2)

	downlim, uplim = findMinMaxDF(propeller_coords)

	ax.plot([np.mean(propeller_coords["X"])], [np.mean(propeller_coords["Y"])], [np.mean(propeller_coords["Z"])],
	        'o', markersize=10, color='red', alpha=0.5)

	ax.set_xlabel('x_values')
	ax.set_ylabel('y_values')
	ax.set_zlabel('z_values')

	ax.set_xlim([downlim, uplim]);
	ax.set_ylim([downlim, uplim]);
	ax.set_zlim([downlim, uplim]);

	plt.title('Point cloud')

	plt.show()