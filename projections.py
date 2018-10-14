import pandas as pd
import numpy as np
from myMathFunction import distance_point_plane, project_point

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