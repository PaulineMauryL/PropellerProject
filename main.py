import numpy as np 
from stl import mesh
from pca import PCA
from get_info import getBox, getSizeBox, middleOfPropeller

propellerMesh = mesh.Mesh.from_file('propeller.stl') #fill here 


# The mesh normals 
propellerMesh.normals      #liste de vecteur à 3 dimensions
#print(len(propellerMesh.normals))  #12'980

# The mesh vectors
propellerMesh.v0, propellerMesh.v1, propellerMesh.v2
propellerMesh.v0                   #liste de vecteur à 3 dimensions
#print(len(propellerMesh.v0))      #12980

#print(propellerMesh.x)

#Get the outer box of the propeller position in file
minx, maxx, miny, maxy, minz, maxz = getBox(propellerMesh)
length, width, height = getSizeBox(minx, maxx, miny, maxy, minz, maxz)

# Get middle of propeller to only consider one blade
# Should work because propeller is symetrical
xmid, ymid, zmid = middleOfPropeller(minx, maxx, miny, maxy, minz, maxz)


#List of array of all points in 3D
allpoints = [liste for subliste in propellerMesh.vectors for liste in subliste]
allpoints_array = np.asarray(allpoints)
#print(allpoints_array)

eigenvalues, eigenvectors = PCA(allpoints_array)
main_direction = eigenvectors[0]

print('Main direction from PCA is {}'.format(main_direction))

