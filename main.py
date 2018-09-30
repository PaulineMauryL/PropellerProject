import numpy as np 
from stl import mesh
from pca import PCA
from get_info import getBox, getSizeBox, middleOfPropeller


propellerMesh = mesh.Mesh.from_file('propeller.stl')

#List of array of all points in 3D
allpoints = [liste for subliste in propellerMesh.vectors for liste in subliste]
allpoints_array = np.asarray(allpoints)
#print(allpoints_array)

eigenvalues, eigenvectors = PCA(allpoints_array)
main_direction = eigenvectors[0]
print('Main direction from PCA is {}'.format(main_direction))


#Get the outer box of the propeller position in file
minx, maxx, miny, maxy, minz, maxz = getBox(propellerMesh)
length, width, height = getSizeBox(minx, maxx, miny, maxy, minz, maxz)

# Get middle of propeller to only consider one blade
# Should work because propeller is symetrical
xmid, ymid, zmid = middleOfPropeller(minx, maxx, miny, maxy, minz, maxz)

class Blade:
	"""Class to represent blade of propeller alone"""
	def __init__(self, X, Y, Z):
		self.x = X
		self.y = Y
		self.z = Z



def keepUpperBlade(propellerMesh):
	minx, maxx, miny, maxy, minz, maxz = getBox(propellerMesh)
	xmid, ymid, zmid = middleOfPropeller(minx, maxx, miny, maxy, minz, maxz)

	zpoints = [point for vect in propellerMesh.z for point in vect if point > zmid]
	print('z done')
	xpoints = [point for vect in propellerMesh.x for point in vect if zpoints in propellerMesh.z]
	print('x done')
	ypoints = [point for vect in propellerMesh.y for point in vect if zpoints in propellerMesh.z]
	print('y done')

	upperBlade = Blade(xpoints, ypoints, zpoints)

	return upperBlade

#print(propellerMesh.z)
upperBlade = keepUpperBlade(propellerMesh)

#print(upperBlade)
