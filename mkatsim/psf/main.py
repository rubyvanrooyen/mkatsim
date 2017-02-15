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


def main(opts, args):
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
