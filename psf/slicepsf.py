import numpy as np
from scipy import ndimage
import matplotlib.pylab as plt
import pyfits

def along_axes(imfile, verbose=False, output=None):

    #Chop the psf to desired size
    t=pyfits.open(imfile,mode='update')
    t[0].header['NAXIS1']=480
    t[0].header['NAXIS2']=480
    t[0].header['CRPIX1']=241
    t[0].header['CRPIX2']=241
    sl=slice(3600-240,3600+240)
    t[0].data=t[0].data[:,:,sl,sl]
    t.flush()
    t.close()

    fitsfile=pyfits.open(imfile)

    bmaj=float(fitsfile[0].header['BMAJ'])*3600.
    bmin=float(fitsfile[0].header['BMIN'])*3600.
    bpa=float(fitsfile[0].header['BPA'])
    pixels=fitsfile[0].header['NAXIS1']
    pixel_scale=fitsfile[0].header['CDELT1']
    num=100000

    if bpa<=45.0:
        length_angle = np.tan(np.deg2rad(bpa))*(pixels/2)
        major_xmax=pixels
        major_xmin=0.0
        major_ymin=(pixels/2) - length_angle
        major_ymax=(pixels/2) + length_angle
        xmaj_r,ymaj_r=np.linspace(major_xmax, major_xmin, num), np.linspace(major_ymin, major_ymax, num)
        ymin_r,xmin_r=np.linspace(major_xmin, major_xmax, num), np.linspace(major_ymin, major_ymax, num)

    if bpa>45.0 and bpa <=90.0:
        length_angle = np.tan(np.deg2rad(90.0-bpa))*(pixels/2)
        major_xmax=(pixels/2) + length_angle
        major_xmin=(pixels/2) - length_angle
        major_ymax=pixels
        major_ymin=0.0
        xmaj_r,ymaj_r=np.linspace(major_xmax, major_xmin, num), np.linspace(major_ymin, major_ymax, num)
        ymin_r,xmin_r=np.linspace(major_xmin, major_xmax, num), np.linspace(major_ymin, major_ymax, num)

    if bpa>90.0 and bpa <=90.0+45.0:
        length_angle = np.tan(np.deg2rad(bpa-90))*(pixels/2)
        major_xmax=(pixels/2) + length_angle
        major_xmin=(pixels/2) - length_angle
        major_ymax=pixels
        major_ymin=0.0
        xmaj_r,ymaj_r=np.linspace(major_xmin, major_xmax, num), np.linspace(major_ymin, major_ymax, num)
        ymin_r,xmin_r=np.linspace(major_xmax, major_xmin, num), np.linspace(major_ymin, major_ymax, num)

    if bpa >90.0+45.0:
        length_angle = np.tan(np.deg2rad(180.0-bpa))*(pixels/2)
        major_xmax=pixels
        major_xmin=0.0
        major_ymin=(pixels/2) - length_angle
        major_ymax=(pixels/2) + length_angle
        xmaj_r,ymaj_r=np.linspace(major_xmax, major_xmin, num), np.linspace(major_ymax, major_ymin, num)
        ymin_r,xmin_r=np.linspace(major_xmax, major_xmin, num), np.linspace(major_ymin, major_ymax, num)

    #How long is the line in arcseconds
    line_length=np.sqrt(((major_xmax-major_xmin)*pixel_scale)**2 + ((major_ymax-major_ymin)*pixel_scale)**2)*3600.0

    #Cut 50% of the beam
    cut=int(pixels*0.25)

    # Extract the values along the line, using cubic interpolation
    major = ndimage.map_coordinates(fitsfile[0].data[0,0], np.vstack((xmaj_r,ymaj_r)),order=1)
    minor =  ndimage.map_coordinates(fitsfile[0].data[0,0], np.vstack((xmin_r,ymin_r)),order=1)
    pixels_asec=np.linspace(0.,line_length,num)-(line_length/2)

    if verbose or output is not None:
        fig = plt.figure(figsize=(10,7))
        plt.title('Fitted Beam Maj:%4.1f asec. Min:%4.1f asec. PA %3.0f deg.'%(bmaj,bmin,bpa,),fontsize=14)
        plt.plot(pixels_asec,major,color='black',label='Major Axis')
        plt.plot(pixels_asec,minor,linestyle='dashed',color='black',label='Minor Axis')
        plt.xlim([-60.,60.])
        plt.xticks(np.arange(-60,60,20.0))
        plt.axhline(0.0,linestyle='dotted',color='black')
        plt.xlabel('Beam Width (arcseconds)',fontsize=16)
        plt.ylabel('Beam Height',fontsize=16)
        plt.legend(loc='upper left', numpoints=1,fontsize=16)
        plt.yticks(fontsize=16)
        plt.xticks(fontsize=16)
        if output is not None: plt.savefig(output)

    return [major, minor, pixels_asec]

if __name__ == '__main__':
    from optparse import OptionParser, OptionGroup
    usage='%prog [options] <fitsimage>'
    parser = OptionParser(usage=usage, description="Plot a slice through the major and minor axes of a beam.", version="%prog 1.0")
    parser.add_option('-o', '--outfile',
                      action='store',
                      dest='outfile',
                      type=str,
                      default=None,
                      help='Filename for output image')
    parser.add_option('-v', "--verbose",
                      dest='verbose',
                      action="store_true",
                      default=False,
                      help="Display image")
    (opts, args) = parser.parse_args()
    if len(args) < 1:
        print('No Fits image file given')
        parser.print_usage()
        raise SystemExit

    [major, minor, pixels_asec] = along_axes(args[0], verbose=opts.verbose, output=opts.outfile)

    if opts.verbose:
        try: plt.show()
        except: pass # nothing to show

# -fin-
