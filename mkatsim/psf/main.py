"""Simulate PSF, Image and Dirty Image"""

from __future__ import print_function
from datetime import datetime, timedelta

import glob
import matplotlib.pyplot as plt
import os
import subprocess

import casacore.tables

from makems import ms_make
from ..common import coordinates
import plot


def main(parser, opts, args):
    # TODO:
    #   possibly be more explicit about what opts & args are accepted -- would
    #   be helpful info for when one wants to call main() from somewhere else
    # Reference location
    ref_location = coordinates.location(
                                        opts.lat,
                                        opts.lon,
                                        opts.alt,
                                       )

## Create CASA ANTENNA table for antenna positions
    if opts.tblname is None:
        # Array location
        [array_geocentric, ant_list] = coordinates.read(
                                                        args[0],
                                                        ref_location,
                                                        antennas=opts.ant_list,
                                                        enu=opts.enu,
                                                       )
        opts.tblname = '%s_ANTENNA' % opts.array
        import anttbl
        try:
            anttbl.make_tbl(opts.tblname, ant_list)
        except:
            raise

    # Only create a CASA antenna table
    if opts.ant_table:
        import sys
        sys.exit(0)

## Make dummy measurement set for simulations
    nscans = int(12./opts.dtime)  # number scans
    dintegration = opts.synthesis/nscans  # integration time per scan
    if opts.stime is not None:
        starttime_object = datetime.strptime(opts.stime, "%Y/%m/%d/%H:%M:%S")
    else:
        starttime_object = datetime.now()

    declinations_deg = opts.declination.strip().split(',')
    for opts.declination in declinations_deg:
        mslist = []
        for scan in range(nscans):
            starttime = starttime_object + timedelta(seconds=scan*opts.dtime*3600.)  # noqa
            opts.stime = starttime.strftime("%Y/%m/%d/%H:%M:%S")
            mslist.append(ms_make(opts))

        if len(mslist) > 1:
            msname = '%s_%sdeg_%.2fsec.ms_p0' % (opts.array, opts.declination, opts.synthesis)  # noqa
            casacore.tables.msconcat(mslist, msname, concatTime=True)
        else:
            msname = mslist[0]

##Clean simulated data to get psf
        cmd_array = ['wsclean',
                     '-j', '4',
                     '-size', '7200', '7200',
                     '-scale', '0.5asec',
                     '-make-psf',
                     '-fitbeam',  # determine beam shape by fitting the PSF
                     '-name', msname,
                    ]
        if opts.weight == 'briggs':
            cmd_array.extend(['-weight', opts.weight, str(opts.robust)])
        else:
            cmd_array.extend(['-weight', opts.weight])
        for arg in parser.get_option_group('--robust').option_list[:]:
            if arg.dest == 'weight' or arg.dest == 'robust':
                continue
            arg_val = getattr(opts, str(arg.dest))
            if arg_val is None:
                continue
            if str(arg_val) == 'False':
                continue
            if str(arg_val) == 'True':
                cmd_array.extend(['-%s' % ((arg.dest.replace('_', '-')))])
                continue
            cmd_array.extend(['-%s' % ((arg.dest.replace('_', '-'))), str(arg_val)])  # noqa
        cmd_array.append(msname)

        try:
            subprocess.check_call(cmd_array)
        except subprocess.CalledProcessError as e:  # noqa
            # TODO: handle or report exception here, maybe
            pass

    sliceout = None
    uvout = None
## Convert wsclean generated fits files to PNG
    # PSF files to PNG
    from fits2png import fits2png
    for fitsfile in glob.glob('*psf.fits'):
        fits2png(fitsfile, area=0.04, contrast=0.05, cmap='jet')
## Slice through the major axis of the PSF
        sliceout = '%s-slice.png' % os.path.splitext(os.path.basename(fitsfile))[0]  # noqa
        plot.slicepsf(fitsfile, beamwidth=opts.beamwidth, crop=opts.crop, output=sliceout)  # noqa
## UV coverage of measurement set
        uvout = '%s-uv.png' % os.path.splitext(os.path.basename(msname))[0]
        plot.uv(msname, output=uvout)
    # # All fits files to PNG
    # if opts.allfits:
    #     for fitsfile in glob.glob('*.fits'):
    #         try:
    #             fits2png(fitsfile, area=0.04, contrast=0.05, cmap='jet')
    #         except:
    #             pass  # do not care

    if opts.verbose:
        try:
            plt.show()
        except:
            pass  # nothing to show

# -fin-
