# PropellerProject

The user only has to interact with the file propeller_information.py. 

The file propeller_information imports its functions from:
- preprocessing.py to preprocess the aerofoil, 
- aerofoil_shape.py to compute the points on each aerofoil, 
- parameters.py to compute the propeller parameters, 
- final_aerofoil_plot.py to plot the aerofoil with their blade twist and chord length values, 
- aerodynamic_parameters.py to compute the Reynolds and Mach numbers, 
- xfoil_output.py to output the .txt file in the right shape for the X-foil software

INPUTS -- when launched, the algorithm asks the following inputs

- 'Enter your stl file name (without .stl): '
The user should give as input the name of the stl file (ex: propeller)
This file should be in the same folder as propeller_information.py.

- 'Enter your positions (in percentage from hub to tip) '
The user should give as input the positions of the aerofoil in percentage from hub to tip (ex: 40 50 for 40 r/R and 50 r/R)

- 'Aerodynamic parameters ?  (1: yes, 0: No)'
The user should enter 1 if he/she wants to output the Reynolds and Mach numbers in a .txt file. 
And enter 0 otherwise.

- 'Enter rpm of propeller (integer): '
If the user wants to output the Reynolds and Mach numbers, then he/she should also enter the rpm considered.

- 'Plots ? (1: yes, 0: No)'
The user should enter 1 if he/she wants to see the plots with the aerofoils and parameters. 
And enter 0 otherwise.


OUTPUTS -- depending on the inputs, the algorithm returns in the 'output' folder

- aerofoil_XX_.txt   (with XX being the position r/R)
For each position of aerofoil given, the algorithm outputs the aerofoil points in the right order for xfoil.

- blade_parameters.csv
The parameters of the blade: hub radius, tip radius, chord length and blade twist for each positions

- aerodynamic_parameters.csv
Reynolds and Mach numbers for each position depending on the given rpm speed

- plot_XX_.png  (with XX being the position r/R)
The plots with the aerofoil points, blade twist and chord length for each positions