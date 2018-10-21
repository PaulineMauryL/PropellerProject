import pandas as pd
import numpy as np
from myMathFunction import distance_point_plane, project_point, distance_p2p, point_on_plane


#Plane i is associated with segments i-1 and i
def all_projections(nb_seg, planes, segments, nb_point):
    proj_down = {}
    proj_up = {}

    for proj in range(1, nb_seg):
        df_d, df_u = project_on_plane(planes[proj], segments['points'][proj-1], segments['points'][proj], nb_point)
        proj_down[proj-1] = df_d
        proj_up[proj-1] = df_u
    
    return proj_up, proj_down


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
        
    df_d = pd.DataFrame(pp_d)
    df_d.columns = ['X', 'Y','Z']
    df_u = pd.DataFrame(pp_u)
    df_u.columns = ['X', 'Y','Z']
    
    return df_d, df_u

def find_closest_couple_plane(proj_down, proj_up):
    couple = []
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
            couple.append((i,value))
            
    return couple

def couple_all_planes(proj_down, proj_up, nb_seg):
    #print("couple all plane \n \n \n")
    couples = []
    for proj in range(nb_seg-1):
        couples.append( find_closest_couple_plane(proj_down[proj], proj_up[proj]) )
    return couples



def project_couple(couple, plane, proj_up_i, proj_down_i): 
    projection = []
    for i, pair in enumerate(couple):
        projection.append( point_on_plane( proj_up_i.loc[pair[0], :], proj_down_i.loc[pair[1], :], plane ) )
        
    return projection


def project_all_couples(couples, planes, proj_up, proj_down):
    plan_df = {}
    projections = []
    
    for i, couple in enumerate(couples):
        projections.append( project_couple(couple, planes[i+1], proj_up[i], proj_down[i]) )
        
    for i, plan in enumerate(projections):
        plan_df[i] = pd.DataFrame(plan, index = False)
        
    return plan_df
