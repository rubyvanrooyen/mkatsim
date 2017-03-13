from optparse import OptionGroup

from ..common import option
from .main import main


def cli():
    usage = '%prog [options] <ant_pos_file>'
    parser = option.parser(usage=usage)

    # now add unique options

    # antenna selection
    group = OptionGroup(parser, 'Antenna Selection for Subarray')
    group.add_option('--sub',
                     action='store',
                     dest='subarray',
                     type=str,
                     default=None,
                     help='Name of subarray as defined in config')
    group.add_option('--ant',
                     action='store',
                     dest='antenna_list',
                     type=str,
                     default=None,
                     help='Comman separated list of antenna names')
    parser.add_option_group(group)

    # layout
    group = OptionGroup(parser, 'Layout Options')
    group.add_option('--layout',
                     dest='arr_layout',
                     action='store_true',
                     default=False,
                     help='Generate simple array layout')
    group.add_option('--map',
                     dest='genmap',
                     action='store_true',
                     default=False,
                     help='Generate detailed map of array layout')
    group.add_option('-s', '--save',
                     dest='savesubarray',
                     action='store_true',
                     default=False,
                     help='Save selected subarray to ITRF file')
    parser.add_option_group(group)
    (opts, args) = parser.parse_args()

    if len(args) < 1:
        print('Antenna position file needed for Array Map generation')
        parser.print_usage()
        raise SystemExit

    main(opts, args)


if __name__ == '__main__':
    cli()

# -fin-
