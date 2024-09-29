#!/usr/bin/env python

import logging
from glob import glob
from os import path

import imas

from idstools import idschk
from idstools.database import DBMaster
from idstools.utils.clihelper import get_backend_id

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
def all_ids_types():
    """Returns a list of strings corresponding to all IDS types defined in the version of IMAS being used."""
    return [ids.value for ids in list(imas.IDSName)]


def available_in_dbentry(db, time_mode=None):
    """Returns a list of pairs (idstype:str,occurrence:int) with data in the given DBEntry.

    Parameters
    ----------
    db: imas.DBEntry object
        an open DBEntry in which available IDSs will be looked for
    time_mode: int, optional
        time_mode of interest (imas.imasdef.IDS_TIME_MODE_HETEROGENEOUS, IDS_TIME_MODE_HOMOGENEOUS or
        IDS_TIME_MODE_INDEPENDENT)
        if not specified, occurrences of IDS in all time modes will be returned
    """
    presentidslist = []
    for idstype in all_ids_types():
        for occ in range(getattr(imas, idstype)().getMaxOccurrences()):
            homogeneous_time = db.partial_get(idstype, "ids_properties/homogeneous_time", occurrence=occ)
            if homogeneous_time != imas.imasdef.EMPTY_INT and (time_mode is None or time_mode == homogeneous_time):
                presentidslist.append((idstype, occ))
    return presentidslist

def load_scenario(user, database, version, backend):
    """
    Return a list of pulses as tuple (shot,run) by using idstools.db_helper

    Parameters
    ----------
    user: str="public"
        Status of user: either public or local. A public user should just be left as public, whereas
        a local user should write their proper identifier
    database: str="ITER"
        Name of database where the data is harbored
    version: str="3"
        String of number of data version
    backend: str="MDSPLUS"
        Name of backend format

    Returns
    -------
    scenarios: list=[]
        List of pulses in tuple as (shot, run)
    """

    logger.info("loading scenario table...")

    scenarios = []
    if backend == "MDSPLUS":
        scenarios = DBMaster.mds_list_pulse_run(DBMaster.get_db_Path(user, database, version), with_status="active")
    elif backend == "HDF5":
        scenarios = DBMaster.hdf5_list_pulse_run(DBMaster.get_db_Path(user, database, version))

    return scenarios


# ----------------------------------------------------------------------


def merge_dict(d1, d2):
    """
    Merge two python dicts

    Parameters
    ----------
    d1: dict
        Type dict with IDS name as key and schema as value
    d2: dict
        Type dict with IDS name as key and schema as value

    Returns
    -------
    dict
        Merged input dicts
    """

    inter_keys = set(d1.keys()) & set(d2.keys())

    d = {**d1, **d2}

    for k in inter_keys:
        d[k] = {**d1.get(k), **d2.get(k)}

    return d


# ----------------------------------------------------------------------


class ScenarioValidator:
    """
    Scenario Validator for IMASDB

    Attributes
    ----------
    DD: dict={}
        Data Dictionary
    SHCEMA: dict={}
        Validation schema
    schema_path: list=[]
        List of shcema file paths in str
    dd_path: str=""
        Path to DD
    """

    dd = {}
    schema = {}
    schema_path = []

    def __init__(self, dd_path=idschk.FILE_IDSDef, schema_path=[]):
        """
        Parameters
        ----------
        dd_path: str=idschk.FILE_IDSDef
            Path to DD
        schema_path: list=[]
            List of shcema file paths in str

        Returns
        -------
        """

        ScenarioValidator.dd or self.load__dd(dd_path)

        if schema_path != ScenarioValidator.schema_path:
            self.load_schema(schema_path)
            ScenarioValidator.schema_path = schema_path

    def load__dd(self, fpath):
        """
        Read the xml file of DD and store in self.DD

        Parameters
        ----------
        fpath: str=""
            Path to DD

        Returns
        -------
        """

        try:
            self.dd = idschk.load_xml(fpath)
        except Exception as e:
            logger.debug(f"{e}")
            raise OSError(f"can not load DD: {fpath}")

        logger.debug(f" DD= {fpath}")
        logger.debug(f" self.DD= {self.dd}")

    def load_schema(self, yaml):
        """
        Read the yaml file of validation shemas and store in self.SCHEMA

        Parameters
        ----------
        yaml: list
            List of file path of validation shcema

        Returns
        -------
        """

        try:
            for f in yaml:
                self.schema[f] = idschk.load_yaml(f)
        except Exception as e:
            logger.debug(f"{e}")
            raise OSError(f"failed to load Schema: {yaml}")

        self.schema = self.arrange_schema(self.schema)

        logger.debug(f" schema file= {f}")
        logger.debug(f" schema = {self.schema}")

    def arrange_schema(self, *args):
        """
        Merge validation schemas of same IDS

        Parameters
        ----------
        args: dict
            Validation schemas in type dict with fpath of yaml files as key

        Returns
        -------
        dict
            Validation schema merged in type dict
        """

        dw = {}
        for a in args:
            dw.update(a)

        d = {}
        for _, schemas in dw.items():
            for idsname in schemas:
                if idsname in d.keys():
                    d[idsname] = merge_dict(d[idsname], schemas[idsname])
                else:
                    d[idsname] = schemas[idsname]

        return {"schema": d}

    def validate(self, db, idsname, occ=0, time=-99.0, fmt=""):
        """
        IDS/occ validation for multiple schemas

        Parameters
        ----------
        db: imas.DBEntry
            Class imas.DBEntry
        idsname: str
            Name of IDS
        occ: int=0
            IDS occurence
        time: float=-99.0
            Specific time[s] for one timeslice validation
        fmt: str=""
            "log" for output using logging, otherwise function print()

        Returns
        -------
        """

        dd0 = [dd for dd in self.dd if dd.get("name") == idsname][0]
        ret = {}
        for fpath, schemas in self.schema.items():
            for key, schema in schemas.items():
                if key == idsname:
                    ids = None
                    db_entry_details = ""
                    if "uri" in db.__dict__:
                        db_entry_details = db.__dict__["uri"]
                    else:
                        if "pulse" in db.__dict__:
                            db_entry_details = f"{db.__dict__['pulse']}/{db.__dict__['run']}"
                        if "shot" in db.__dict__:
                            db_entry_details = f"{db.__dict__['shot']}/{db.__dict__['run']}"

                    logger.info(
                        "- {}/{}/{} < {}".format(
                            db_entry_details,
                            idsname,
                            occ,
                            path.relpath(fpath),
                        )
                    )

                    try:
                        idstime = db.partial_get(idsname, "time", occurrence=occ)
                        #
                        if (time < 0.0) or (idstime is None):
                            ids = db.get(idsname, occurrence=occ)
                        else:
                            tm, itm = idschk.find_time(idstime, time)
                            ids = db.get_slice(idsname, tm, 1, occurrence=occ)
                    except Exception as e:
                        logger.debug(f"{e}")
                        print(f"Cannot retrieve IDS/{idsname}: {e}")
                    #
                    flag, dout = idschk.ids_validator(
                        ids,
                        {key: schema},
                        dd=dd0,
                        occ=occ,
                        # verbose=args.verbose,
                        check_all=True,
                    )
                    #
                    if fmt == "log":
                        if flag:
                            logger.info("- OK")
                        else:
                            logger.error("\n{}".format(idschk.dict_to_yaml(dout)))
                    else:
                        print(idschk.dict_to_yaml(dout))
                    #
                    ret[ids.__name__ + "/" + str(occ)] = flag
        return ret

    def validate_db(self, db, time=-99.0, fmt=""):
        """
        IDS validation in Class DBEntry for multiple schemas

        Parameters
        ----------
        db: imas.DBEntry
            Class imas.DBEntry
        time: float=-99.0
            Specific time[s] for one timeslice validation
        fmt: str=""
            Output format, "log" with logging, otherwise with print() function

        Returns
        -------
        """

        ids_oc = available_in_dbentry(db)
        logger.debug(f"ids_oc= {ids_oc}")
        ret = {}

        for idsname, occ in ids_oc:
            d = self.validate(db, idsname, occ=occ, time=time, fmt=fmt)
            ret.update(d)

        return ret


# ----------------------------------------------------------------------


def db_validator(
    user="public",
    database="ITER",
    version="3",
    backend="MDSPLUS",
    schema_path=[],
    pulse=[],
):
    """
    Function that validates scenarios in IMAS database

    Parameters
    ---------
    user: str="public"
        Status of user: either public or local. A public user should just be left as public,
        whereas a local user should write their proper i    dentifier
    database: str="ITER"
        Name of database where the data is harbored
    version: str="3"
        String of number of data version
    backend: str="MDSPLUS"
        Name of backend format
    schema_path: list=[]
        List of shcema file paths in str
    pulse: list=[]
        List of pulses in tuple as (shot, run)
    Returns
    -------

    """

    logger.info("loading schema...")

    schema = []
    if not schema_path:
        # Load default validation schema in case of "schema_path" not given
        current_fpath = path.dirname(path.realpath(__file__))
        schema_dir = path.join(current_fpath, "../../../../bin/validation_schemas")
        if path.isdir(schema_dir):
            schema += sorted(glob(schema_dir + "/generic/*.y*ml", recursive=True))
            schema += sorted(glob(schema_dir + "/ITER/*.y*ml", recursive=True))
    else:
        for p in schema_path:
            if path.isdir(p):
                # Find yaml files in the dir recursively
                schema.extend(sorted(glob(p + "/**/*.y*ml", recursive=True)))
            elif path.isfile(p):
                # Add the path if found
                schema.append(p)

    if len(schema) < 1:
        raise OSError(f"not found schema: {schema_path}")

    # Initialize Scenario Validator
    sv = ScenarioValidator(schema_path=schema)

    pulses = []
    if len(pulse) >= 1:
        for shot, run in pulse:
            if shot > 0 and run >= 0:
                pulses.extend([(shot, run)])
            if shot > 0 and run < 0:
                scenarios = load_scenario(user, database, version, backend)
                pulses.extend([(s, r) for s, r in scenarios if shot == s])
    else:
        pulses = load_scenario(user, database, version, backend)

    # Scenario Validation for Pulses
    npulse = len(pulses)
    for i, (shot, run) in enumerate(pulses):
        db = imas.DBEntry(get_backend_id(backend), database, shot, run, user)
        status, _ = db.open()
        if status != 0:
            raise OSError(
                f"can not open backend={backend}, user_or_path={user}, database={database}, shot={shot}, run={run}"
            )

        logger.info("-----------------------------------------------------------")
        logger.info(f"{i+1}/{npulse} ({(i+1)//npulse*100}%) {shot}/{run}")
        logger.info("-----------------------------------------------------------")

        # Scenario Validation
        sv.validate_db(db, fmt="log")


# ----------------------------------------------------------------------
