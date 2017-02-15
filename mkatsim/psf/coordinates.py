"""Utility module for various antenna coordinates"""

from __future__ import print_function

import astropy
from astropy import units as u
from astropy.coordinates import Longitude, Latitude, EarthLocation

#Read ENU file assuming layout:
#E N U dish_diam station mount
def enu_read(
            ant_pos_file, # ENU file
            ref_location, # Array location: (LAT,LON,ALT)
           ):
    [x,y,z] = ref_location.to_geocentric()

    fin = open(ant_pos_file,'r')
    # ignore header line
    fin.readline()
    data = fin.readlines()
    fin.close()

    array = {}
    ant_list=[]
    for idx, line in enumerate(data):
        [delta_North, delta_East, delta_Up, Diameter, name, mount] = line.strip().split()
        # Antenna location
        if array.has_key(name): raise RuntimeError('Duplicate antenna name: Exiting')
        ant_location = EarthLocation((x.value+float(delta_North))*u.m, (y.value+float(delta_East))*u.m, (z.value+float(delta_Up))*u.m)
        array[name] = ant_location

        # Antenna list
        ant_parms={}
        ant_parms['POSITION'] = [ant_location.x.value, ant_location.y.value, ant_location.z.value]
        ant_parms['NAME'] = name
        ant_parms['DISH_DIAMETER']=float(Diameter)
        ant_list.append(ant_parms)

    return [array, ant_list]

# -fin-
