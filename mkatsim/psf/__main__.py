from optparse import OptionParser, OptionGroup


def cli():
    usage = '%prog [options] --cfg <makems.cfg> <ant_pos_file>'
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
                     help='Antenna table name,'
                     ' else ANTENNA table will be generated')
    parser.add_option_group(group)
    group = OptionGroup(parser, 'Basic wsclean options')
    group.add_option('--dec',
                     action='store',
                     dest='declination',
                     type=str,
                     default='-60',
                     help='Declination for simulation.'
                     ' Use comma separated list for multiple declinations')
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
                     default=0.05,  # hr
                     help='Total synthesis / integration time in hours'
                     ' (default snapshot of 3 minutes).')
#SEPARATE UIT MAKEMS SE OPTIONS EN SIT AL DIE WSCLEAN OPTIONS IN
    group.add_option('--dt',
                     action='store',
                     dest='dt',
                     type=float,
                     default=256,  # sec
                     help='Accumulation time given as nr seconds per dump')
    group.add_option('--dtime',
                     action='store',
                     dest='dtime',
                     type=float,
                     default=12,  # hr
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


if __name__ == '__main__':
    cli()
