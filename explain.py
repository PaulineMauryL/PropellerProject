#to understand structure of Mesh

# The mesh normals 
propellerMesh.normals      #liste de vecteur à 3 dimensions
#print(len(propellerMesh.normals))  #12'980

# The mesh vectors
propellerMesh.v0, propellerMesh.v1, propellerMesh.v2
propellerMesh.v0                   #liste de vecteur à 3 dimensions
#print(len(propellerMesh.v0))      #12980


# Accessing individual points (concatenation of v0, v1 and v2 in triplets)
#First point
propellerMesh.points[0][0:3] == propellerMesh.v0[0]
propellerMesh.points[0][3:6] == propellerMesh.v1[0]
propellerMesh.points[0][6:9] == propellerMesh.v2[0]

#Second point
propellerMesh.points[1][0:3] == propellerMesh.v0[1]
propellerMesh.points[1][3:6] == propellerMesh.v1[1]
propellerMesh.points[1][6:9] == propellerMesh.v2[1]