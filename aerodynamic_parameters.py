import numpy as np
import pandas as pd
import math

def reynold_number(radius, rpm, chord_length):
    kinematic_viscosity = 14.88 * math.pow(10,-6) #[m^2/s]  https://www.engineeringtoolbox.com/air-absolute-kinematic-viscosity-d_601.html at 18°
    kinematic_viscosity = kinematic_viscosity*60*math.pow(10,6)   # *60 -> [m^2/min]  *10^6 -> [mm^2/min]
    u = radius * rpm  #[mm] * [/min] 
    reynold = (u * chord_length)/kinematic_viscosity    # [mm/min] * [mm] / [mm^2/min] -> [X]
    return reynold

def get_reynold_numbers(radius, rpm, chord_length):
    reynold = []
    for rad, cl in zip(radius, chord_length):
        reynold.append( reynold_number(rad, rpm, cl) )
    return reynold

def mach_number(radius, rpm):  
    c =  20580000 #v_sound = 343[m/s] = 343*60[m/min] = 343*60*1000 [mm/min]
    u = radius * rpm  #[mm] * [/min] 
    mach = u/c     # [min/mmm] / [mm/min] -> [X]
    return mach

def get_mach_numbers(radius, rpm):
    mach = []
    for rad in radius:
        mach.append( mach_number(rad, rpm) )
    return mach

def output_reynold_mach(positions, radius, reynold, mach, filename):
    df = pd.DataFrame({'Percentage': positions, 'Radius': radius,  'Reynold': reynold, 'Mach':mach})
    df.to_csv(filename)
    return df

