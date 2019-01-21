'''
Service classes for handling IDSs

@author: Hajo Klingshirn, MPI-IPP
'''
from .helper import *
import logging
import imas

# List of all IDS names to be read if 'all' is supplied as a IDS name
ALL_IDSS = ('edge')

class ImasDb():
    '''Helper class wrapping an IMAS database entry.'''
    def __init__(self, shot, run, user=None, tokamak=None, version=None, doOpen=True, useHDF5=False):
        '''Creates an object wrapping a database entry with the given parameters.
        Shot and run number have to be given.

        If user, tokamak, version are omitted, the values set in the environment are used
        (environment variables USER, TOKAMAKNAME, DATAVERSION).
        
        The doOpen argument specifies whether the database is opened immediately.
        If set to False, opening the database is delayed to the first access.
        
        The useHDF5 property controls whether UAL access is done through HDF5 (instead of the default MDSPlus.
        If set to True, the parameters user, tokamak and version have no effect.'''

        self._shot = shot
        self._run = run

        # Environment parameters
        self._user = user
        self._tokamak = tokamak
        self._version = version
        # We want to use open_env, so we need proper parameters for it
        if not self._user: self._user=os.getenv("USER")
        if not self._tokamak: self._tokamak=os.getenv("MDSPLUS_TREE_BASE_0").split("/")[-3]
        if not self._version: self._version=os.getenv("IMAS_VERSION").split(".")[0]

        self._useHDF5 = useHDF5
        self._dbUALDAO = None # this is the UAL data access object (DAO)

    @property
    def shot(self):
        '''Returns the shot number'''
        return self._shot
    @property
    def run(self):
        '''Returns the run number.'''
        return self._run
    @property
    def version(self):
        '''Returns the IMAS data version.'''
        return self._version

    def __str__(self):
        """Returns an identifier string for the database.
        
        Format: shot/run"""
        return str(self._shot) + '/' + str(self._run)

    @property
    def db(self):
        if not self._dbUALDAO:
            self._open()
        return self._dbUALDAO

    def close(self):
        '''Close the UAL database access object for this database.'''
        if self._dbUALDAO:
            self._dbUALDAO.close()
            self._dbUALDAO = None

    def reopen(self):
        '''Reopen the database.'''
        if self._dbUALDAO:
            self.close()
        self._open()

    def _open(self):
        """Open database."""
        logging.debug("Opening database " + str(self))

        self._dbUALDAO = imas.ids(self._shot, self._run)
        if self._useHDF5:
            self._dbUALDAO.open_hdf5()
        else:
            self._dbUALDAO.open_env(self._user, self._tokamak, self._version)

        return self._dbUALDAO

    def _create(self):
        """Create database."""

        logging.debug("Creating dtabase " + str(self))
        dbUALDAO = imas.ids(self._shot, self._run)

        if self._useHDF5:
            dbUALDAO.create_hdf5()
        else:
            dbUALDAO.create_env(self._user, self._tokamak, self._version)

        self._dbUALDAO = dbUALDAO
        return self._dbUALDAO

    def times(self, idsName):
        """Return list of time points for the timeslices for which the IDS with given name is present.
        
        If no time slices present for the IDS, returns an empty list."""
        #print('X', idsName, 'X')
        (status, times) = self.db.getTimes(idsName)
        return times

    def all_times(self):
        """Returns a list of existing timeslices for all time-dependent IDSs present in the database."""
        import inspect
        import types

        # FIXME: Crude hack to get names of all time-dependent IDS. Will be fixed with improved UAL interface
        timedep_ids_test = lambda x: isinstance(x, types.InstanceType)
        timedep_idss = inspect.getmembers(self.db, timedep_ids_test )
        #print("IDSS:  ", timedep_idss)

        result = []
        for idsnameArray, obj in timedep_idss:
            #print('X',idsnameArray,'Y',obj)
            for occurrence in xrange(4):
                if occurrence == 0:
                    idsname = idsnameArray
                else:
                    idsname = idsnameArray + '/' + str(occurrence)
                times = self.times(idsname)
                if times is not None and len(times):
                    result.append( (idsname, times) )

        return result

    def get_ids(self, idsName, time=None, doOpen=True):
        """Get IDS with given name. For time-dependent IDSs, the time has to be given.
        
           If the optional argument time is set to False, reading of the IDS data is delayed
           to the first access."""
        return Ids(self._shot, self._run, idsName, time=time,
                   user=self._user, tokamak=self._tokamak, version=self._version,
                   doOpen=doOpen, useHDF5=self._useHDF5, parentImasDb = self )

    def get_ids_array(self, idsName, doOpen=False):
        """ """
        idsArrayName = idsName + "Array"
        if idsArrayName not in self.db.__dict__:
            # TODO: maybe throw exception
            return []

        idsArray = eval('self._dbUALDAO.' + idsArrayName)
        idsArray.get()
        idss = [ Ids(self._shot, self._run, idsName, time=idsUALDAO.time,
                     user=self._user, tokamak=self._tokamak, version=self._version,
                     doOpen=doOpen, useHDF5=self._useHDF5, parentImasDb = self, idsUALDAO = idsUALDAO ) for idsUALDAO in idsArray.array ]
        return idss

class Ids():
    '''Helper class wrapping a UAL IDS data structure to add high-level functionality.'''

    def __init__(self, shot, run, idsName, time=None,
                 user=None, tokamak=None, version=None, doOpen=True, useHDF5=False,
                 parentImasDb = None, idsUALDAO = None ):
        '''Creates an object wrapping an IDS with the given parameters. Shot number, run number and
        ids name (e.g. 'equilibrium') have to be given. For time-dependent IDSs, time has to be given.
        
        If user, tokamak, version are omitted, the values set in the environment are used
        (variables USER, TOKAMAKNAME, DATAVERSION).
        
        The doOpen parameter controls whether UAL access is done immediately when creating the Ids object.
        If it is set to False, UAL access is deferred to the first access to IDS data.
        
        The useHDF5 property controls whether UAL access is done through HDF5. If set to True, the
        parameters user, tokamak and version have no effect.'''

        if parentImasDb:
            self._parentImasDb = parentImasDb
        else:
            #logging.debug("Creating exclusive ImasDb object for ids")
            self._parentImasDb = ImasDb(shot, run, user, tokamak, version, doOpen, useHDF5)

        self._idsUALDAO = idsUALDAO

        self._idsName = idsName
        self._time = time

        if doOpen:
            self.ids

    @property
    def shot(self):
        '''The shot number of the IDS.'''
        return self._parentImasDb.shot
    @property
    def run(self):
        '''The run number of the IDS.'''
        return self._parentImasDb.run
    @property
    def version(self):
        '''The IMAS data version.'''
        return self._parentImasDb.version
    @property
    def name(self):
        '''The name of the IDS (e.g. 'equilibrium').'''
        return self._idsName
    @property
    def time(self):
        '''The time value of the IDS.'''
        return self._time

    def __str__(self):
        """Returns an identifier string for the IDS
        
        Format: shot/run/time/name for time-dependent IDSs,
        shot/run/name for non-time-dependent IDSs."""
        name = str(self.shot) + '/' + str(self.run)
        if self._time is not None:
            name += '/' + str(self._time)
        return name + '/' + self.name

    @property
    def ids(self):
        '''The IDS data object associated with this IDS object as provided by the UAL Python interface.'''
        if self._idsUALDAO is None:
            self._retrieve_from_ual()
        return self._idsUALDAO

    def close(self):
        '''Close the UAL database access object for this IDS.'''
        self._parentImasDb.close()
        self._idsUALDAO = None

    def reload(self):
        '''Reload the IDS data from the UAL.'''
        self.close()
        self._retrieve_from_ual()

    def _retrieve_from_ual(self):
        """Retrieve the IDS described by this object from the UAL and return it.
        
        Subsequent calls will return the instance created on the first call."""

        if self._idsUALDAO:
            return self._idsUALDAO

        logging.debug("Retrieving IDS " + str(self))

        db = self._parentImasDb.db
        self._idsUALDAO = eval('db.' + self._idsName)

        if hasattr(self._idsUALDAO, 'get'):
            # Time-independent IDS
            self._idsUALDAO.get()
        elif hasattr(self._idsUALDAO, 'getSlice'):
            times = self._parentImasDb.times(self.name)
            if len(times) == 0:
                raise ValueError("No slices stored for IDS " + self.name)
            # Time-dependent IDS
            if self._time is None:
                raise ValueError("Need valid time for getting a time-dependent IDS")
            self._idsUALDAO.getSlice(self._time, ual.ualdef.CLOSEST_SAMPLE)
        else:
            raise TypeError("Found unexpected type of IDS, check IDS name")

        return self._idsUALDAO

class IdsDescriptor():
    '''Helper class describing one or more IDSs and presenting them as a sequence.
    
    It holds combinations of  shot/run number(s), IDS name(s), time stamp(s), user/tokamak/version.'''
    # TODO: add occurrence...?

    def __init__(self, shot, run, idsNames='all', time=0.0,
                 user=None, tokamak=None, version=None, doOpen=True, useHDF5=False):
        '''Create a IDS Descriptor.
        
        Every parameter to the constructor can
        be either a single value or a tuple. The IdsDescriptor then describes
        all possible combinations of these parameters. The order of the IDSs
        is obtained by iterating the leftmost parameter first.
        
        If one of user, tokamak, version are omitted, the resulting IDS
        will take the values set in the environment (variables USER, TOKAMAKNAME, DATAVERSION).
        
        If doOpen = False is given, UAL access for the resulting IDSs is deferred to the first
        method call that accesses IDS data.
        
        If useHDF5 = True is specified, UAL access is done via HDF5 instead of MDSPlus. In this
        case, user/tokamak/version have no effect.'''

        # Make sure every parameter is a sequence
        self._shot = make_sequence(shot)
        self._run = make_sequence(run)
        self._idsNames = make_sequence(idsNames)
        self._time = make_sequence(time)

        # Environment parameters
        self._user = make_sequence(user)
        self._tokamak = make_sequence(tokamak)
        self._version = make_sequence(version)

        # Access parameters
        self._doOpen = doOpen
        self._useHDF5 = useHDF5

        # Expand "all" IDS name into list of IDSs using the general grid description
        if self._idsNames[0] == 'all':
            self._idsNames = ALL_IDSS

        # Figure out the counts for the individual parameters
        self._nPar = [1,] * 7
        self._nPar[0] = len(self._shot)
        self._nPar[1] = len(self._run)
        self._nPar[2] = len(self._idsNames)
        self._nPar[3] = len(self._time)
        self._nPar[4] = len(self._user)
        self._nPar[5] = len(self._tokamak)
        self._nPar[6] = len(self._version)

    def __str__(self):
        '''Return a string representation in the form shot/run/time/ids name/user/tokamak/version,
        where individual values are either scalars or tuples.'''
        return str(self._shot) + '/' \
                + str(self._run) \
                + '/' + str(self._time) \
                + '/' + str(self._idsNames) \
                + '/' + str(self._user) \
                + '/' + str(self._tokamak) \
                + '/' + str(self._version)

    def __len__(self):
        '''Return number of IDSs described by this descriptor.'''
        l = 1
        for i in self._nPar:
            l = l * i
        return l
        
    def __getitem__(self, ind):
        '''Returns the IDS object for the given index as a Ids object.'''
        if (ind < 0) or (ind >= len(self)):
            raise IndexError()

        # set up object counts for every components of the local index
        iCount = [1,] * len(self._nPar)
        for i in xrange(len(self._nPar) - 1):
            iCount[-i-2] = iCount[-i-1] * self._nPar[-i-1]

        # From global index ind, compute local index tuple lInd (which is 0-based)
        lInd = [0,] * len(self._nPar)
        tInd = ind
        for i in xrange(len(self._nPar)):
            lInd[i] = tInd / iCount[i]
            tInd -= lInd[i] * iCount[i]

        # create IDS object
        return Ids(self._shot[lInd[0]],
                   self._run[lInd[1]],
                   self._idsNames[lInd[2]],
                   self._time[lInd[3]],
                   self._user[lInd[4]],
                   self._tokamak[lInd[5]],
                   self._version[lInd[6]],
                   self._doOpen,
                   self._useHDF5)

def get_all_idss(idsDescs):
    '''Get a list of all IDSs described by a list of IDS descriptors.'''
    all = []
    for desc in idsDescs:
        idss = list(desc)
        all.extend(idss)
    return all

def field_filled(idsfield):
    """Check whether a given field of a IDS is filled with data."""
    # TODO: check how to make this general for all IDS fields...
    return len(idsfield) != 0
