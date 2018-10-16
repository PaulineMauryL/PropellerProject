from stl import mesh
import numpy as np
import pandas as pd


stl_file = input('Enter your stl file name: ')

propellerMesh = mesh.Mesh.from_file(stl_file + '.stl')


x_coord = [x for ls in propellerMesh.x for x in ls]
y_coord = [y for ls in propellerMesh.y for y in ls]
z_coord = [z for ls in propellerMesh.z for z in ls]



propeller_coords = pd.DataFrame()

propeller_coords["X"] = x_coord
propeller_coords["Y"] = y_coord
propeller_coords["Z"] = z_coord

# to save the dataframe
propeller_coords.to_csv(stl_file + '_data.csv', index = False)