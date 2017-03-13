"""MeerKAT subarray simulators for selected antenna layouts"""

from __future__ import print_function

import matplotlib.pyplot as plt

from ..common import coordinates

def main(opts, args):
    # Reference location
    ref_location = coordinates.location(opts.lat, opts.lon, opts.alt)
    # Array location
    [array_geocentric, ant_list] = coordinates.read(args[0], ref_location, enu=opts.enu)  # noqa

## Display array antenna locations on EARTH grid using astropy coordinates
    if opts.genmap:
        from telescopearray import generate_map
        generate_map(ref_location, array_geocentric, opts.array, savegraph=opts.savegraph)  # noqa
    if opts.arr_layout:
        from telescopearray import show_layout
        show_layout(array_geocentric, subname=opts.array, savegraph=opts.savegraph)  # noqa

## Options for selecting antennas into subarrays
    from mkat_config import Subarrays
    from telescopearray import show_subarray
    mkat = Subarrays(ref_location, array_geocentric, ant_list)

    if opts.subarray is not None:
        if opts.subarray == '?':
            mkat.list_subs()
        else:
            subarray_geocentric = mkat.get_sub(opts.subarray)
            show_subarray(ref_location, array_geocentric, subarray_geocentric, subname=opts.subarray, savegraph=opts.savegraph)  # noqa

    if opts.antenna_list is not None:
        subarray_geocentric = mkat.def_sub(opts.antenna_list.split(','))
        show_subarray(ref_location, array_geocentric, subarray_geocentric, subname='custom', radii=False, savegraph=opts.savegraph)  # noqa

        if opts.savesubarray:
            from telescopearray import save_array
            save_array(subarray_geocentric)

    if not opts.savegraph:
        opts.verbose = True
    if opts.verbose:
        try:
            plt.show()
        except:
            pass  # nothing to show

# -fin-
