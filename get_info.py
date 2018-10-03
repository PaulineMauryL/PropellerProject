# https://media.readthedocs.org/pdf/numpy-stl/latest/numpy-stl.pdf
import math
import stl
from stl import mesh
import numpy as np

#volume, cog, inertia = propellerMesh.get_mass_properties()
#print("Volume                                  = {0}".format(volume))
#print("Position of the center of gravity (COG) = {0}".format(cog))
#print("Inertia matrix at expressed at the COG  = {0}".format(inertia[0,:]))
#print("                                          {0}".format(inertia[1,:]))
#print("                                          {0}".format(inertia[2,:]))


def getBox(propellerMesh):
    minx = min(point for vect in propellerMesh.x for point in vect)
    maxx = max(point for vect in propellerMesh.x for point in vect)

    miny = min(point for vect in propellerMesh.y for point in vect)
    maxy = max(point for vect in propellerMesh.y for point in vect)

    minz = min(point for vect in propellerMesh.z for point in vect)
    maxz = max(point for vect in propellerMesh.z for point in vect)
    #maxz= max(l1    for l2   in l3              for l1    in l2)

    return minx, maxx, miny, maxy, minz, maxz

def getSizeBox(minx, maxx, miny, maxy, minz, maxz):
    width = maxx - minx
    length = maxy - miny
    height = maxz - minz

    #print('\nBox_Length (x) : {}\nBox_Width (y) : {}\nBox_Height (z) : {}\n'.format(length, width, height))

    return length, width, height

def middleOfPropeller(minx, maxx, miny, maxy, minz, maxz):
    xmid = (minx + maxx)/2
    ymid = (miny + maxy)/2
    zmid = (minz + maxz)/2

    #print('\nx_middle (x) : {}\ny_middle (y) : {}\nz_middle (z) : {}\n'.format(xmid, ymid, zmid))
    
    return xmid, ymid, zmid
