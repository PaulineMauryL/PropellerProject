#https://stackoverflow.com/questions/38754668/plane-fitting-in-a-3d-point-cloud
import numpy as np 

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

