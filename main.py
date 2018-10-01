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
#xmid, ymid, zmid = middleOfPropeller(minx, maxx, miny, maxy, minz, maxz)

class Blade:
	"""Class to represent blade of propeller alone"""
	def __init__(self, X, Y, Z):
		self.x = X
		self.y = Y
		self.z = Z



def keepUpperBlade(propellerMesh, pente):
	""""Keeps only set of points above z middle"""
	#minx, maxx, miny, maxy, minz, maxz = getBox(propellerMesh)
	xmid, ymid, zmid = middleOfPropeller(minx, maxx, miny, maxy, minz, maxz)

	zpoints = []
	xpoints = []
	ypoints = []
	nb = 0
	for i, vect in enumerate(propellerMesh.z) :
		for j, point in enumerate(vect) :
			#Orientation légèrement penchée. 
			#J'ai un point (xmid, ymid, zmid) et un vecteur (eigen[1])
			#Donc besoin de equation pour orientation du plan de coupe et condition
			##Equation de droite: z = mx + c  (m is 2nd_dir)
			if point >= zmid :   
				nb = nb + 1
				zpoints.append(propellerMesh.z[i][j])
				xpoints.append(propellerMesh.x[i][j])
				ypoints.append(propellerMesh.y[i][j])

	upperBlade = Blade(xpoints, ypoints, zpoints)
	print('nb :{}'.format(nb))
	return upperBlade

upperBlade = keepUpperBlade(propellerMesh, eigenvectors[1])

#bladeArray = zip(upperBlade.x, upperBlade.y, upperBlade.x)

print(propellerMesh.x)
print(len(propellerMesh.x))
print(len(upperBlade.x))


def choppingSegements(blade, cutting_plane):
	#devrait choisir regulierement les plans de coupe parralèle au eigenvectors 2
	#les segmentations sont les points entre 2 plans
	return coordinates

coordinates = choppingSegements(upperBlade, eigenvectors[1])