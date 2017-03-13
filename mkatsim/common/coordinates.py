"""Utility module for various antenna coordinates"""

from __future__ import print_function

from astropy import units as u
from astropy.coordinates import Longitude, Latitude, EarthLocation


#Read antenna position file
def read(
        ant_pos_file,  # Antenna coord file
        ref_location,  # Array location: (LAT,LON,ALT)
        enu=False,     # Coord file has ENU coords
        ):
    [x, y, z] = ref_location.to_geocentric()

    fin = open(ant_pos_file, 'r')
    # ignore header line
    fin.readline()
    data = fin.readlines()
    fin.close()

    array = {}
    ant_list = []
    for idx, line in enumerate(data):
        if enu:
            # ENU file
            # E N U dish_diam station mount
            [delta_North, delta_East, delta_Up, diameter, name, mount] = line.strip().split()
            # Antenna location
            if name in array:  # .has_key(name):
                raise RuntimeError('Duplicate antenna name: Exiting %s' % name)
            ant_location = EarthLocation((x.value+float(delta_North))*u.m, (y.value+float(delta_East))*u.m, (z.value+float(delta_Up))*u.m)
        else:
            # default assume ITRF coords
            # X Y Z diameter station mount
            [x, y, z, diameter, name, mount] = line.strip().split()
            # Antenna location
            if name in array:  # .has_key(name):
                raise RuntimeError('Duplicate antenna name: Exiting %s' % name)
            ant_location = EarthLocation((float(x))*u.m, (float(y))*u.m, (float(z))*u.m)
        array[name] = ant_location

        # Antenna list
        ant_parms = {}
        ant_parms['POSITION'] = [ant_location.x.value, ant_location.y.value, ant_location.z.value]
        ant_parms['NAME'] = name
        ant_parms['DISH_DIAMETER'] = float(diameter)
        ant_list.append(ant_parms)

    return [array, ant_list]


# Telescope reference position
def location(lat, lon, alt):

    # Reference location
    lon = Longitude(lon.strip(), u.degree, wrap_angle=180*u.degree, copy=False)  # noqa
    lat = Latitude(lat.strip(), u.degree, copy=False)
    height = u.Quantity(float(alt.strip()), u.m, copy=False)
    ref_location = EarthLocation(lat=lat.to(u.deg).value, lon=lon.to(u.deg).value, height=height.to(u.m).value)  # noqa

    return ref_location

# -fin-
