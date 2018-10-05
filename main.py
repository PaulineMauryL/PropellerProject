import numpy as np 
from stl import mesh
from pca import PCA
from get_info import getBox, getSizeBox, middleOfPropeller
from plot_eigen import plot_eigen
#from get_segments import segment

propellerMesh = mesh.Mesh.from_file('propeller.stl')


#Get the outer box of the propeller position in file
minx, maxx, miny, maxy, minz, maxz = getBox(propellerMesh)
length, width, height = getSizeBox(minx, maxx, miny, maxy, minz, maxz)
xmid, ymid, zmid = middleOfPropeller(minx, maxx, miny, maxy, minz, maxz)
point_mid = np.asarray([xmid, ymid, zmid])
#print("point  is {}".format(point_mid))



#List of array of all points in 3D
allpoints = [liste for subliste in propellerMesh.vectors for liste in subliste]
allpoints_array = np.asarray(allpoints)			# np.ndarray of shape (38940,3)
#print("Allpoints array is {} of shape {}".format(allpoints_array, allpoints_array.shape))  


eigenvalues, eigenvectors = PCA(allpoints_array)                   #scikit-learn
#print('Main direction from PCA is {}'.format(eigenvectors[0]))

print(propellerMesh.vectors)
#plot_eigen(propellerMesh, eigenvectors[0:2])

#print("ha")
#print(eigenvectors[0:2])
#print("ha")

#  Get middle of propeller to only consider one blade
#  Should work because propeller is symetrical
#xmid, ymid, zmid = middleOfPropeller(minx, maxx, miny, maxy, minz, maxz)

#segment(allpoints_array, eigenvectors[0], 8)

