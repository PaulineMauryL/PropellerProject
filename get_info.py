# https://media.readthedocs.org/pdf/numpy-stl/latest/numpy-stl.pdf
import math
import stl
from stl import mesh
import numpy as np

propellerMesh = mesh.Mesh.from_file('propeller.stl')


volume, cog, inertia = propellerMesh.get_mass_properties()
print("Volume                                  = {0}".format(volume))
print("Position of the center of gravity (COG) = {0}".format(cog))
print("Inertia matrix at expressed at the COG  = {0}".format(inertia[0,:]))
print("                                          {0}".format(inertia[1,:]))
print("                                          {0}".format(inertia[2,:]))


