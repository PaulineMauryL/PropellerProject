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



def points_of_plane(propeller_coords, plane, delta, threshold):
    ''' Get the points to consider for projection on ONE plane
        INPUT: Dataframe points of blade, 
                np.array plane equation, 
                scalar delta
        OUTPUT: Datafreme points to consider
    '''
    index_segment = []
    index_segment_up = []
    index_segment_dn = []

    threshold = 20
    points_taken = 0

    ## Upper side
    old_plane = plane[:]
    new_plane = plane[:] + [0,0,0,delta]

    while(points_taken < threshold):   # while less than threshold nb of pts are added at each iteration, continue to add points
        #nb_pts_at_a_time = 0

        for index, point in propeller_coords.iterrows(): 
            point_mult = np.append(point, 1)                                #[x, y, z] to [x, y, z, 1]: to multiply with plane [a, b, c, d]

            if(point_mult @ old_plane < 0 and point_mult @ new_plane >= 0): #if point between in interval delta between planes
                points_taken += 1
                #print("upper" + index)
                index_segment.append(index)                                 #take index of point
                index_segment_up.append(index)  #DEBUG

        old_plane = new_plane[:]
        new_plane = new_plane[:] + [0,0,0,delta]                            #consider next interval at next iteration

    '''
    for index, point in propeller_coords.iterrows(): #take a last one in case last iteration was in between a row of pts
        point_mult = np.append(point, 1)
        if(point_mult @ old_plane < 0 and point_mult @ new_plane >= 0):
            index_segment.append(index)
            index_segment_up.append(index) #DEBUG
    '''



    ## Lower side
    old_plane = plane[:]
    new_plane = plane[:] - [0,0,0,delta]
    points_taken = 0
    while(points_taken < threshold):   # while less than threshold nb of pts are added at each iteration, continue to add points
        #nb_pts_at_a_time = 0

        for index, point in propeller_coords.iterrows(): 
            point_mult = np.append(point, 1)                                #[x, y, z] to [x, y, z, 1]: to multiply with plane [a, b, c, d]

            if(point_mult @ old_plane > 0 and point_mult @ new_plane <= 0): #if point between in interval delta between planes
                points_taken += 1
                #print("lower" + index)
                index_segment.append(index)                                 #take index of point
                index_segment_dn.append(index) #DEBUG

        old_plane = new_plane[:]
        new_plane = new_plane[:] - [0,0,0,delta]                            #consider next interval at next iteration

    '''
    for index, point in propeller_coords.iterrows(): #take a last one in case last iteration was in between a row of pts
        point_mult = np.append(point, 1)
        if(point_mult @ old_plane > 0 and point_mult @ new_plane <= 0):
            index_segment.append(index)
            index_segment_dn.append(index) #DEBUG
    '''


    # Takes both sides points
    plane_points = propeller_coords.loc[index_segment].copy()

    #DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG
    #plane_points_up = propeller_coords.loc[index_segment_up].copy()
    #plane_points_dn = propeller_coords.loc[index_segment_dn].copy()
    #plot_projection_up_down(plane_points_up, plane_points_dn)
    #DEBUG#DEBUG#DEBUG#DEBUG#DEBUG#DEBUG

    return plane_points.reset_index(drop=True)


def add_border_points(right_points, one_plane_point):
    '''Add the border points to the list of points to interpolate 
    Goal: be more sure that each projection will start and end at same position
    INPUT: Dataframe points to project
            np.array coordinates of border points
    OUTPUT: DataFrame of ordered point to interpolate. (ordered important for plot)
    '''
    side1_border, side2_border, _, _, _ = extreme_points(one_plane_point)

    right_points = right_points.append(pd.DataFrame(side1_border.reshape(1, 3), columns = ["X","Y","Z"]))
    right_points = right_points.append(pd.DataFrame(side2_border.reshape(1, 3), columns = ["X","Y","Z"]))

    return right_points.sort_values('X').reset_index(drop=True)

def get_segments(blade, planes, nb_seg):

    segments = {}
    segments["points"] = []

    for i in range(nb_seg):
        index_segment = []

        for index, point in blade.iterrows():
            point_mult = np.append(point, 1)
            if(point_mult @ planes[i] > 0 and point_mult @ planes[i+1] <= 0):
                index_segment.append(index)

        segments["points"].append(blade.loc[index_segment].copy().as_matrix())

    for index, point in blade.iterrows():
        point_mult = np.append(point, 1)
        if(point_mult @ planes[nb_seg] > 0):
            index_segment.append(index) 
    segments["points"].append(blade.loc[index_segment].copy().as_matrix())

    return segments