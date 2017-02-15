#! /usr/bin/python
# Container for makems wrapper and all parts of it

from __future__ import print_function

import os
import shutil
import subprocess
import tempfile

#Read makems config file into dictionary
def cfg_read(
            cfgfile, # some default config file
           ):
    fin = open(cfgfile, 'r')
    config = fin.readlines()
    fin.close()
    cfg_dict={}
    for line in config:
        [key, value] = line.strip().split('=')
        if cfg_dict.has_key(key): raise RuntimeError('Duplicate key %s' % key)
        cfg_dict[key]=value
    return cfg_dict
#Fake file for makems input
def cfg_write_ms(cfg_file, cfg_dict):
    for key, value in cfg_dict.iteritems():
        # cfg_file.write('%s\n'%('='.join((key, str(value)))))
        print('='.join((key, str(value))), file=cfg_file)
        print('='.join((key, str(value))))  # debug
#Make empty measurement set
def ms_make(opts):
    cfg_dict = cfg_read(opts.cfg)
    ntimesteps = (opts.synthesis*3600./opts.dt) / (12./opts.dtime)
    msname = '%s_%sdeg_%s.ms' % (opts.array, opts.declination, opts.stime.replace('/','-'))
    # generate makems config file
    cfg_dict.update({
       'AntennaTableName': opts.tblname,
       'MSName': msname,
       'Declination': '%sdeg' % opts.declination,
       'NTimes': int(ntimesteps) + 1,
       'StartTime':opts.stime,
       })
    # generate a measurement set
    # http://stackoverflow.com/a/15343686
    with tempfile.NamedTemporaryFile(delete=False) as file:
        cfg_write_ms(file, cfg_dict)
    try:
        subprocess.check_call(['makems', file.name])
    except subprocess.CalledProcessError as e:
        # handle or report exception here, maybe
        pass
    finally:
        os.remove(file.name)
    # this is a lofar script and will use the position information, but loose the namings
    # so the original ANTENNA table needs to be copied back into the MS
    antenna_dir = '%s_p0/ANTENNA' % msname
    antenna_bak = antenna_dir + '.bak'  # this is at least '.bak'
    shutil.rmtree(antenna_bak, ignore_errors=True)  # /should/ be safe enough
    shutil.move(antenna_dir, antenna_bak)
    shutil.copytree(opts.tblname, antenna_dir)
    return '%s_p0'%msname


# -fin
