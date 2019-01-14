import matplotlib.pyplot as plt
from preprocessing import extreme_points

def plot_interpolation_param(right_points, left_points, x, y_right, y_left, pos, chord_length, blade_twist, i):      

    fig = plt.figure()
    fig.add_subplot(111)

    #Plot chord length
    plt.plot([x[0], x[-1]], [y_right[0], y_right[-1]], "r-", label="Chord length", linewidth = 4);

    #Plot interpolated points
    _, highest, lowest = extreme_points(right_points)
    #x = np.linspace(lowest[0], highest[0], 100)
    plt.scatter(x, y_right, color='b', label="Interpolated points (up)")
    plt.scatter(x, y_left, color ='c', label="Interpolated points (down)")

    #Plot real points
    plt.scatter(right_points["X"], right_points["Y"], color='g', marker='^', label="Real points (up)")
    plt.scatter(left_points["X"],  left_points["Y"],  color='m', marker='^', label="Real points (down)")

    plt.xlabel('X (mm)', fontsize=15)
    plt.ylabel('Y (mm)', fontsize=15)

    cl = str(round(chord_length[i], 2))
    bt = str(round(blade_twist[i], 2))

    plt.text(-3, -4, "Chord length " + cl + "mm", {'color': 'r', 'fontsize': 13})
    plt.text(-3, -5, "Blade twist " + bt + "deg", {'color': 'k', 'fontsize': 13})

    plt.legend()
    plt.title("Aerofoil at " + pos + "% r/R", fontsize = 30)
    plt.axis([-25, 15, -6, 6])
    plt.show()
    fig.savefig('output/plot_' + pos + '_.png')



def complete_plot(right_pts, left_pts, x_list, y_right_list, y_left_list, positions, chord_length, blade_twist):   
    for i in range(len(x_list)):
        plot_interpolation_param(right_pts[i], left_pts[i], x_list[i], y_right_list[i], y_left_list[i], str(positions[i]), chord_length, blade_twist, i)