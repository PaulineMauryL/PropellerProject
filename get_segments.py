import numpy as np 
import pandas as pd

#keep one blade


def segment(allpoints_array, normal, nb_segments):
	""""Get the segments of the blade"""

	#print("normal is {}".format(normal))

	index_max_z = np.argmax(allpoints_array[:,2])
	#zmax = np.max(allpoints_array[:,2])
	index_min_z = np.argmin(allpoints_array[:,2])
	#zmin = np.min(allpoints_array[:,2])
	#print("Max z is {}".format( np.max(allpoints_array[:,2]) ) )
	#print("Min z is {}".format( np.min(allpoints_array[:,2]) ) )
	point_max = allpoints_array[index_max_z,:]
	point_min = allpoints_array[index_min_z,:]

	dmax = - point_max @ normal
	dmin = - point_min @ normal

	delta_d = (dmax - dmin)/nb_segments
	print("Delta d is {}".format(delta_d))

	last_plane = np.append(normal,dmin)
	print("Equation of last plan is {}".format(last_plane))

	new_plane[:] = last_plane[:]

	array_to_compare = allpoints_array[:]

	for i in range(nb_segments):
		new_plane[:] = last_plane[:] + [0, 0, 0, delta_d]
		print("Equation of new plan is {}".format(new_plane))

		segment_list = pd.DataFrame()
		point_in_segment = []
		index_to_remove = []
		###je veux mettre les points de chaque segments ensemble (liste ? classe ? dataframe ?)

		for j, elem in enumerate(array_to_compare):
			elem_mult = np.append(elem, 1)  #ajoute 1 pour d*1 (vecteur x y z 1) ou alors direct ajou
			if(elem_mult @ last_plane > 0 and elem_mult @ new_plane < 0)
				point_in_segment.append(elem_mult)
				index_to_remove.append(j)
				
				#il n'y aura pas forcement le meme nombre de point dans chaque

		######### remove elem from array_to_compare
		segment_list[j] = point_in_segment

		last_plane = new_plane[:]

		return segment_list #tout les segments avec leur points à chacun

def getBlade(allpoints_array, normal, point_mid):
	""""Get one blade of propeller"""

	d = - point_mid @ normal
	#print("d is {}".format(d))

	index_max_z = np.argmax(allpoints_array[:,2])
	#zmax = np.max(allpoints_array[:,2])
	index_min_z = np.argmin(allpoints_array[:,2])
	#zmin = np.min(allpoints_array[:,2])
	#print("Max z is {}".format( np.max(allpoints_array[:,2]) ) )
	#print("Min z is {}".format( np.min(allpoints_array[:,2]) ) )
	point_max = allpoints_array[index_max_z,:]
	point_min = allpoints_array[index_min_z,:]


	for i, elem in allpoints_array:
		elem_mult = np.append(elem, 1)  #ajoute 1 pour d*1 (vecteur x y z 1)
		if(elem_mult @ plane > 0)
			point_upper_blade.append(elem_mult)
		else :
			pont_lower_blade.append(elem_mult)
		
		return #upperblade and lowerblade
