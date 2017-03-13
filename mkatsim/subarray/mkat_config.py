# #! /usr/bin/python
# ##
# ## Holds hardcoded and predefined parameters used by simulation scripts
# ##
# ###############

import string

class Subarrays():
    def __init__(self, ref_location, array_geocentric, ant_list):
        self.array_ref = ref_location
        self.array = array_geocentric
        self.antennas = ant_list
        # AR array rollout plan 2015
        self.ar2 = ['m063', 'm062', 'm024', 'm025', 'm031', 'm034', 'm015', 'm014', 'm001', 'm003', 'm006', 'm010', 'm008', 'm007', 'm021', 'm022', 'm036', 'm017', 'm018', 'm020', 'm011', 'm012', 'm000', 'm002', 'm005', 'm042', 'm041', 'm040', 'm038', 'm037', 'm030', 'm028']  # noqa
        # Standard subarray configurations
        self.ar1 = [string.lower(ant) for ant in self.ar2[:16]]
        self.mkat = [string.lower(ant) for ant in self.array.keys()]
        self.mkatcore = ['m002', 'm000', 'm005', 'm006', 'm001', 'm003', 'm004', 'm018', 'm020', 'm017', 'm015', 'm029', 'm021', 'm007', 'm019', 'm009', 'm016', 'm011', 'm028', 'm012', 'm027', 'm034', 'm035', 'm014', 'm042', 'm022', 'm013', 'm036', 'm008', 'm031', 'm026', 'm047', 'm030', 'm010', 'm032', 'm041', 'm037', 'm023', 'm038', 'm043', 'm039', 'm040', 'm024', 'm025']  # noqa

    def list_subs(self):
        subarrays = self.__dict__.keys()
        del subarrays[subarrays.index('array_ref')]
        del subarrays[subarrays.index('array')]
        del subarrays[subarrays.index('antennas')]
        print 'Known subarray configurations:\n\t%s' % ', '.join(subarrays)

    def get_sub(self, subname):
        if not subname in self.__dict__:
            raise RuntimeError('Subarray %s not predefined' % subname)
        subarray = {}
        for ant in self.__dict__[subname]:
            subarray[ant] = self.array[ant]
        return subarray

    def def_sub(self, ant_list):
        subarray = {}
        for ant in ant_list:
            subarray[ant] = self.array[ant.strip()]
        return subarray

# -fin-
