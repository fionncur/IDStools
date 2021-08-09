# THE ROSETTA CODE

import imas
from imas import imasdef
import pandas as pd
import numpy as np
import argparse
import math


def get_backend_id(name):
    return getattr(imasdef,name+"_BACKEND")


def ids_setter(IDS, path, val):
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


parser = argparse.ArgumentParser(description="This script tries to apply mapping into IDS rules to the content of a non-IDS database (e.g. ITPA DBs).")
parser.add_argument("-i", "--inputCSV", type=str, default="/home/ITER/vidalm/Desktop/HDB5.2.3.csv",
                    help="Path to csv file containing the external database content \t(default=%(default)s)")
parser.add_argument("-m", "--mapping", type=str, default="/home/ITER/vidalm/Desktop/maptest8.csv",
                    help="Path to csv formatted mapping file \t(default=%(default)s)")
parser.add_argument("--varCol", type=str, default='DB VARIABLE',
                    help="Name of the column of the mapping file listing all DB variables \t(default=%(default)s)")
parser.add_argument("--pathCol", type=str, default="IDS PATH",
                    help="Name of the column of the mapping file listing IDS mapping for all DB variables \t(default=%(default)s)")
parser.add_argument("--traCol", type=str, default="TRANSFORMATION",
                    help="Name of the column of the mapping file listing transformations to be done on DB variables \t(default=%(default)s)")
parser.add_argument("--timeloc", type=str, default="summary",
                    help="Name of the IDS from which the time will be extracted to populate time-empty IDSs \t(default=%(default)s")
parser.add_argument("-b", "--backend", type=str, default="MDSPLUS",
                    help="backend format \t(default=%(default)s)")
parser.add_argument("-d", "--database", type=str, default="test",
                    help="target IMAS database name \t(default=%(default)s)")
parser.add_argument("-r", "--row", type=int, default=None,
                    help="Maps data for the given row/entry of the input database \t(processes all rows otherwise)")
parser.add_argument("-v", "--verbose", action='store_true',
                    help="Run in verbose mode")
args = parser.parse_args()

mf = pd.read_csv(args.mapping, keep_default_na=False, usecols=[args.varCol, args.pathCol, args.traCol])
mf.dropna(how="all")
db = pd.read_csv(args.inputCSV, skiprows=1, keep_default_na=False, na_values=['', '9999999','???????'])
db.dropna(how="all")
db = db.replace(to_replace=np.nan, value=None)


rows = [args.row] if args.row!=None else db.index

for row in rows:
    DBVAR = db.iloc[row]
    de = imas.DBEntry(get_backend_id(args.backend),args.database, 1, row)
    de.create()
    iod = {}
    for ids in list(imas.IDSName):
        iod[ids.value] = de.get(ids.value) #getattr(imas,ids.value)()

    for var in mf.loc[:, args.varCol]:
        idspath = mf[mf[args.varCol] == var].iloc[0].at[args.pathCol]
        transformation = mf[mf[args.varCol] == var].iloc[0].at[args.traCol]
        if idspath != '':
            idsname = idspath.split('/')[0]
            path = idspath.split('/')[1:]
            try:
                IDS = iod[idsname]
            except KeyError:
                print(str(idsname)+" is not an IDS name. Please check spelling or IDS entry.")
                break
            if transformation != '':
                try:
                    val = eval(transformation)
                except KeyError as ke:
                    print(var+" could not be transformed with "+str(transformation)+". Please make sure variable names are written in the form DBVAR['var'], and dictionaries end with said variable.")
            else:
                val = db.at[row, var]
            if val != None:
                if type(val) != str and math.isnan(val):
                    if args.verbose:
                        print("Nothing to store for "+str(var)+" in row "+str(row))
                else:
                    ids_setter(IDS, path, val)
                    IDS.ids_properties.homogeneous_time = 1
            else:
                if args.verbose:
                    print(f"No mapping specified for variable {var}")
    for sids in iod.keys():
        if iod[sids].ids_properties.homogeneous_time == 1:
            if iod[sids].time.size == 0:
                iod[sids].time = iod[args.timeloc].time
            try:
                de.put(iod[sids])
            except Exception as ex:
                print(ex)
                print("The IDS "+str(sids)+" could not be put because of a Value Error. IDS Entry should match Database data type (flt, int, str, np.array...), via the transformation column if necessary.")
                break
            print("The IDS "+str(sids)+" for row "+str(row)+" was modified and put successfully")


dd = iod['dataset_description']
s = iod['summary']
barometry = iod['barometry']

print(dd.ids_properties.homogeneous_time)
print(s.boundary.type.value)
print(s.time)
print(s.global_quantities.ip.value)
print(s.global_quantities.volume.value)
print(s.elms.frequency.value)


