import pandas as pd
import numpy as np

from stl import mesh
from preprocessing import *
from aerofoil_shape import *
from parameters import *
from final_aerofoil_plot import *
from aerodynamic_parameters import *
from xfoil_output import *

#####################################################################################################
##########################              USER INPUT              #####################################
#####################################################################################################
stl_file = input('Enter your stl file name (without .stl): ')
propellerMesh = mesh.Mesh.from_file(stl_file + '.stl')

positions_name = input('Enter your positions (in percentage from hub to tip) ')                       #positions in percentage
positions = list(map(int, positions_name.split()))                      

aerodynamic_bool = input('Aerodynamic parameters ?  (1: yes, 0: No)')                                 #Compute Mach and Reynolds ?
if(aerodynamic_bool):
	rpm_name = input('Enter rpm of propeller (integer): ')                                                #propeller rpm (for Reynold and Mach numbers)
	rpm = int(rpm_name)

plots_bool = input('Plots ? (1: yes, 0: No)')                                                         #print plots

#####################################################################################################
##########################            PRE-PROCESSING            #####################################
#####################################################################################################
propeller = stl_to_csv(propellerMesh) 
propeller_coords, vect_length, vect_out, vect_side = prepare_propeller(propeller)                      #principal directions and alignment
dmiddle, dlowest, dhighest   = d_blade(vect_length, propeller_coords)                                  #d of plan ax+by+cx+d = 0
upper_blade, lower_blade     = blade_alone(propeller_coords, vect_length, dmiddle)                     #points of each blades


#####################################################################################################
##########################            AEROFOIL SHAPE            #####################################
#####################################################################################################
planes = get_planes(upper_blade, dmiddle, dhighest, vect_length, positions)                            #get equations of planes for projection
all_plane_points = get_points(upper_blade, planes)                                                     #get points used for each projection
right_param, left_param, right_pts, left_pts = get_all_projections(planes, all_plane_points)           #get interpolation parameters
x_list, y_right_list, y_left_list, rm = get_generated_pts(right_param, left_param, right_pts, left_pts) #generate points


#####################################################################################################
##########################              PARAMETERS              #####################################
#####################################################################################################
hub_radius = param_hub_radius(propeller_coords)
tip_radius = get_tip_radius(propeller_coords)
blade_twist = get_blade_twist(x_list, y_right_list, y_left_list)
chord_length = get_chord_length(x_list, y_right_list, y_left_list)
chord_length_normalized = [x/tip_radius for x in chord_length]
hub_radius = param_hub_radius(propeller_coords)

output_param(positions, tip_radius, hub_radius, chord_length, blade_twist, 'output/blade_parameters.csv')           #output blade parameters in csv file


#####################################################################################################
##########################        FINAL AEROFOIL  PLOTS         #####################################
#####################################################################################################
if plots_bool:
	complete_plot(right_pts, left_pts, x_list, y_right_list, y_left_list, positions, chord_length, blade_twist) #plot aerofoil with parameters


#####################################################################################################
##########################        AERODYNAMIC PARAMETERS        #####################################
#####################################################################################################
if(aerodynamic_bool):
	radius  = get_radius(positions, tip_radius)
	reynold = get_reynold_numbers(radius, rpm, chord_length)
	mach    = get_mach_numbers(radius, rpm)
	df = output_reynold_mach(positions, radius, reynold, mach, "output/aerodynamic_parameters.csv")                   #output aerodynamic in csv file


#####################################################################################################
##########################            X-FOIL OUTPUT              ####################################
#####################################################################################################
x_r_rotated, y_r_rotated, x_l_rotated, y_l_rotated = align_aerofoil(x_list, y_right_list, y_left_list, blade_twist)
y_r_flipped, y_l_flipped = mirror_aerofoil(y_r_rotated, y_l_rotated)

xfoil_inputs(x_r_rotated, y_r_flipped, x_l_rotated, y_l_flipped, positions)                            #output aerofoil for each position in .txt file