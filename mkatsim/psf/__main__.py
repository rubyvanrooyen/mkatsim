from optparse import OptionGroup

from ..common import option
from .main import main


def cli():
    usage = '%prog [options] --cfg <makems.cfg> <ant_pos_file>'
    parser = option.parser(usage=usage)

    # now add unique options

    # standard options
    parser.add_option('--cfg',
                      action='store',
                      dest='cfg',
                      type=str,
                      default=None,
                      help='\
Config file for makems')
    parser.add_option('--table',
                      dest='ant_table',
                     action='store_true',
                     default=False,
                      help='\
Create a CASA antenna table')
    parser.add_option('--ant_list',
                      action='store',
                      dest='ant_list',
                      type=str,
                      default=None,
                      help='Comma separated list of antenna names')
    # makems simulation options
    group = OptionGroup(parser, 'MAKEMS Simulation Options')
    group.add_option('--ant',
                     action='store',
                     dest='tblname',
                     type=str,
                     default=None,
                     help='\
Antenna table name, else ANTENNA table will be generated')
    group.add_option('--ms',
                     action='store',
                     dest='msname',
                     type=str,
                     default=None,
                     help='\
Name of the measurement set to create')
    group.add_option('--stime',
                     action='store',
                     dest='stime',
                     type=str,
                     default=None,
                     help='\
Observation start time YYYY/MM/DD/hh:mm:ss.')
    group.add_option('--synthesis',
                     action='store',
                     dest='synthesis',
                     type=float,
                     default=300,  # sec
                     help='\
Total synthesis / integration time in seconds \
(default snapshot of 5 minutes).')
# to prevent time smearing on MeerKAT longest baselines
    group.add_option('--dt',
                     action='store',
                     dest='dt',
                     type=float,
                     default=4,  # sec
                     help='\
Accumulation time given as nr seconds per dump \
(default rate %default seconds per dump)')
    group.add_option('--dtime',
                     action='store',
                     dest='dtime',
                     type=float,
                     default=12,  # hr
                     help='\
Regular separation of simulated integration series \
(default is a scan every %default hours.)')
    group.add_option('--dec',
                     action='store',
                     dest='declination',
                     type=str,
                     default='-60d00m00.0s',
                     help="\
J2000 declination for simulation default %default")
    group.add_option('--ra',
                     action='store',
                     dest='rightascension',
                     type=str,
                     default='00h00m00.0s',
                     help='\
J2000 right ascension for simulation default %default')
    group.add_option('--nparts',
                     action='store',
                     dest='nparts',
                     type=int,
                     default=1,
                     help='\
Nr of parts into which the measurement set is to be split')
    group.add_option('--nbands',
                     action='store',
                     dest='nbands',
                     type=int,
                     default=1,
                     help='\
Nr of subbands to use, default=%default and max=4.')
    group.add_option('--nfreqs',
                     action='store',
                     dest='nfreqs',
                     type=int,
                     default=512,
                     help='\
Total number of frequencies')
    group.add_option('--sfreq',
                     action='store',
                     dest='sfreq',
                     type=str,
                     default='856.0e+06',  # Hz
                     help='\
Comma separated list of length NBands with start frequency per band')
    group.add_option('--stepfreq',
                     action='store',
                     dest='stepfreq',
                     type=str,
                     default='1671872.0',  # Hz
                     help='\
Comma separated list of length NBands with step frequency per band')
    parser.add_option_group(group)

    # wsclean simulation options
    group = OptionGroup(parser, 'WSCLEAN Simulation Options')
    choices = ['natural', 'uniform', 'briggs']
    group.add_option('--weight',
                     action='store',
                     type='choice',
                     choices=choices,
                     default='uniform',
                     help="\
Weightmode can be: %s (default=%s).\n \
When using Briggs' weighting, add the robustness parameter"
                     % (', '.join(choices), 'uniform'))
    group.add_option('--robust',
                     action='store',
                     type=float,
                     default=0.0,
                     help='\
Robustness parameter for briggs weighting (-2 <= x <= 2)')
    group.add_option('--superweight',
                     action='store',
                     type=float,
                     default=1.0,
                     help="\
Increase the weight gridding box size, \
similar to Casa's superuniform weighting scheme (default %default). \
The factor can be rational and can be less than one for subpixel weighting.")
    group.add_option('--taper-gaussian',
                     action='store',
                     type=str,
                     default=None,
                     help="\
Taper the weights with a Gaussian function ('--taper-gaussian <beamsize>'). \
This will reduce the contribution of long baselines. \
The beamsize is by default in asec, but a unit can be specified ('2amin').")
    group.add_option('--taper-tukey',
                     action='store',
                     type=str,
                     default=None,
                     help="\
Taper the outer weights with a Tukey transition ('--taper-tukey <lambda>'). \
Lambda specifies the size of the transition; use in combination with option 'maxuv-l'.")  # noqa
    group.add_option('--taper-inner-tukey',
                     action='store',
                     type=str,
                     default=None,
                     help="\
Taper the weights with a Tukey transition ('--taper-inner-tukey <lambda>'). \
Lambda specifies the size of the transition; use in combination with option 'minuv-l'.")  # noqa
    group.add_option('--taper-edge',
                     action='store',
                     type=str,
                     default=None,
                     help='\
Taper the weights with a rectangle, to keep a space of lambda between \
the edge and gridded visibilities.')
    group.add_option('--taper-edge-tukey',
                     action='store',
                     type=str,
                     default=None,
                     help="\
Taper the edge weights with a Tukey window ('--taper-edge-tukey <lambda>'). \
Lambda is the size of the Tukey transition. \
When option 'taper-edge' is also specified, the Tukey transition starts \
inside the inner rectangle.")
    group.add_option('--maxuv-l',
                     action='store',
                     type=str,
                     default=None,
                     help='\
Set the min/max uv distance in lambda (--maxuv-l <lambda>).')
    group.add_option('--minuv-l',
                     action='store',
                     type=str,
                     default=None,
                     help='\
Set the min/max uv distance in lambda (--minuv-l <lambda>).')
    group.add_option('--make-psf-only',
                     action='store_true',
                     default=False,
                     help='\
Only make the psf, no images are made.')
    parser.add_option_group(group)

    # PSF slice options
    group = OptionGroup(parser, 'PSF slice')
    group.add_option('--beamwidth',
                     action='store',
                     dest='beamwidth',
                     type=float,
                     default=None,
                     help='Beamwidth in arcseconds')
    group.add_option('--crop',
                     dest='crop',
                     action='store_true',
                     default=False,
                     help='Crop the PSF to size')
    parser.add_option_group(group)
    (opts, args) = parser.parse_args()

    if len(args) < 1 and opts.tblname is None:
        print('Cannot simulate PSF: Antenna position file needed')
        parser.print_usage()
        raise SystemExit
    if len(args) > 1:
        print('Simulations using multiple antenna position files not supported currently')  # noqa
        parser.print_usage()
        raise SystemExit
    if opts.cfg is None and not opts.ant_table:
        print('Cannot simulate PSF: Need makems config file')
        parser.print_usage()
        raise SystemExit

    # makems input parameter requirements
    # nbands must be divisible by nparts
    if (opts.nbands % opts.nparts) > 0:
        print('NBands is not divisible by NParts')
        raise RuntimeError

    # nfreqs must be divisible by nbands
    if (opts.nfreqs % opts.nbands) > 0:
        print('NFrequencies not divisible by NBands')
        raise RuntimeError

    # nr start frequencies must be equal to nr subbands
    if len(opts.sfreq.split(',')) != opts.nbands:
        print('Need to provide a start frequency per subband')
        raise RuntimeError

    # nr frequencies steps must be equal to nr subbands
    if len(opts.stepfreq.split(',')) != opts.nbands:
        print('Need to provide a start frequency per subband')
        raise RuntimeError

    # ensure that (ra,dec) coordinates in correct format for makems
    from astropy.coordinates import SkyCoord
    from astropy import units as u
    coord_str = '%s %s' % (opts.rightascension, opts.declination)
    c = SkyCoord(coord_str, unit=(u.hourangle, u.deg))
    opts.rightascension = '%.3fdeg' % c.ra.deg
    opts.declination = '%.3fdeg' % c.dec.deg

    main(parser, opts, args)


if __name__ == '__main__':
    cli()
