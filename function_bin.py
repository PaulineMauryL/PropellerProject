#file to store old function than might be useful in future


def all_border(up_side1_border, up_side2_border, dn_side1_border, dn_side2_border):
    borders_tb = np.zeros([4,3])
    
    borders_tb[0][:] = up_side1_border
    borders_tb[1][:] = up_side2_border
    borders_tb[2][:] = dn_side1_border
    borders_tb[3][:] = dn_side2_border
    
    xmin = min(borders_tb[:,0])
    xmax = max(borders_tb[:,0])
    ymin = min(borders_tb[:,1])
    ymax = max(borders_tb[:,1])
    
    return xmin, xmax, ymin, ymax



def get_all_points_for_projections(planes, segments, nb_seg, resolution):
    '''Get the points next to each planes on both sides'''
    up = []
    down = []
    labels = ['X', 'Y', 'Z']


    for proj in range(1, nb_seg):
        up_i, down_i = get_points_to_project_on_plane(planes[proj], segments['points'][proj-1], segments['points'][proj], resolution)
        up.append(pd.DataFrame(up_i, columns = labels))
        down.append(pd.DataFrame(down_i, columns = labels))

    return up, down


def get_points_to_project_on_plane(plane, segment_down, segment_up, resolution):
    '''Get points in a range 'resolution' around the plan'''
        #print(segment_down.shape)
    upper_plane = plane[:] + [0,0,0,resolution]
    lower_plane = plane[:] - [0,0,0,resolution]
    
    idx_up = []
    for index, point in enumerate(segment_up):
        point_mult = np.append(point, 1)
        if(point_mult @ lower_plane < 0 and point_mult @ plane >= 0):
            idx_up.append(index)
            #print("here")
    idx_down = []
    for index, point in enumerate(segment_down):
        point_mult = np.append(point, 1)
        if(point_mult @ plane < 0 and point_mult @ upper_plane >= 0):
            idx_down.append(index)
            #print("here")

    up = segment_up[idx_up]
    down = segment_down[idx_down]

    return up, down



def project_points_on_plane(up_right_pts, dn_right_pts, up_left_pts, dn_left_pts, plan1):
    proj_right = []
    proj_left = []
    labels = ['X', 'Y', 'Z']
    
    for i, _ in up_right_pts.iterrows():
        #print(up_right_pts.iloc[i])
        proj_right.append(point_on_plane(up_right_pts.iloc[i], dn_right_pts.iloc[i], plan1))
        proj_left.append( point_on_plane(up_left_pts.iloc[i],  dn_left_pts.iloc[i],  plan1))
        
    proj_right_df = pd.DataFrame(proj_right, columns = labels)
    proj_left_df  = pd.DataFrame(proj_left,  columns = labels)
    
    return proj_right_df, proj_left_df