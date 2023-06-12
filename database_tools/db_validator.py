#!/usr/bin/env python
from os import path, getenv
from glob import glob
import logging
import inspect

import imas
from database_tools import db_helpers
from database_tools import idschk
from idstools.idslist import available_in_dbentry
from idstools.cli import get_backend_id


logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------


def load_scenario(user, database, version, backend):
    """
    Return a list of pulses as tuple (shot,run) by using database_tools.db_helper

    Parameters
    ----------
    user: str="public"
        Status of user: either public or local. A public user should just be left as public, whereas a local user should write their proper i    dentifier
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

    scenarios = []
    if backend == "MDSPLUS":
        scenarios = db_helpers.mdsListPulseRun(
            db_helpers.getDBPath(user, database, version), with_status="active"
        )
    elif backend == "HDF5":
        scenarios = db_helpers.hdf5ListPulseRun(
            db_helpers.getDBPath(user, database, version)
        )

    return scenarios


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

    DD = {}
    SCHEMA = {}
    SCHEMA_PATH = []

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

        ScenarioValidator.DD or self.load_DD(dd_path)

        if schema_path != ScenarioValidator.SCHEMA_PATH:
            self.load_schema(schema_path)
            ScenarioValidator.SCHEMA_PATH = schema_path

    def load_DD(self, fpath):
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
            self.DD = idschk.load_XML(fpath)
        except:
            raise OSError(f"can not load DD: {fpath}")

        logger.debug(f" DD= {fpath}")
        logger.debug(f" self.DD= {self.DD}")

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
                self.SCHEMA[f] = idschk.load_YAML(f)
        except:
            raise OSError(f"failed to load Schema: {yaml}")

        logger.debug(f" schema file= {f}")
        logger.debug(f" schema = {self.SCHEMA}")

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

        dd0 = [dd for dd in self.DD if dd.get("name") == idsname][0]
        ret = {}
        for fpath, schemas in self.SCHEMA.items():
            for key, schema in schemas.items():
                if key == idsname:
                    #
                    try:
                        logger.info(
                            "- {}/{}/{}/{} < {}".format(
                                db.__dict__["shot"],
                                db.__dict__["run"],
                                idsname,
                                occ,
                                path.relpath(fpath),
                            )
                        )
                        idstime = db.partial_get(idsname, "time", occurrence=occ)
                        #
                        if (time < 0.0) or (idstime is None):
                            ids = db.get(idsname, occurrence=occ)
                        else:
                            tm, itm = find_time(idstime, time)
                            ids = db.get_slice(idsname, tm, 1, occurrence=occ)
                    except Exception as e:
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
                            logger.error(
                                "\n{}".format(idschk.dict_to_yaml(dout))
                            )
                    else:
                        print(idschk.dict_to_yaml(dout))
                    #
                    ret[ids.__name__+"/"+str(occ)] = flag
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

        for (idsname, occ) in ids_oc:
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
        Status of user: either public or local. A public user should just be left as public, whereas a local user should write their proper i    dentifier
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
            schema_ITER = sorted(glob(schema_dir + "/ITER/*.y*ml", recursive=True))
            schema_generic = sorted(glob(schema_dir + "/generic/*.y*ml", recursive=True))
            # Avoid Duplication of Schema Files
            w = [path.basename(f) for f in schema_ITER]
            schema_ITER += [f for f in schema_generic if path.basename(f) not in w]
            schema = schema_ITER
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

    # Load scenario table in case of "pulse" not given
    logger.info("loading scenario table...")
    scenarios = load_scenario(user, database, version, backend)
    pulses = []
    if len(pulse) >= 1:
        for shot, run in pulse:
            if shot > 0 and run >= 0:
                pulses.extend([(shot, run)])
            if shot > 0 and run < 0:
                pulses.extend([(s, r) for s, r in scenarios if shot == s])
    else:
        pulses = scenarios

    # Scenario Validation for Pulses
    npulse = len(pulses)
    for i, (shot, run) in enumerate(pulses):

        db = imas.DBEntry(get_backend_id(backend), database, shot, run, user)
        status, _ = db.open()
        if status != 0:
            raise OSError(
                f"can not open backend={backend}, user_or_path={user}, database={database}, shot={shot}, run={run}"
            )

        logger.info(f"-----------------------------------------------------------")
        logger.info(f"{i+1}/{npulse} ({(i+1)//npulse*100}%) {shot}/{run}")
        logger.info(f"-----------------------------------------------------------")

        # Scenario Validation
        sv.validate_db(db, fmt="log")


# ----------------------------------------------------------------------
