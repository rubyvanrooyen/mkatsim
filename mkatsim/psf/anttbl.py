"""Create CASA ANTENNA table for antenna ENU positions"""
#  Similar to mkant.py for LOFAR
import casacore.tables
from casacore.tables import tablecreatescalarcoldesc as cldsc
from casacore.tables import tablecreatearraycoldesc as clarrdsc

# Use an ordered dictionary so table columns are in the expected order
class ord_dict(dict):
    def __init__(self):
        dict.__init__(self)
        self._order = []
    def __setitem__(self, key, value):
        self._order.append(key)
        dict.__setitem__(self, key, value)
    def keys(self):
        return self._order
    def __iter__(self):
        self._iter_n = 0
        return self
    def next(self):
        if self._iter_n == len(self._order):
            raise StopIteration
        self._iter_n += 1
        return self._order[self._iter_n - 1]

# From pyrap/casacore but using ordered dictionary
def tablecreatedesc(descs = []):
    rec = ord_dict()
    for desc in descs:
        colname = desc['name']
        if rec.has_key(colname):
            raise ValueError('Column name ' + name + ' multiply used in table description')
        rec[colname] = desc['desc']
    return rec;

# Build table for given list of antennas
def make_tbl(tblname, ant_list):
    # Define columns
    offset_desc = clarrdsc('OFFSET', value = float(), ndim = 1, shape = [3])
    position_desc = clarrdsc('POSITION', value = float(), ndim = 1, shape = [3])
    type_desc = cldsc('TYPE', value = str())
    dish_desc = cldsc('DISH_DIAMETER', value = float())
    flag_desc = cldsc('FLAG_ROW', value = bool())
    mount_desc = cldsc('MOUNT', value = str())
    name_desc = cldsc('NAME', value = str())
    station_desc = cldsc('STATION', value = str())

    desc = tablecreatedesc([offset_desc, position_desc, type_desc, dish_desc, flag_desc, mount_desc, name_desc, station_desc])

    # Create and populate our table
    table = casacore.tables.table(tblname, desc, nrow = len(ant_list), readonly = False)
    table.putcolkeywords('OFFSET', {'QuantumUnits': ['m', 'm', 'm'], 'MEASINFO': {'Ref': 'ITRF', 'type': 'position'}})
    table.putcolkeywords('POSITION', {'QuantumUnits': ['m', 'm', 'm'], 'MEASINFO': {'Ref': 'ITRF', 'type': 'position'}})
    table.putcolkeywords('DISH_DIAMETER', {'QuantumUnits': ['m']})
    table[:] = {'DISH_DIAMETER': 13.5, 'OFFSET': [0.0,0.0,0.0], 'TYPE': 'GROUND-BASED', 'MOUNT': 'ALT_AZ'}
    for i in range(len(ant_list)):
        table[i] = ant_list[i]

# -fin-

