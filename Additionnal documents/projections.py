import pandas as pd
import numpy as np
from myMathFunction import distance_point_plane, project_point, distance_p2p, point_on_plane


#Plane i is associated with segments i-1 and i
def projections_by_side(nb_seg, planes, segments, nb_point):
    proj_down = []
    proj_up = []
    
    points_up = []
    points_down = []

    for proj in range(1, nb_seg): #1,2,3,4
        df_d, df_u, point_down, point_up = project_on_plane(planes[proj], segments['points'][proj-1], segments['points'][proj], nb_point)
        #print(proj)
        proj_down.append(df_d)
        proj_up.append(df_u)
        
        points_down.append(point_down) #0,1,2,3
        points_up.append(point_up)
        
    return proj_up, proj_down, points_down, points_up


def project_on_plane(plan, segment_down, segment_up, nb_point):
    distance_down = []
    distance_up = []
    
    # Get the distance of the upper and lower point to the plan
    for point in segment_down:
        distance_down.append(distance_point_plane(point, plan)) 
    for point in segment_up:
        distance_up.append(distance_point_plane(point, plan)) 
    
    # Get the 100 point closest to plane on each side
    sort_idx_down = np.argsort(distance_down)
    sort_idx_up   = np.argsort(distance_up)
    
    sort_idx_down = sort_idx_down[:nb_point]
    sort_idx_up   = sort_idx_up[:nb_point]
    
    point_down = segment_down[sort_idx_down]
    point_up   = segment_up[sort_idx_up]
    
    # Project point on plan
    pp_d = []
    pp_u = []
    for p in point_down:
        pp_d.append(project_point(p, plan))
    for p in point_up:
        pp_u.append(project_point(p, plan))
    
    labels = ['X', 'Y', 'Z']

    df_d = pd.DataFrame(pp_d, columns = labels)
    df_u = pd.DataFrame(pp_u, columns = labels)
    
    return df_d, df_u, point_down, point_up



def find_closest_couple_plane(proj_down, proj_up):
    down = []
    up = []
    
    d = np.zeros([proj_down.shape[0],proj_up.shape[0]])
    #print("find_closest_couple_plane")
    for i, x1 in proj_down.iterrows():
        for j, x2 in proj_up.iterrows():
            d[i][j] = distance_p2p(x1, x2)
    
    min_down = np.argmin(d, axis=0)
    min_up = np.argmin(d, axis=1)

    for i in range(len(proj_down)):
        value = min_down[i]
        #print("i is {}".format(i))
        #print("value is {}".format(value))
        if(min_up[value]==i):
            #print("min_up[value] is {}".format(min_up[value]))
            #couple.append((i,value))
            down.append(proj_down.iloc[i])
            #down.append(proj_down.iloc[value])
            up.append(proj_up.iloc[value])
            #up.append(proj_up.iloc[i])   
    return down, up



def couple_all_planes(proj_down, proj_up, nb_seg):
    #print("couple all plane \n \n \n")
    #couples = []
    down = []
    up = []
    
    for proj in range(nb_seg-1):
        #print(proj)
        down_proj, up_proj = find_closest_couple_plane(proj_down[proj], proj_up[proj])
        
        #couples.append(couple)
        down.append(down_proj)
        up.append(up_proj)
        
    return down, up


def project_couple(plane, up, down): 
    projection = []
    for i in range(len(up)):
        projection.append( point_on_plane(up[i], down[i], plane) )
        
    return projection


def project_all_couples(planes, up, down):
    
    projections = []
    for i in range(len(up)):
        projections.append( project_couple(planes[i+1], up[i], down[i]) )

    print(len(projections))

    projections_df = []
    labels = ['X', 'Y', 'Z']
    for i, pt in enumerate(projections):
        print(i)
        projections_df.append( pd.DataFrame(pt, columns = labels) )
        
    return projections_df



def points_to_project(segments, idx_up, idx_down, couples, nb_seg):
    up_keep = []
    down_keep = []
    
    for i in range(nb_seg-1):
        up_keep.append( [segments['points'][i+1][j] for j in idx_up[i]] )
        down_keep.append( [segments['points'][i][j] for j in idx_down[i]] )
    
    up = []
    down = []
    
    for i, couple in enumerate(couples):
        up_points = [] 
        down_points = [] 
    
        for j, tup in enumerate(couple):  
            down_points.append(down_keep[i][tup[0]])        
            up_points.append(up_keep[i][tup[1]])
        
        up.append(up_points)
        down.append(down_points)
        
    return down, up
