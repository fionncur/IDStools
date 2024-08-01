"""
Service classes for handling i_d_ss

@author: Hajo Klingshirn, MPI-IPP
"""

from idstools.database import DBMaster
from idstools.helper import make_sequence
import imas
import logging
import os
import sys

# List of all IDS names to be read if 'all' is supplied as a IDS name
a_l_l__i_d_s_s = "edge"

logger = logging.getLogger("module")


class imas_db:
    """Helper class wrapping an IMAS database entry."""

    def __init__(
        self,
        shot,
        run,
        user=None,
        tokamak=None,
        version=None,
        do_open=True,
        use_h_d_f5=False,
    ):
        """Creates an object wrapping a database entry with the given parameters.
        Shot and run number have to be given.

        If user, tokamak, version are omitted, the values set in the environment are used
        (environment variables USER, TOKAMAKNAME, DATAVERSION).

        The doOpen argument specifies whether the database is opened immediately.
        If set to False, opening the database is delayed to the first access.

        The useHDF5 property controls whether UAL access is done through HDF5 (instead of the default MDSPlus.
        If set to True, the parameters user, tokamak and version have no effect."""

        self._shot = shot
        self._run = run

        # Environment parameters
        self._user = user
        self._tokamak = tokamak
        self._version = version
        # We want to use open_env, so we need proper parameters for it
        if not self._user:
            self._user = os.getenv("USER")
        if not self._tokamak:
            self._tokamak = os.getenv("MDSPLUS_TREE_BASE_0").split("/")[-3]
        if not self._version:
            self._version = DBMaster.get_dd_version().split(".")[0]

        self._use_h_d_f5 = use_h_d_f5
        self._db_u_a_l_d_a_o = None  # this is the UAL data access object (DAO)

    @property
    def shot(self):
        """Returns the shot number"""
        return self._shot

    @property
    def run(self):
        """Returns the run number."""
        return self._run

    @property
    def version(self):
        """Returns the IMAS data version."""
        return self._version

    def __str__(self):
        """Returns an identifier string for the database.

        Format: shot/run"""
        return str(self._shot) + "/" + str(self._run)

    @property
    def db(self):
        if not self._db_u_a_l_d_a_o:
            self._open()
        return self._db_u_a_l_d_a_o

    def close(self):
        """Close the UAL database access object for this database."""
        if self._db_u_a_l_d_a_o:
            self._db_u_a_l_d_a_o.close()
            self._db_u_a_l_d_a_o = None

    def reopen(self):
        """Reopen the database."""
        if self._db_u_a_l_d_a_o:
            self.close()
        self._open()

    def _open(self):
        """Open database."""
        logging.debug("Opening database " + str(self))

        self._db_u_a_l_d_a_o = imas.ids(self._shot, self._run)
        if self._use_h_d_f5:
            self._db_u_a_l_d_a_o.open_hdf5()
        else:
            self._db_u_a_l_d_a_o.open_env(self._user, self._tokamak, self._version)

        return self._db_u_a_l_d_a_o

    def _create(self):
        """Create database."""

        logging.debug("Creating dtabase " + str(self))
        db_u_a_l_d_a_o = imas.ids(self._shot, self._run)

        if self._use_h_d_f5:
            db_u_a_l_d_a_o.create_hdf5()
        else:
            db_u_a_l_d_a_o.create_env(self._user, self._tokamak, self._version)

        self._db_u_a_l_d_a_o = db_u_a_l_d_a_o
        return self._db_u_a_l_d_a_o

    def times(self, ids_name):
        """Return list of time points for the timeslices for which the IDS with given name is present.

        If no time slices present for the IDS, returns an empty list."""
        # print('X', idsName, 'X')
        (status, times) = self.db.get_times(ids_name)
        return times

    # TODO to be removed.. migrated to idshelper.getAvailableIdsAndTimes
    def all_times(self):
        """Returns a list of existing timeslices for all time-dependent IDSs present in the database."""
        import inspect

        def is_ids(obj):
            try:
                obj.__getattribute__("ids_properties")
                return True
            except Exception as e:
                logger.debug(f"{e}")
                return False

        def timedep_ids_test(x):
            return is_ids(x)

        timedep_idss = inspect.getmembers(self.db, timedep_ids_test)

        result = []
        for idsname_array, obj in timedep_idss:
            try:
                max_occurrences = obj.get_max_occurrences()
            except AttributeError:
                max_occurrences = 1
            for occurrence in range(max_occurrences + 1):
                if occurrence == 0:
                    idsname = idsname_array
                else:
                    idsname = idsname_array + "/" + str(occurrence)
                try:
                    times = self.times(idsname)
                except Exception as e:
                    logger.debug(f"{e}")
                    times = []
                    print(
                        "ERROR! IDS '" + idsname + "': Reading time array fails due to following problem : " + str(e),
                        file=sys.stderr,
                    )
                if times is not None and len(times):
                    result.append((idsname, times))

        return result

    def get_ids(self, ids_name, time=None, do_open=True):
        """Get IDS with given name. For time-dependent IDSs, the time has to be given.

        If the optional argument time is set to False, reading of the IDS data is delayed
        to the first access."""
        return ids(
            self._shot,
            self._run,
            ids_name,
            time=time,
            user=self._user,
            tokamak=self._tokamak,
            version=self._version,
            do_open=do_open,
            use_h_d_f5=self._use_h_d_f5,
            parent_imas_db=self,
        )

    def get_ids_array(self, ids_name, do_open=False):
        """ """
        ids_array_name = ids_name + "Array"
        if ids_array_name not in self.db.__dict__:
            # TODO: maybe throw exception
            return []

        ids_array = eval("self._dbUALDAO." + ids_array_name)
        ids_array.get()
        idss = [
            ids(
                self._shot,
                self._run,
                ids_name,
                time=ids_u_a_l_d_a_o.time,
                user=self._user,
                tokamak=self._tokamak,
                version=self._version,
                do_open=do_open,
                use_h_d_f5=self._use_h_d_f5,
                parent_imas_db=self,
                ids_u_a_l_d_a_o=ids_u_a_l_d_a_o,
            )
            for ids_u_a_l_d_a_o in ids_array.array
        ]
        return idss


class ids:
    """Helper class wrapping a UAL IDS data structure to add high-level functionality."""

    def __init__(
        self,
        shot,
        run,
        ids_name,
        time=None,
        user=None,
        tokamak=None,
        version=None,
        do_open=True,
        use_h_d_f5=False,
        parent_imas_db=None,
        ids_u_a_l_d_a_o=None,
    ):
        """Creates an object wrapping an IDS with the given parameters. Shot number, run number and
        ids name (e.g. 'equilibrium') have to be given. For time-dependent IDSs, time has to be given.

        If user, tokamak, version are omitted, the values set in the environment are used
        (variables USER, TOKAMAKNAME, DATAVERSION).

        The doOpen parameter controls whether UAL access is done immediately when creating the Ids object.
        If it is set to False, UAL access is deferred to the first access to IDS data.

        The useHDF5 property controls whether UAL access is done through HDF5. If set to True, the
        parameters user, tokamak and version have no effect."""

        if parent_imas_db:
            self._parent_imas_db = parent_imas_db
        else:
            # logging.debug("Creating exclusive ImasDb object for ids")
            self._parent_imas_db = imas_db(shot, run, user, tokamak, version, do_open, use_h_d_f5)

        self._ids_u_a_l_d_a_o = ids_u_a_l_d_a_o

        self._ids_name = ids_name
        self._time = time

        if do_open:
            self.ids

    @property
    def shot(self):
        """The shot number of the IDS."""
        return self._parent_imas_db.shot

    @property
    def run(self):
        """The run number of the IDS."""
        return self._parent_imas_db.run

    @property
    def version(self):
        """The IMAS data version."""
        return self._parent_imas_db.version

    @property
    def name(self):
        """The name of the IDS (e.g. 'equilibrium')."""
        return self._ids_name

    @property
    def time(self):
        """The time value of the IDS."""
        return self._time

    def __str__(self):
        """Returns an identifier string for the IDS

        Format: shot/run/time/name for time-dependent IDSs,
        shot/run/name for non-time-dependent IDSs."""
        name = str(self.shot) + "/" + str(self.run)
        if self._time is not None:
            name += "/" + str(self._time)
        return name + "/" + self.name

    @property
    def ids(self):
        """The IDS data object associated with this IDS object as provided by the UAL Python interface."""
        if self._ids_u_a_l_d_a_o is None:
            self._retrieve_from_ual()
        return self._ids_u_a_l_d_a_o

    def close(self):
        """Close the UAL database access object for this IDS."""
        self._parent_imas_db.close()
        self._ids_u_a_l_d_a_o = None

    def reload(self):
        """Reload the IDS data from the UAL."""
        self.close()
        self._retrieve_from_ual()

    def _retrieve_from_ual(self):
        """Retrieve the IDS described by this object from the UAL and return it.

        Subsequent calls will return the instance created on the first call."""

        if self._ids_u_a_l_d_a_o:
            return self._ids_u_a_l_d_a_o

        logging.debug("Retrieving IDS " + str(self))

        eval("db = + self._parentImasDb.db")
        self._ids_u_a_l_d_a_o = eval("db." + self._ids_name)

        if hasattr(self._ids_u_a_l_d_a_o, "get"):
            # Time-independent IDS
            self._ids_u_a_l_d_a_o.get()
        elif hasattr(self._ids_u_a_l_d_a_o, "getSlice"):
            times = self._parent_imas_db.times(self.name)
            if len(times) == 0:
                raise ValueError("No slices stored for IDS " + self.name)
            # Time-dependent IDS
            if self._time is None:
                raise ValueError("Need valid time for getting a time-dependent IDS")
            self._ids_u_a_l_d_a_o.get_slice(self._time, imas.imasdef.c_l_o_s_e_s_t__i_n_t_e_r_p)
        else:
            raise TypeError("Found unexpected type of IDS, check IDS name")

        return self._ids_u_a_l_d_a_o


class ids_descriptor:
    """Helper class describing one or more IDSs and presenting them as a sequence.

    It holds combinations of  shot/run number(s), IDS name(s), time stamp(s), user/tokamak/version.
    """

    # TODO: add occurrence...?

    def __init__(
        self,
        shot,
        run,
        ids_names="all",
        time=0.0,
        user=None,
        tokamak=None,
        version=None,
        do_open=True,
        use_h_d_f5=False,
    ):
        """Create a IDS Descriptor.

        Every parameter to the constructor can
        be either a single value or a tuple. The IdsDescriptor then describes
        all possible combinations of these parameters. The order of the IDSs
        is obtained by iterating the leftmost parameter first.

        If one of user, tokamak, version are omitted, the resulting IDS
        will take the values set in the environment (variables USER, TOKAMAKNAME, DATAVERSION).

        If doOpen = False is given, UAL access for the resulting IDSs is deferred to the first
        method call that accesses IDS data.

        If useHDF5 = True is specified, UAL access is done via HDF5 instead of MDSPlus. In this
        case, user/tokamak/version have no effect."""

        # Make sure every parameter is a sequence
        self._shot = make_sequence(shot)
        self._run = make_sequence(run)
        self._ids_names = make_sequence(ids_names)
        self._time = make_sequence(time)

        # Environment parameters
        self._user = make_sequence(user)
        self._tokamak = make_sequence(tokamak)
        self._version = make_sequence(version)

        # Access parameters
        self._do_open = do_open
        self._use_h_d_f5 = use_h_d_f5

        # Expand "all" IDS name into list of IDSs using the general grid description
        if self._ids_names[0] == "all":
            self._ids_names = a_l_l__i_d_s_s

        # Figure out the counts for the individual parameters
        self._n_par = [
            1,
        ] * 7
        self._n_par[0] = len(self._shot)
        self._n_par[1] = len(self._run)
        self._n_par[2] = len(self._ids_names)
        self._n_par[3] = len(self._time)
        self._n_par[4] = len(self._user)
        self._n_par[5] = len(self._tokamak)
        self._n_par[6] = len(self._version)

    def __str__(self):
        """Return a string representation in the form shot/run/time/ids name/user/tokamak/version,
        where individual values are either scalars or tuples."""
        return (
            str(self._shot)
            + "/"
            + str(self._run)
            + "/"
            + str(self._time)
            + "/"
            + str(self._ids_names)
            + "/"
            + str(self._user)
            + "/"
            + str(self._tokamak)
            + "/"
            + str(self._version)
        )

    def __len__(self):
        """Return number of IDSs described by this descriptor."""
        product = 1
        for i in self._n_par:
            product = product * i
        return product

    def __getitem__(self, ind):
        """Returns the IDS object for the given index as a Ids object."""
        if (ind < 0) or (ind >= len(self)):
            raise IndexError()

        # set up object counts for every components of the local index
        i_count = [
            1,
        ] * len(self._n_par)
        for i in range(len(self._n_par) - 1):
            i_count[-i - 2] = i_count[-i - 1] * self._n_par[-i - 1]

        # From global index ind, compute local index tuple lInd (which is 0-based)
        l_ind = [
            0,
        ] * len(self._n_par)
        t_ind = ind
        for i in range(len(self._n_par)):
            l_ind[i] = t_ind / i_count[i]
            t_ind -= l_ind[i] * i_count[i]

        # create IDS object
        return ids(
            self._shot[l_ind[0]],
            self._run[l_ind[1]],
            self._ids_names[l_ind[2]],
            self._time[l_ind[3]],
            self._user[l_ind[4]],
            self._tokamak[l_ind[5]],
            self._version[l_ind[6]],
            self._do_open,
            self._use_h_d_f5,
        )


def get_all_idss(ids_descs):
    """Get a list of all IDSs described by a list of IDS descriptors."""
    all = []
    for desc in ids_descs:
        idss = list(desc)
        all.extend(idss)
    return all


def field_filled(idsfield):
    """Check whether a given field of a IDS is filled with data."""
    # TODO: check how to make this general for all IDS fields...
    return len(idsfield) != 0
