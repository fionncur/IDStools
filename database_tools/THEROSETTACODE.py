# THE ROSETTA CODE

import imas
from imas import imasdef
import pandas as pd
import numpy as np
import argparse


def ids_setter(IDS, path, val):
    try:
        dodi = IDS
        for node in path[0:-1]:
            if '(' in node:
                aos = node.split('(')
                ind = int(aos[1][:1])
                dodi = getattr(dodi, aos[0])
                dodi.resize(ind+1, keep=True)
                dodi = dodi[ind]
            else:
                try:
                    dodi = getattr(dodi, node)
                except AttributeError:
                    print(str(node) + " could not be found in " + str(path) + ". Please check spelling or IDS entry.")
                    #continue
        node = path[-1]
        try:
            if type(getattr(dodi, node)) == str:
                setattr(dodi, str(node), str(val))
            elif type(getattr(dodi, node)) == float:
                setattr(dodi, str(node), float(val))
            elif type(getattr(dodi, node)) == int:
                setattr(dodi, str(node), int(val))
            elif type(getattr(dodi, node)) == np.ndarray:
                if (getattr(dodi, node)).dtype == 'int32':
                    setattr(dodi, str(node), (np.array([val], dtype='object')))
                elif (getattr(dodi, node)).dtype == 'float64':
                    setattr(dodi, str(node), (np.array([val], dtype='float64')))
            else:
                print("The type of " + str(idspath) + " is not recognized. Make sure it is either a string, float, integer or numpy.ndarray.")
        except AttributeError:
            print("The leaf '" + str(node) + "' could not be found in " + str(path) + ". Please check spelling or IDS Entry")
    except KeyError:
        print(str(var) + " cannot be stored in " + str(idspath) + " (path not found). Please check spelling and IDS entry.")


parser = argparse.ArgumentParser(description="This script tries to apply mapping into IDS rules to the content of a non-IDS database (e.g. ITPA DBs).")
parser.add_argument("-d", "--database", type=str, default="/home/ITER/vidalm/Desktop/HDB5.2.3.csv",
                    help="Path to csv file containing the external database content \t(default=%(default)s)")
parser.add_argument("-m", "--mapping", type=str, default="/home/ITER/vidalm/Desktop/maptest4.csv",
                    help="Path to csv formatted mapping file \t(default=%(default)s)")
parser.add_argument("--varCol", type=str, default='DB VARIABLE',
                    help="Name of the column of the mapping file listing all DB variables \t(default=%(default)s)")
parser.add_argument("--pathCol", type=str, default="IDS PATH",
                    help="Name of the column of the mapping file listing IDS mapping for all DB variables \t(default=%(default)s")
parser.add_argument("-v","--verbose", action='store_true',
                    help="Run in verbose mode")
args = parser.parse_args()

mf = pd.read_csv(args.mapping, keep_default_na=False, usecols=[args.varCol, args.pathCol])
mf.dropna(how="all")
db = pd.read_csv(args.database, skiprows=1, keep_default_na=False, na_values=[""])
db.dropna(how="all")
row = 0
de = imas.DBEntry(imasdef.MDSPLUS_BACKEND, 'test', 1, row)
de.create()
iod = {}
DBVAR = db.iloc[row]

for ids in list(imas.IDSName):
    iod[ids.value] = de.get(ids.value)

    
for var in mf.loc[:, args.varCol]:
    idspath = mf[mf[args.varCol] == var].iloc[0].at[args.pathCol]

    if idspath!='':
        idsname = (idspath.split('/')[0])
        val = db.at[row, var]
        path = idspath.split('/')[1:]

        ids = iod[idsname]
        ids_setter(ids, path, val)
    else:
        if args.verbose:
            print(f"No mapping specified for variable {var}")




s = iod['summary']
barometry = iod['barometry']
s.ids_properties.homogeneous_time = 1

print(barometry.gauge[0].pressure.data)
print(s.boundary.type.value)
print(s.time)
print(s.global_quantities.ip.value)
print(s.global_quantities.volume.value)
de.put(s)


# for var in mf.loc[63, 'DB VARIABLE']:
#     path = idspath.split('/')[1:]
#     x = 0
#     row = 0
#     node = path[x]
#     dodi = getattr(ids, str(node))
#     while node != path[-1]:
#         x = x + 1
#         node = path[x]
#         getattr(dodi, node)
#         locals()["dodi"+str(x)] = dodi
#         if node == path[-1]:
#             if type(db.at[row, var]) == str:
#                 setattr(dodi, str(node), db.at[row, var])
#             else:
#                 setattr(dodi, str(node), (np.array([db.at[row, var]], dtype='float64')))


# idspath2leaf = de.partial_get(str(idsname), str(leaf))
# if type(db.at[row, var]) == str:
# idspath2leaf = [db.at[row, var]]
# else:
# idspath2leaf = np.array([db.at[row, var]], dtype='float64')
# de.put_slice(ids)

#fe = getattr(dodi, node)
#fe.resize(1)
#fe[0] = val

# for var in mf.loc[:, 'DB VARIABLE']:
# print('store '+str(db.at[row, var])+' from '+var+' into '+str(mf[mf['DB VARIABLE'] == var].iloc[0].at['IDS PATH']))
