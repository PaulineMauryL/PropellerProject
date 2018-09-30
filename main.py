import numpy as np 
from stl import mesh

propellerMesh = mesh.Mesh.from_file('propeller.stl') #fill here 


# The mesh normals 
propellerMesh.normals      #liste de vecteur à 3 dimensions
#print(len(propellerMesh.normals))  #12'980

# The mesh vectors
propellerMesh.v0, propellerMesh.v1, propellerMesh.v2
propellerMesh.v0                   #liste de vecteur à 3 dimensions
#print(len(propellerMesh.v0))      #12980

#print(propellerMesh.x)
minx = min(point for vect in propellerMesh.x for point in vect)
maxx = max(point for vect in propellerMesh.x for point in vect)

miny = min(point for vect in propellerMesh.y for point in vect)
maxy = max(point for vect in propellerMesh.y for point in vect)

minz = min(point for vect in propellerMesh.z for point in vect)
maxz = max(point for vect in propellerMesh.z for point in vect)
#maxz= max(l1    for l2   in l3              for l1    in l2)


width = maxx - minx
length = maxy - miny
height = maxz - minz

#print('Box_Length (x) : {}\nBox_Width (y) : {}\nBox_Height (z) : {}'.format(length, width, height))


#List of array of all points in 3D
allpoints = [liste for subliste in propellerMesh.vectors for liste in subliste]
allpoints_array = np.asarray(allpoints)
#print(allpoints_array)

def PCA(data, correlation = False, sort = True):
	""" Applies Principal Component Analysis to the data

	Parameters
	----------        
	data: array
	    The array containing the data. The array must have NxM dimensions, where each
	    of the N rows represents a different individual record and each of the M columns
	    represents a different variable recorded for that individual record.
	        array([
	        [V11, ... , V1m],
	        ...,
	        [Vn1, ... , Vnm]])

	correlation(Optional) : bool
	        Set the type of matrix to be computed (see Notes):
	            If True compute the correlation matrix.
	            If False(Default) compute the covariance matrix. 

	sort(Optional) : bool
	        Set the order that the eigenvalues/vectors will have
	            If True(Default) they will be sorted (from higher value to less).
	            If False they won't.   
	Returns
	-------
	eigenvalues: (1,M) array
	    The eigenvalues of the corresponding matrix.

	eigenvector: (M,M) array
	    The eigenvectors of the corresponding matrix.

	Notes
	-----
	The correlation matrix is a better choice when there are different magnitudes
	representing the M variables. Use covariance matrix in other cases.

	"""

	mean = np.mean(data, axis=0)

	data_adjust = data - mean

	#: the data is transposed due to np.cov/corrcoef syntax
	if correlation:

	    matrix = np.corrcoef(data_adjust.T)

	else:
	    matrix = np.cov(data_adjust.T) 

	eigenvalues, eigenvectors = np.linalg.eig(matrix)

	if sort:
	    #: sort eigenvalues and eigenvectors
	    sort = eigenvalues.argsort()[::-1]
	    eigenvalues = eigenvalues[sort]
	    eigenvectors = eigenvectors[:,sort]

	return eigenvalues, eigenvectors

eigenvalues, eigenvectors = PCA(allpoints_array)

main_direction = eigenvectors[0]

print(main_direction)

