#! /usr/bin/python
## Simulate PSF, Image and Dirty Image

from __future__ import print_function
from datetime import datetime, timedelta

import glob
import matplotlib.pyplot as plt
import numpy
import os
import shutil
import subprocess
import tempfile

import astropy
from astropy import units as u
from astropy.coordinates import Longitude, Latitude, EarthLocation

import casacore.tables

from fits2png import fits2png
from makems import ms_make
import coordinates
import slicepsf

if __name__ == '__main__':
    from optparse import OptionParser, OptionGroup
    usage='%prog [options] --cfg <makems.cfg> <ant_pos_file>'
    parser = OptionParser(usage=usage, version="%prog 1.0")
    group = OptionGroup(parser, 'Antenna Array')
    group.add_option('--array',
                      action='store',
                      dest='array',
                      type=str,
                      default='mkat',
                      help='Name of telescope / array')
    group.add_option('--lat',
                      action='store',
                      dest='lat',
                      type=str,
                      default='-30:42:47.4',
                      help='Array location , latitude')
    group.add_option('--lon',
                      action='store',
                      dest='lon',
                      type=str,
                      default='21:26:38.0',
                      help='Array location , longitude')
    group.add_option('--alt',
                      action='store',
                      dest='alt',
                      type=str,
                      default='1060.0',
                      help='Array location , altitude')
    parser.add_option_group(group)
    group = OptionGroup(parser, 'Configuration Files')
    group.add_option('--cfg',
                      action='store',
                      dest='cfg',
                      type=str,
                      default=None,
                      help='Config file for makems')
    parser.add_option_group(group)
    group = OptionGroup(parser, 'Coordinate Classification')
    group.add_option("--enu",
                      dest='enu',
                      action="store_true",
                      default=False,
                      help="Antenna position file giving ENU coordinates")
    parser.add_option_group(group)
    group = OptionGroup(parser, 'Simulation Options')
    group.add_option('--ant',
                      action='store',
                      dest='tblname',
                      type=str,
                      default=None,
                      help='Antenna table name, else ANTENNA table will be generated')
    parser.add_option_group(group)
    group = OptionGroup(parser, 'Basic wsclean options')
    group.add_option('--dec',
                      action='store',
                      dest='declination',
                      type=str,
                      default='-60',
                      help='Declination for simulation. Use comma separated list for multiple declinations')
    group.add_option('--briggs_weight',
                      action='store',
                      dest='briggs_weight',
                      type=float,
                      default=-0.5,
                      help='Weight for Briggs weight during clean')
    group.add_option('--synthesis',
                      action='store',
                      dest='synthesis',
                      type=float,
                      default=0.05, # hr
                      help='Total synthesis / integration time in hours (default snapshot of 3 minutes).')
#SEPARATE UIT MAKEMS SE OPTIONS EN SIT AL DIE WSCLEAN OPTIONS IN
    group.add_option('--dt',
                      action='store',
                      dest='dt',
                      type=float,
                      default=256, # sec
                      help='Accumulation time given as nr seconds per dump')
    group.add_option('--dtime',
                      action='store',
                      dest='dtime',
                      type=float,
                      default=12, # hr
                      help='Regular separation of simulated obs.')
    group.add_option('--stime',
                      action='store',
                      dest='stime',
                      type=str,
                      default=None,
                      help='Observation start time YYYY/MM/DD/hh:mm.')
    parser.add_option_group(group)
    group = OptionGroup(parser, 'Output Options')
    group.add_option('-v', "--verbose",
                      dest='verbose',
                      action="store_true",
                      default=False,
                      help="Display results and all graphs")
    parser.add_option_group(group)
    (opts, args) = parser.parse_args()

    if len(args) < 1 and opts.tblname is None:
        print('No antenna coordinate file provided')
        parser.print_usage()
        raise SystemExit
    if opts.cfg is None:
        print('Need makems config file')
        parser.print_usage()
        raise SystemExit

    # Reference location
    lon = Longitude(opts.lon.strip(), u.degree, wrap_angle=180*u.degree, copy=False)
    lat = Latitude(opts.lat.strip(), u.degree, copy=False)
    height = u.Quantity(float(opts.alt.strip()), u.m, copy=False)
    ref_location = EarthLocation(lat=lat.to(u.deg).value, lon=lon.to(u.deg).value, height=height.to(u.m).value)
    # Array location
    if len(args) > 0:
        if opts.enu:
            [array_geocentric, ant_list] = coordinates.enu_read(args[0], ref_location)
        else:
            raise RuntimeError('Coordinate system not implemented yet')

## Create CASA ANTENNA table for antenna positions
    if opts.tblname is None:
        opts.tblname = '%s_ANTENNAS'%opts.array
        import anttbl
        try: anttbl.make_tbl(opts.tblname, ant_list)
        except: raise

## Make dummy measurement set for simulations
    nscans=int(12./opts.dtime) # number scans
    dintegration=opts.synthesis*3600/nscans # integration time per scan
    declinations_deg = opts.declination.strip().split(',')
    for opts.declination in declinations_deg:
        if opts.stime is not None:
            starttime_object = datetime.strptime(opts.stime, "%Y/%m/%d/%H:%M")
        else:
            starttime_object = datetime.now()

        mslist = []
        for scan in range(nscans):
            starttime = starttime_object + timedelta(seconds=scan*opts.dtime*3600.)
            opts.stime=starttime.strftime("%Y/%m/%d/%H:%M")
            mslist.append(ms_make(opts))

        if len(mslist) > 1:
            msname='%s_%sdeg_%.2fhr.ms_p0' % (opts.array, opts.declination, opts.synthesis)
            casacore.tables.msconcat(mslist,msname,concatTime=True)
        else: msname = mslist[0]

##Clean simulated data to get psf
        try:
            subprocess.check_call([
                'wsclean',
                '-j', '4',
                '-size', '7200', '7200',
                '-scale', '0.5asec',
                '-weight', 'briggs', str(opts.briggs_weight),
                '-make-psf',
                '-fitbeam',
                '-name', msname,
                msname,
                ])
        except subprocess.CalledProcessError as e:
            # handle or report exception here, maybe
            pass

## Convert wsclean generated fits files to PNG
    for fitsfile in glob.glob('*psf.fits'):
        fits2png(fitsfile,area=0.04,contrast=0.05,cmap='jet')
#KYK WAT HIER AANGAAN -- HOEKOM VERANDER DIT DIE FITS FILE
# ## Slice through the major axis of the PSF
#         outfile = '%s-slice.png'%os.path.splitext(os.path.basename(fitsfile))[0]
#         slicepsf.along_axes(fitsfile, output=outfile) # need to look at this script -- something in here changes the FITS file



    if opts.verbose:
        try: plt.show()
        except: pass # nothing to show

# -fin-
