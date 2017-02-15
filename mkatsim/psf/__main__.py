from optparse import OptionParser, OptionGroup

from .main import main
from .. import _version


def cli():
    from optparse import OptionParser, OptionGroup
    usage='%prog [options] --cfg <makems.cfg> <ant_pos_file>'
    parser = OptionParser(usage=usage, version="%prog " + _version.__version__)
    parser.add_option('--array',
                      action='store',
                      dest='array',
                      type=str,
                      default='mkat',
                      help='Name of telescope / array')
    parser.add_option('--cfg',
                      action='store',
                      dest='cfg',
                      type=str,
                      default=None,
                      help='Config file for makems')
    group = OptionGroup(parser, 'MeerKAT Telescope')
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
    group = OptionGroup(parser, 'Coordinate Classification')
    group.add_option("--enu",
                      dest='enu',
                      action="store_true",
                      default=False,
                      help="Antenna position file giving ENU coordinates")
    parser.add_option_group(group)
    group = OptionGroup(parser, 'Make MS Simulation Options')
    group.add_option('--ant',
                      action='store',
                      dest='tblname',
                      type=str,
                      default=None,
                      help='Antenna table name, else ANTENNA table will be generated')
    group.add_option('--synthesis',
                      action='store',
                      dest='synthesis',
                      type=float,
                      default=0.05, # hr
                      help='Total synthesis / integration time in hours (default snapshot of 3 minutes).')
    group.add_option('--dt',
                      action='store',
                      dest='dt',
                      type=float,
                      default=256, # sec
                      help='Accumulation time given as nr seconds per dump (default rate %default seconds per dump')
    group.add_option('--dtime',
                      action='store',
                      dest='dtime',
                      type=float,
                      default=12, # hr
                      help='Regular separation of simulated integration series (default is a scan every %default hours.')
    group.add_option('--dec',
                      action='store',
                      dest='declination',
                      type=str,
                      default='-60',
                      help='Declination for simulation. Use comma separated list for multiple declinations such as \'-60,-30,-10\' (default is %default deg)')
    group.add_option('--stime',
                      action='store',
                      dest='stime',
                      type=str,
                      default=None,
                      help='Observation start time YYYY/MM/DD/hh:mm.')
    parser.add_option_group(group)
    group = OptionGroup(parser, 'Clean Options wsclean')
    group.add_option('--weight',
                      action='store',
                      dest='weight',
                      type=str,
                      default='briggs',
                      help='Type of weighting to use can be anything accepted by casa (default %default)')
    group.add_option('--robust',
                      action='store',
                      dest='robust',
                      type=float,
                      default=-0.5,
                      help='Robustness parameter for briggs weighting (default %default)')
    parser.add_option_group(group)
    group = OptionGroup(parser, 'Output Options')
    group.add_option('-o', "--output",
                      dest='savegraph',
                      action="store_true",
                      default=False,
                      help="Save graphs to PNG format")
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

    main(opts, args)


if __name__ == '__main__':
    cli()
