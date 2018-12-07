
coord = importdata('xfoil40.txt');
alpha = 10;
Re = 1e6;
Mach = 0.2;
[pol,foil] = xfoil(coord,alpha,Re,Mach);

