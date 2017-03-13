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

    # positional options
    group = OptionGroup(parser_, 'MeerKAT Telescope')
    ### XXX: shouldn't the next line be group.add_option()?
    parser_.add_option('--array',
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
    parser_.add_option_group(group)

    # coordinate options
    group = OptionGroup(parser_, 'Coordinate Classification')
    group.add_option('--enu',
                     dest='enu',
                     action='store_true',
                     default=False,
                     help='Antenna position file giving ENU coordinates')
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
    parser_.add_option_group(group)

    return parser_
