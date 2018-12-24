'''
Helper routines to parse command line arguments for typical scripts that access the UAL.

This will be extended quite a bit in 2012.
'''
import optparse
import os

def read_env():
    parser = setup_parser()
    pars, opts, args = parse_cli(parser)
    return pars, args[1:]

def read_shot():
    '''Parse database entry specifier provided on the command line.
    The form of the command line is:
    
        my_program [OPTIONS] IMASDBSPECIFIER
    
    where IMASDBSPECIFIER has the form
    
        shotnum,runnum[,time]
    
    with the time being optional.
    
    Returns a dictionary with all parameters and options and the remaining arguments.'''

    parser = setup_parser()
    pars, opts, args = parse_cli(parser)
    if len(args) == 0:
        raise SystemExit("No shot parameters given")

    pars.update(parseShotDescription(args[0]))

    return pars, args[1:]


def read_shot_ids():
    '''Parse database entry specifier and IDS name provided on the command line.
    The form of the command line is:
    
        my_program [OPTIONS] IMASDBSPECIFIER IDSNAME
    
    where IMASDBSPECIFIER has the form
    
        shotnum,runnum[,time]
    
    with the time being optional. Specifying the IDSNAME is mandatory.
    
    Returns a dictionary with all parameters and options and the remaining arguments.'''

    pars, args = read_shot()

    if len(args) < 1:
        raise SystemExit("Not enough arguments given")

    # FIXME: check that the IDS string makes sense - test against known IDS names (see Matlab interface)
    pars["ids"] = args[0]

    return pars, args[1:]

def read_shot_ids_list():
    '''Parse database entry specifier and IDS name provided on the command line.
    The form of the command line is:
    
        my_program [OPTIONS] IMASDBSPECIFIER [IDSNAME1 IDSNAME2 ...]
    
    where IMASDBSPECIFIER has the form
    
        shotnum,runnum[,time]
    
    with the time being optional. The list of IDSNAMES can be empty.
    
    Returns a dictionary with all parameters.'''

    pars, args = read_shot()
    # FIXME: check that the IDS string makes sense - test against known IDS names (see Matlab interface)
    pars["ids"] = args
    return pars

def parseShotDescription(shotDesc):
    pars = {}
    try:
        parts = shotDesc.split(',')
        if len(parts) >= 2:
            pars["shot"] = int(parts[0])
            pars["run"] = int(parts[1])
        if len(parts) >= 3:
            pars["time"] = float(parts[2])
    except:
        raise SystemExit("Invalid shot description: " + shotDesc)

    return pars

def setup_parser():
    p = optparse.OptionParser()
    p.add_option("-u", "--user", dest="user", default=None)
    p.add_option("-t", "--tokamak", dest="tokamak", default=None)
    p.add_option("-v", "--version", dest="version", default=None)

    p.add_option("--hdf5", action="store_true", dest="useHDF5", default=False)
    p.add_option("--debug", action="store_true", dest="debug", default=False)
    return p

def parse_cli(p):
    opts, args = p.parse_args()

    if ((opts.user is not None) | (opts.tokamak is not None) | (opts.version is not None)) \
        & opts.useHDF5:
        raise SystemExit("HDF5 access method not allowed when specifying user, tokamak or data version.")

    pars = setDefaultParameters()
    if opts.user is not None: pars["user"] = opts.user
    if opts.tokamak is not None: pars["tokamakname"] = opts.tokamak
    if opts.version is not None: pars["dataversion"] = opts.version
    pars["hdf5"] = opts.useHDF5
    pars["debug"] = opts.debug

    return pars, opts, args

def setDefaultParameters():
    default = {}
    default["user"] = os.getenv("USER")
    default["tokamakname"] = os.getenv("MDSPLUS_TREE_BASE_0").split("/")[-3]
    default["dataversion"] = os.getenv("IMAS_VERSION").split(".")[0]
    default["hdf5"] = False
    default["debug"] = False

    return default
