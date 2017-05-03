#flake8: noqa
# rename this file to common/option.py

from optparse import OptionParser, OptionGroup

from .. import _version


# def cli(parser):
def parser(usage='%prog [options]'):
    """Collection of common options."""

    parser_ = OptionParser(
        usage=usage,
        version="%prog {}".format(_version.__version__),
        )
    # increase space reserved for option flags (default 24), trick to make the help more readable
    parser_.formatter.max_help_position = 100
    # increase help width from 120 to 200
    parser_.formatter.width = 120

    # positional options
    group = OptionGroup(parser_, 'Telescope Geographic Coordinates')
    ### XXX: shouldn't the next line be group.add_option()?
    group.add_option('--array',
                     action='store',
                     dest='array',
                     type=str,
                     default='mkat',
                     help="Name of telescope / array (default array='%default')")
    group.add_option('--lat',
                     action='store',
                     dest='lat',
                     type=str,
                     default='-30:42:47.4',
                     help="Latitude (default MeerKAT lat='%default')")
    group.add_option('--lon',
                     action='store',
                     dest='lon',
                     type=str,
                     default='21:26:38.0',
                     help="Longitude (default MeerKAT lon='%default')")
    group.add_option('--alt',
                     action='store',
                     dest='alt',
                     type=str,
                     default='1060.0',
                     help="Altitude (default MeerKAT alt='%default')")
    parser_.add_option_group(group)

    # coordinate options
    group = OptionGroup(parser_, 'Coordinate Classification')
    group.add_option('--enu',
                     dest='enu',
                     action='store_true',
                     default=False,
                     help='Antenna position file giving ENU coordinates using format: E N U dish_diam station mount\n \
Default if not specified is ITRF coordinates using format: X Y Z diameter station mount')
    parser_.add_option_group(group)

    # output options
    group = OptionGroup(parser_, 'Output Options')
    group.add_option('-o', '--output',
                     dest='savegraph',
                     action='store_true',
                     default=False,
                     help='Save graphs to PNG format')
    group.add_option('-v', '--verbose',
                     dest='verbose',
                     action='store_true',
                     default=False,
                     help='Display results and all graphs')
    group.add_option('--debug',
                     dest='debug',
                     action='store_true',
                     default=False,
                     help='Display additional debug results')
    parser_.add_option_group(group)

    return parser_
