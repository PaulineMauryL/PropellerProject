import pandas as pd
import numpy as np
from myMathFunction import distance_point_plane, project_point


#Plane i is associated with segments i-1 and i
def all_projections(nb_seg, planes, segments, nb_point):
    proj_down = {}
    proj_up = {}

    for proj in range(1, nb_seg):
        df_d, df_u = project_on_plane(planes[proj], segments['points'][proj-1], segments['points'][proj], nb_point)
        proj_down[proj] = df_d
        proj_up[proj] = df_u
    
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