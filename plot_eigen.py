import numpy as np
from stl import mesh 
from mpl_toolkits import mplot3d 
import matplotlib.pyplot as plt


def plot_eigen(mesh, eigenvectors):
	'''Scatter the lines of allpoints_array and add arrow of eigenvectors
		allpoints_array is np.ndarray of shape (38940,3)
		eigenvectors are the two first eigenvectors : (2,3)
	'''
	# Create a new plot
	figure = plt.figure()
	axes = mplot3d.Axes3D(figure)
	
	#plt.plot(eigenvectors[:,0], eigenvectors[:,1])
	axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh.vectors))

	scale = mesh.points.flatten(-1) 
	axes.auto_scale_xyz(scale, scale, scale)

	# Add the vectors to the plot  --> from allpoints in points and eigen in arrows

	#Axes3D.scatter


	#Add PCA vector to plot
	#pyplot.quiver(eigenvectors,color=['r'], scale=21)

	plt.title('Eigenvectors')

	# Show the plot to the screen
	plt.show()