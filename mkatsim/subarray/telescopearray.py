#! /usr/bin/python
## Display array antenna locations on EARTH grid using astropy coordinates

import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Copied library functions
def shoot(lon, lat, azimuth, maxdist=None):
    """Shooter Function
    Original javascript on http://williams.best.vwh.net/gccalc.htm
    Translated to python by Thomas Lecocq
    """
    import numpy as np
    glat1 = lat * np.pi / 180.
    glon1 = lon * np.pi / 180.
    s = maxdist / 1.852
    faz = azimuth * np.pi / 180.

    EPS= 0.00000000005
    if ((np.abs(np.cos(glat1))<EPS) and not (np.abs(np.sin(faz))<EPS)):
        alert("Only N-S courses are meaningful, starting at a pole!")

    a=6378.13/1.852
    f=1/298.257223563
    r = 1 - f
    tu = r * np.tan(glat1)
    sf = np.sin(faz)
    cf = np.cos(faz)
    if (cf==0):
        b=0.
    else:
        b=2.  * np.arctan2(tu, cf)

    cu = 1.  / np.sqrt(1 + tu * tu)
    su = tu * cu
    sa = cu * sf
    c2a = 1 - sa * sa
    x = 1.  + np.sqrt(1.  + c2a * (1.  / (r * r) - 1.))
    x = (x - 2.) / x
    c = 1.  - x
    c = (x * x / 4.  + 1.) / c
    d = (0.375 * x * x - 1.) * x
    tu = s / (r * a * c)
    y = tu
    c = y + 1
    while (np.abs (y - c) > EPS):

        sy = np.sin(y)
        cy = np.cos(y)
        cz = np.cos(b + y)
        e = 2.  * cz * cz - 1.
        c = y
        x = e * cy
        y = e + e - 1.
        y = (((sy * sy * 4.  - 3.) * y * cz * d / 6.  + x) * d / 4.  - cz) * sy * d + tu

    b = cu * cy * cf - su * sy
    c = r * np.sqrt(sa * sa + b * b)
    d = su * cy + cu * sy * cf
    glat2 = (np.arctan2(d, c) + np.pi) % (2*np.pi) - np.pi
    c = cu * cy - su * sy * cf
    x = np.arctan2(sy * sf, c)
    c = ((-3.  * c2a + 4.) * f + 4.) * c2a * f / 16.
    d = ((e * cy * c + cz) * sy * c + y) * sa
    glon2 = ((glon1 + x - (1.  - c) * d * f + np.pi) % (2*np.pi)) - np.pi

    baz = (np.arctan2(sa, b) + np.pi) % (2 * np.pi)

    glon2 *= 180./np.pi
    glat2 *= 180./np.pi
    baz *= 180./np.pi

    return (glon2, glat2, baz)

def equi(m, centerlon, centerlat, radius, *args, **kwargs):
    glon1 = centerlon
    glat1 = centerlat
    X = []
    Y = []
    for azimuth in range(0, 360):
        glon2, glat2, baz = shoot(glon1, glat1, azimuth, radius)
        X.append(glon2)
        Y.append(glat2)
    X.append(X[0])
    Y.append(Y[0])

    #~ m.plot(X,Y,**kwargs)
    #Should work, but doesn't...
    X,Y = m(X,Y)
    plt.plot(X,Y,**kwargs)

# Show simple layout for quick look
def show_layout(
                array,              # antenna location array
                subname='MeerKAT',  # name of telescope array
                savegraph=False,    # output to PNG image
               ):
    [arr_names, arr_lat, arr_lon] = build_array(array)
    plt.figure(facecolor='white')
    ax1 = plt.axes(frameon=False)
    plt.plot(arr_lon, arr_lat, 'ro', alpha=0.3)
    ax1.axes.get_yaxis().set_visible(False)
    ax1.axes.get_xaxis().set_visible(False)
    plt.title(str(subname))
    if savegraph:
        plt.savefig('%s_SimpleArray.png' % subname, dpi=300)

# Show overlap of subarray on MeerKAT array layout
def show_subarray(
                  array_ref,       # array reference location
                  array,           # MeerKAT full array layout
                  subarray,        # Subarray to display
                  subname=None,    # Name of subarray to display
                  savegraph=False,
                  radii=True,
                 ):
# def mkat_subarr(mkat, subarray=None, antennalist=[], savegraph=False):
    [arr_names, arr_lat, arr_lon] = build_array(array)
    [subarr_names, subarr_lat, subarr_lon] = build_array(subarray)

    # Earth projection
    m = Basemap(projection='merc',
                lat_0=array_ref.latitude.value,
                lon_0=array_ref.longitude.value,
                llcrnrlon=numpy.min(arr_lon)-0.005,
                llcrnrlat=numpy.min(arr_lat)-0.005,
                urcrnrlon=numpy.max(arr_lon)+0.005,
                urcrnrlat=numpy.max(arr_lat)+0.005)
    # set regular grid and map projected coordinates
    arr_x, arr_y = m(arr_lon, arr_lat)
    subarr_x, subarr_y = m(subarr_lon, subarr_lat)
    # # Array layout
    plt.figure(figsize=(20, 13))
    # draw parallels.
    parallels = numpy.arange(-30.73, -30.69, .01)
    m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
    # draw meridians
    meridians = numpy.arange(21.41, 21.48, .01)
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)
    m.drawmapboundary(fill_color='white')
    m.scatter(arr_x, arr_y, 5, marker='o', color='c', label='MeerKAT antennas')
    m.scatter(subarr_x, subarr_y, 10, marker='o', color='k', label='SubArray')
    if radii:
        equi(m, array_ref.longitude.value, array_ref.latitude.value, radius=0.5,lw=1., linestyle='--', label='0.5 deg')
        equi(m, array_ref.longitude.value, array_ref.latitude.value, radius=1,lw=1., linestyle='--', label='1 deg')
        equi(m, array_ref.longitude.value, array_ref.latitude.value, radius=2,lw=1., linestyle='--', label='2 deg')
        equi(m, array_ref.longitude.value, array_ref.latitude.value, radius=3,lw=1., linestyle='--', label='3 deg')
    cntr = 0
    for x, y in zip(subarr_x, subarr_y):
        plt.text(x, y, subarray.keys()[cntr], fontsize=6, ha='center', va='baseline', color='k')  # noqa
        cntr += 1
    plt.title('SubArray %s' % subname)
    plt.legend(loc=0, numpoints=1)
    if savegraph:
        if subname is None:
            plt.savefig('SubArrayLayout.png')
        else:
            plt.savefig('Sub%sLayout.png' % subname)

# Generate layout map using Mercator projection
def generate_map(
                ref_location,       # array geodetic (LAT,LON) reference
                array,              # antenna location array
                subname='MeerKAT',  # name of telescope array
                savegraph=False,    # output to PNG image
               ):
    [arr_names, arr_lat, arr_lon] = build_array(array)
    # Earth projection
    m = Basemap(projection='merc',
                lat_0=ref_location.latitude.value,
                lon_0=ref_location.longitude.value,
                llcrnrlon=numpy.min(arr_lon)-0.005,
                llcrnrlat=numpy.min(arr_lat)-0.005,
                urcrnrlon=numpy.max(arr_lon)+0.005,
                urcrnrlat=numpy.max(arr_lat)+0.005)
    # set regular grid and map projected coordinates
    ref_x, ref_y = m(ref_location.longitude.value, ref_location.latitude.value)
    arr_x, arr_y = m(arr_lon, arr_lat)
    # Array layout
    plt.figure(figsize=(20, 13), facecolor='white')
    # draw parallels.
    parallels = numpy.arange(-30.73, -30.69, .01)
    m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
    # draw meridians
    meridians = numpy.arange(21.41, 21.48, .01)
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)
    m.drawmapboundary(fill_color='white')
    m.scatter(ref_x, ref_y, 1000, marker='+', color='r', label='Array reference')  # noqa
    cntr = 0
    for x, y in zip(arr_x, arr_y):
        plt.text(x, y, arr_names[cntr], fontsize=6, ha='center', va='baseline', color='k')  # noqa
        cntr += 1
    plt.title('Detail Map: %s Layout' % subname)
    plt.legend(loc=0, numpoints=1, ncol=1, prop={'size': 10}, scatterpoints=1)
    if savegraph:
        plt.savefig('%s_ArrayLayout.png' % subname, dpi=300)

# Utility script to extract antenna (LAT,LON) positions for plotting
def build_array(
                array_antennas,  # ENU coordinates from astropy
               ):
    # Get array
    arr_latitude = []
    arr_longitude = []
    arr_names = []
    for antenna in array_antennas:
        arr_names.append(antenna)
        arr_latitude.append(array_antennas[antenna].latitude.value)
        arr_longitude.append(array_antennas[antenna].longitude.value)
    return [arr_names, arr_latitude, arr_longitude]

# Save subarray in ITRF geo-centric coordinate file
def save_array(
               subarray,  # Geo-centric coordinates of subarray
              ):
    out_str = 'X Y Z diameter station mount\n'
    for ant in subarray.keys():
        itrf = subarray[ant]
        out_str += ('%f %f %f 13.5 %s ALT-AZ\n' %
                   (itrf.x.value, itrf.y.value, itrf.z.value, ant))

    fout = open('subarray.itrf', 'w')
    fout.write(out_str)
    fout.close()

# -fin-
