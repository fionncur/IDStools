#!/usr/bin/env python

import copy
import logging
import os
import re
from os import path
from pathlib import Path
from sys import exit
from xml.etree import ElementTree as ET

import cerberus

try:
    import imaspy as imas
except ImportError:
    import imas
import numpy as np
import yaml

from idstools.cocos import COCOS, IDS_COCOS, compute_COCOS

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------

# Global Constants
imas_prefix = Path(os.environ["IMAS_PREFIX"]).resolve()
FILE_IDSDef = str(imas_prefix / "include" / "IDSDef.xml")
TARGET_TAG = "IDS"
ids_header = "ids."
idx_header = "idx."
args_verbose = False
args_check_all = True


# Initialization for yaml Dumper
yaml.Dumper.ignore_aliases = lambda *args: True

# Validation Schema for COCOS using IDS/equilibrium
required_fields_eq = {
    "ids.ids_properties.homogeneous_time": {"min": 0, "max": 2},
    "ids.time_slice": {"minlength": 1},
    "ids.time_slice[itime].global_quantities.ip": {
        "ids_gt": imas.ids_defs.EMPTY_FLOAT,
    },
    "ids.vacuum_toroidal_field.b0": {
        "empty": False,
    },
    "ids.time_slice[itime].profiles_1d.psi": {
        "empty": False,
    },
    "ids.time_slice[itime].profiles_1d.q": {
        "empty": False,
    },
    "ids.time_slice[itime].profiles_1d.dpressure_dpsi": {
        "empty": False,
    },
    "ids.time_slice[itime].profiles_2d": {"minlength": 1},
    "ids.time_slice[itime].profiles_2d[i1].b_field_z": {
        "empty": False,
    },
    "ids.time_slice[itime].profiles_2d[i1].psi": {
        "empty": False,
    },
    "ids.time_slice[itime].profiles_2d[i1].r": {
        "empty": False,
        "ids_gt": 0.0,
    },
}

required_fields_cocos = {
    "ids.ids_properties.homogeneous_time": {"min": 0, "max": 2},
    "ids.time_slice": {"minlength": 1},
    "ids.time_slice[itime].global_quantities.ip": {"ids_ip_like": False},
    "ids.vacuum_toroidal_field.b0": {"ids_b0_like": False},
    "ids.time_slice[itime].profiles_1d.psi": {"ids_psi_like": False},
    "ids.time_slice[itime].profiles_1d.q": {"ids_q_like": False},
    "ids.time_slice[itime].profiles_1d.dpressure_dpsi": {"ids_dPdpsi_like": False},
}

# Default Validation Schema
default_schema = {
    "ids_nan": False,
    "ids_inf": False,
}

# ----------------------------------------------------------------------


# FUNCTION TO FIND THE INDEX OF THE DESIRED TIME SLICE IN THE TIME ARRAY
def find_nearest(a, a0):
    """
    Element in ndarray 'a' closest to the scalar value 'a0'

    Attributes
    ----------
    a: numpy.ndarray
        A list or array of values
    a0: float
        The value to find a close value and its index in the ndarray given

    Returns
    -------
    tuple
        A tuple containing a value and its index in the ndarray given
    """

    idx = np.abs(a - a0).argmin()
    return a.flat[idx], idx


def find_time(timevec, time):
    """
    Return time slice and its index in time vector

    Attributes
    ----------
    timevec: numpy.ndarray
        A list or array of time values
    time: float
        The time value to search for in the time vector

    Returns
    -------
    tuple
        A tuple containing the time slice and its index in the time vector
    """

    if len(timevec) > 1:
        if time >= 0:
            [tc, it] = find_nearest(timevec, time)
        else:
            it = len(timevec) // 2
            tc = timevec[it]
    else:
        if len(timevec) > 0:
            tc = timevec[0]
        else:
            tc = 0
        it = 0
    time = tc

    return time, it


# ----------------------------------------------------------------------


def path2py(p, rm_last_bracket=False, header=False, idx=None):
    """Substitute IDS Path to Python Expression

    Parameters
    ----------
    p: str
        Field path
    rm_last_bracket: boolean
        Flag to remove last bracket from the path
    header: str
        Additional header preceding to the path
    idx: IdxDict=None
        DD Sub-Indices (e.g. itime, i1, ..., etc.)

    Returns
    -------
    p: str
        Field path in Python
    """

    result = re.search("^(\\d)\\.\\.\\.(\\d)$", p)
    if result is not None:  # constant coordinate definition (e.g. 1...3)
        return "range(" + str(result.group(2)) + ")"

    else:  # other coordinate definition
        if rm_last_bracket:
            p = p[: p.rfind("(")]
        p = re.sub("\\((\\w+)\\)", r"(" + idx_header + "\\1)", p)
        p = p.replace("/", ".")
        p = p.replace("(", "[")
        p = p.replace(")", "]")

        if idx is not None:
            keys = idx.__dict__.keys()
            for k in keys:
                s = idx_header + k
                p = p.replace(s, str(eval(s)))

        if header:
            return ids_header + p
        else:
            return p


# ----------------------------------------------------------------------


class idx_dict(dict):
    """
    Class for DD Sub-Indices (e.g. itime, i1, ..., etc.).

    Subscripts are stored as instance attributes with None as initial values.
    """

    def __init__(self, p):
        """
        Initialize idx_dict from a field path.

        Parameters
        ----------
        p : str
            Field path string containing subscript identifiers in parentheses
        """

        # idict = []

        for m in re.finditer("\\((\\w+)\\)", p):  # find subscripts and set as attribute
            it = m.group()[1:-1]
            setattr(self, it, None)  # initial value = None


# ----------------------------------------------------------------------


class IDSValidator(cerberus.Validator):
    """
    Cerberus-Validator extended with custom rules for IDS

    """

    ids = None
    idx = None
    cocos = {}
    # shape = []
    # coord = []
    ndim = None

    def __init__(self, *args, **kwargs):
        """ """
        # assign configuration value to instance property
        # self.ids = kwargs.get("ids")
        # self.idx = kwargs.get("idx")

        # pass all data to the base classes
        super(IDSValidator, self).__init__(*args, **kwargs)

    def set_ids(self, ids):
        """ """
        self.ids = ids

    def set_idx(self, idx):
        """ """
        self.idx = idx

    def set_cocos(self, cocos):
        """ """
        self.cocos = cocos

    def set_dim(self, field, ids, data):
        """ """
        dtype = re.search("^(INT|FLT)_([1-9])D$", field.get("data_type"))
        if dtype is not None:
            self.shape = []
            self.coord = []
            self.ndim = int(dtype.group(2))
            #
            for i in range(data.ndim):
                c = path2py(field.get("coordinate" + str(i + 1)), header=True)
                # homogeneous_time = ids.ids_properties.homogeneous_time
                #
                if re.search("1\\.\\.\\.", c):
                    lcrd = data.shape[i]
                else:
                    try:
                        crd = eval(c)
                        lcrd = len(crd)
                    except Exception as e:
                        logger.debug(f"{e}")
                        lcrd = -1

                self.shape.append(lcrd)
                self.coord.append(c)

    def _validate_ids_nan(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            if np.any(np.isnan(v)):
                if not constraint:
                    self._error(field, "Found nan")
        except TypeError:
            pass

    def _validate_ids_inf(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            if np.any(np.isinf(v)):
                if not constraint:
                    self._error(field, "Found inf")
        except TypeError:
            pass

    def _validate_ids_le(self, max_value, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            if np.any(v > max_value):
                self._error(field, f"Must be smaller than {max_value}")
        except ValueError:
            pass

    def _validate_ids_ge(self, min_value, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            if np.any(v < min_value):
                self._error(field, f"Must be larger than {min_value}")
        except ValueError:
            pass

    def _validate_ids_lt(self, max_value, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            if np.any(v >= max_value):
                self._error(field, f"Must be smaller than {max_value}")
        except ValueError:
            pass

    def _validate_ids_gt(self, min_value, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            if isinstance(min_value, str):
                min_value = eval(min_value)
            if np.any(v <= min_value):
                self._error(field, f"Must be larger than {min_value}")
        except ValueError:
            pass

    def _validate_ids_psi_like(self, constraint, field, value):
        """{'nullable': False }"""
        if (value.ndim != 1) or (value.size < 2):
            self._error(field, "ndim is expected as 1, and size as greater than 1")
            return
        else:
            try:
                v = np.atleast_1d(value).flatten()
                psi_like = self.cocos["sigma_Ip"] * self.cocos["sigma_Bp"]
                if np.sign(v[-1] - v[0]) != psi_like:
                    if not constraint:
                        self._error(field, f"Sign expected as {psi_like}")
            except ValueError:
                pass

    def _validate_ids_b0_like(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            b0_like = self.cocos["sigma_B0"]
            if np.any(np.sign(v) != b0_like):
                if not constraint:
                    self._error(field, f"Sign expected as {b0_like}")
        except ValueError:
            pass

    def _validate_ids_dodpsi_like(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            dodpsi_like = -self.cocos["sigma_Ip"] * self.cocos["sigma_Bp"]
            if np.any(np.sign(v) != dodpsi_like):
                if not constraint:
                    self._error(field, f"Sign expected as {dodpsi_like}")
        except ValueError:
            pass

    def _validate_ids_q_like(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            q_like = self.cocos["sigma_Ip"] * self.cocos["sigma_B0"] * self.cocos["sigma_rhothetaphi"]
            if np.any(np.sign(v) != q_like):
                if not constraint:
                    self._error(field, f"Sign expected as {q_like}")
        except ValueError:
            pass

    def _validate_ids_ip_like(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            ip_like = self.cocos["sigma_Ip"]
            if any(np.sign(v) != ip_like):
                if not constraint:
                    self._error(field, f"Sign expected as {ip_like}")
        except ValueError:
            pass

    def _validate_ids_d_pdpsi_like(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            dodpsi_like = -self.cocos["sigma_Ip"] * self.cocos["sigma_Bp"]
            if np.sign(np.sum(np.sign(v))) != dodpsi_like:
                if not constraint:
                    self._error(field, f"avg(Sign) expected as {dodpsi_like}")
        except ValueError:
            pass

    def _validate_ids_dim(self, constraint, field, value):
        """{'nullable': False }"""
        if value.size > 0:
            try:
                for i in range(len(self.shape)):
                    if self.shape[i] != value.shape[i]:
                        if not constraint:
                            msg = "size of coordinate{}|{} = {}, expected as {}".format(
                                str(i + 1), self.coord[i], value.shape[i], self.shape[i]
                            )
                            self._error(field, msg)
            except ValueError:
                pass

    def _validate_ids_bool(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            if not np.all(constraint):
                self._error(field, "false boolean expression")
        except ValueError:
            pass

    def _validate_ids_eq(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            if value != constraint:
                self._error(field, f"Must be equal to {constraint}")
        except ValueError:
            pass

    def _validate_ids_cocos(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            if self.ids.__name__ == "equilibrium":
                val = compute_COCOS(self.ids, self.idx.itime, self.idx.i1)
                if val["COCOS"] != constraint:
                    msg = f"COCOS computed {val['COCOS']}, expected as {constraint}"
                    self._error(field, msg)
        except ValueError:
            pass


# ----------------------------------------------------------------------


def validator(field, path_doc, ids, schema, cocos, buf, idx):
    """Check the consistency of IDS quantities w.r.t. Schema and COCOS

    Parameters
    ----------
    field: Element
        Sub-elements in an IDS
    path_doc: str
        Field path
    ids: IDS
        IDS for validation
    schema: dict
        Cerberus schema loaded as type dict
    cocos: COCOS
        COCOS input for validation
    buf: dict
        Result of validation for logging
    idx: IdxDict=None
        DD Sub-Indices (e.g. itime, i1, ..., etc.)

    Returns
    -------
    remark: boolean
    """

    # data_size = 0

    p = path2py(path_doc, header=True)

    # eval for target data
    try:
        data = eval(p)
    except Exception as e:
        logger.debug(f"{e}")
        print(f"eval error on key {p}, skipped")
        return

    # add default schema
    if schema[path_doc]:
        schema[path_doc].update(default_schema)
    else:
        schema[path_doc] = default_schema
    schemaw = copy.deepcopy(schema)

    # eval for schema value in case of validation between data
    for key, value in schema[path_doc].items():
        if isinstance(value, str):
            val = re.sub("_(i+\\w+)_", idx_header + r"\1", value)
            val = val.replace(ids.__name__ + ".", ids_header)
            try:
                schemaw[path_doc][key] = eval(val)
            except Exception as e:
                logger.debug(f"{e}")
                # print(f"eval error on value {val}, ignored: {e}")
                # return
                pass

    # Initialization
    v_ids = IDSValidator({path_doc: schemaw[path_doc]})
    v_ids.set_dim(field, ids, data)
    v_ids.set_cocos(cocos)
    v_ids.set_ids(ids)
    v_ids.set_idx(idx)

    # Validation
    d = {path_doc: data}
    remark = v_ids.validate(d)
    errors = v_ids.errors

    # Report
    if args_verbose:
        report = {}
        report["remark"] = remark
        report["errors"] = errors
        buf.update({path2py(path_doc, idx=idx): report})
    else:
        if not remark:
            buf.update({path2py(path_doc, idx=idx): errors[list(errors)[0]]})

    # Result
    return remark


# ----------------------------------------------------------------------


def path_iterator(field, nodes, ids, schema, cocos, buf, idx=None, level=0):
    """Iterate Recursively over Sub-Indices of IDS Path (e.g. itime, i1, ..., etc.)

    Parameters
    ----------
    field: Element
        Sub-elements in an IDS
    nodes: list
        Name of nodes consisting path_doc (field)
    ids: IDS
        IDS for validation
    schema: dict
        Cerberus schema loaded as type dict
    cocos: COCOS
        COCOS input for validation
    buf: dict
        Result of validation for logging
    idx: IdxDict=None
        DD Sub-Indices (e.g. itime, i1, ..., etc.)
    level: int=0
        Depth of node in target field
    """

    p = "/".join(nodes[: level + 1])
    if level < len(nodes) - 1:
        result = re.search("(\\w+)(\\(\\w+\\))$", p)

        # for dynamic array (e.g. path(itime)/to(i1)/array(i2))
        if result is not None:
            try:
                wk = eval(path2py(p, rm_last_bracket=True, header=True, idx=idx))
                for i in range(len(wk)):
                    idxname = result.group(2)[1:-1]
                    # increment the index
                    idx.__dict__[idxname] = i
                    path_iterator(
                        field,
                        nodes,
                        ids,
                        schema,
                        cocos,
                        buf,
                        idx=idx,
                        level=level + 1,
                    )
                    if not args_check_all:
                        break
            except Exception as e:
                logger.debug(f"{e}")
                print(f"Error at calling path_iterator: {e}")

        # for node (e.g. path(itime)/to(i1)/node)
        else:
            path_iterator(field, nodes, ids, schema, cocos, buf, idx=idx, level=level + 1)

    else:
        validator(field, p, ids, schema, cocos, buf, idx)


# ----------------------------------------------------------------------


def validate_COCOS(ids, schema, itime, i1, cocos=None):
    """Compute COCOS values using stored data in IDS/equilibrium

    Parameters
    ----------
    ids: IDS
        IDS for COCOS estimation
    schema: dict
        Cerberus schema loaded as type dict
    itime: int|None
        Index of struct_array time_slice in IDS/equilibrium
    i1: int=0
        Index of struct_array profiles_2d in IDS/equilibrium
    cocos: COCOS=None
        Validate IDS wrt COCOS if given

    Returns
    -------
    cocos: COCOS
    """

    # Inter-COCOS Validation
    for key, value in schema.items():
        v_ids = IDSValidator({key: value})
        if cocos is not None:
            v_ids.cocos = cocos

        try:
            data = eval(key)
        except Exception as e:
            logger.debug(f"{e}")
            print(f"eval error on key {key}")
            return

        remark = v_ids.validate({key: data})
        errors = v_ids.errors
        if not remark:
            raise ValueError(errors)
            # return
            pass


# ----------------------------------------------------------------------


def dict_to_yaml(din):
    """Transform python dictionary to string in yaml

    Parameters
    ----------
    din: dict
       dict to be transformed to yaml string

    Returns
    -------
    yaml.dump: str
       string in yaml format
    """

    return yaml.dump(
        din,
        indent=4,
        default_flow_style=False,
        sort_keys=False,
        width=float("inf"),
    )


# ----------------------------------------------------------------------


def load_xml(fpath):
    """Read XML file and Retrun as ElementTree

    Parameters
    ----------
    fpath: str
        Path to XML file

    Returns
    -------
    root: ElementTree
    """

    # Load IMAS-DD File
    if path.isfile(fpath):
        root = ET.parse(fpath).getroot()
    else:
        exit(f"file not found:{fpath}")

    return root


# ----------------------------------------------------------------------


def load_yaml(fpath):
    """Read YAML file and Retrun as dictionary

    Parameters
    ----------
    fpath: str
        Path to YAML file

    Returns
    -------
    d: dict
    """

    # Load Schema File
    try:
        f = open(fpath, mode="r")
    except Exception as e:
        logger.debug(f"{e}")
        exit(f"can not open file:{fpath}")
    try:
        d = yaml.safe_load(f)
    except Exception as e:
        logger.debug(f"{e}")
        exit(f"invalid yaml in:{fpath}")

    return d


# ----------------------------------------------------------------------


def load_dd(idsname):
    """Return Data Dictionary (DD)

    Parameters
    ----------
    idsname: str
        IDS name

    Returns
    -------
    dd: class Element
        DD correspoinding to idsname
    """

    root = load_xml(FILE_IDSDef)
    dd = [dd for dd in root if dd.get("name") == idsname][0]

    return dd


# ----------------------------------------------------------------------


def eval_idss(s):
    """Return True if IDSs validate

    Parameters
    ----------
    s: str
        input string in YAML

    Returns
    -------
    flag: boolean
    """

    flag = True
    if s:
        d_ids = yaml.safe_load(s)
        # 1st level for IDSs
        for k_ids, d_occ in d_ids.items():
            # 2nd level for occurences
            for k_occ, val in d_occ.items():
                # 3rd level
                if args_verbose:
                    if not (val["remark"]):
                        flag = False
                        break
                else:
                    if val:
                        flag = False
                        break
            if not flag:
                break
    else:
        flag = False

    return flag


# ----------------------------------------------------------------------


def ids_iterator(ids, schema, dd, cocos, occ=0):
    """Iterate over the occurences and fields

    Parameters
    ----------
    ids: IDS
        IDS for validation
    schema: dict
        Cerberus schema loaded as type dict
    dd: Element=None
        Data Dictionary as class Element (read IDSDef.xml if None)
    cocos: COCOS
        COCOS input for validation
    occ: int=0
        IDS occurence

    Returns
    -------
    dict
        Result of validation in type dict
    """

    idsname = ids.__name__
    maxoc = ids.getMaxOccurrences()
    buf = {}
    dictw = {}

    # Initialization of IDS Occurrence
    if isinstance(occ, int):
        if occ in range(maxoc):
            range_oc = [occ]
        else:
            exit(f"value error:{occ}")
    else:
        exit(f"type error:{occ}")

    for oc in range_oc:
        report_buf = {}
        idsprop = ids.ids_properties
        homogeneous_time = idsprop.homogeneous_time
        if args_verbose:
            dictw = {
                "remark": None,
                "ids_properties": {
                    "homogeneous_time": homogeneous_time,
                    "data_dictionary": idsprop.version_put.data_dictionary,
                    "access_layer": idsprop.version_put.access_layer,
                    "access_layer_language": idsprop.version_put.access_layer_language,
                },
            }

        if homogeneous_time in [0, 1, 2]:
            for field in dd.iter("field"):
                path = field.get("path_doc")
                if path in schema[idsname]:
                    nodes = path.split("/")
                    path_iterator(
                        field,
                        nodes,
                        ids,
                        schema[idsname],
                        cocos,
                        report_buf,
                        idx=idx_dict(path),
                    )

            if args_verbose:
                if bool(report_buf):
                    dictw["remark"] = all({report_buf[x]["remark"] for x in report_buf.keys()})
            dictw.update(report_buf)
            buf.update({"occurence(" + str(oc) + ")": dictw})

    return {idsname: buf}


# ----------------------------------------------------------------------


def init_schema_coordinate(idsname, dd=None, rule={"ids_dim": False}):
    """Return validation schema and Data Dictionary (DD)

    Parameters
    ----------
    idsname: str
        Name of IDS for validation
    dd: class Element
        DD input
    rule: dict = {ids_dim:False}
        Cerberus validation rule in type dict

    Returns
    -------
    schema: dict
        validation schema for ids_validator
    ddo: class Element
        DD output
    """

    d = {}

    if ET.iselement(dd):
        ddo = dd
    elif dd is None:
        ddo = load_dd(idsname)
    else:
        exit("type error:{}".format(dd))

    for field in ddo.iter():
        data_type = field.attrib.get("data_type")
        path_doc = field.attrib.get("path_doc")

        # validate for data_type = INT_*D and FLT_*D
        if data_type and re.search("^(INT|FLT)_([1-9])D$", data_type) is not None:

            # skip validation for error_upper and error_lower
            if re.search("_error_(upper|lower)", path_doc) is None:
                d[path_doc] = rule

    schema = {idsname: d}

    return schema, ddo


# ----------------------------------------------------------------------


def ids_validator(ids, schema, dd=None, occ=0, ipsign=-1, b0sign=-1, verbose=False, check_all=True):
    """Function Interface for IDS Validation w.r.t. DD (IDSDef.xml)

    Parameters
    ----------
    ids: IDS
        IDS for validation
    schema: dict | str
        1. dict: Cerberus schema loaded as type dict
        2. str: File path to Cerberus schema
    dd: Element=None
        Data Dictionary as class Element (read IDSDef.xml if None)
    occ: int=0
        IDS occurence
    ipsign: int=-1
        Sign of Ip
    b0sign: int=-1
        Sign of B0
    verbose: boolean=False
        Verbosity
    check_all: boolean=True
        Check all fields

    Returns
    -------
    eval_IDSs(dump): boolean
        Validation result in type boolean
    out: dict
        Validation result in type dict
    """

    # Schema Initialization
    if isinstance(schema, dict):
        pass
    elif isinstance(schema, str):
        schema = load_yaml(schema)
    else:
        exit(f"type error:{schema}")

    # DD Initialization for Target IDS
    if ET.iselement(dd):
        pass
    elif dd is None:
        dd = load_dd(ids.__name__)
    else:
        exit(f"type error:{dd}")

    # COCOS Initialization
    index = {"COCOS": IDS_COCOS, "ipsign": ipsign, "b0sign": b0sign}
    cocos = COCOS(index=index).get()

    # Check all fields if check_all = True
    global args_verbose, args_check_all
    args_verbose = verbose
    args_check_all = check_all

    # Check for Target IDS
    out = {}
    if ids.__name__ in schema:
        out = ids_iterator(ids, schema, dd, cocos, occ=occ)

    return eval_idss(dict_to_yaml(out)), out


# ----------------------------------------------------------------------


def ids_coordinate_check(ids, verbose=False):
    """Function Interface for IDS Validation on Coordinate

    Parameters
    ----------
    ids: IDS
        IDS for validation
    verbose: boolean=False
        Increase output verbosity if true

    Returns
    -------
    flag: boolean
        Validation result in type boolean
    out: dict
        Validation result in type dict
    """

    schema, dd = init_schema_coordinate(ids.__name__)
    flag, out = ids_validator(ids, schema, dd=dd, verbose=False)
    if verbose:
        print(dict_to_yaml(out))
    return flag, out


# ----------------------------------------------------------------------


def ids_cocos_check(ids, itime=None, i1=0, verbose=False):
    """Function Interface for IDS Validation on COCOS

    Parameters
    ----------
    ids: IDS
        IDS for validation
    itime: int|None
        Index of struct_array time_slice in IDS/equilibrium
    i1: int=0
        Index of struct_array profiles_2d in IDS/equilibrium
    verbose: boolean=False
        Increase output verbosity if true

    Returns
    -------
    remark: boolean
        Validation result in type boolean
    error: dict
        Validation result in type dict
    """

    remark = False
    error = {}
    key = "COCOS"

    if ids.__name__ == "equilibrium":
        try:
            cocos = compute_COCOS(ids, itime, i1)
        except Exception as e:
            logger.debug(f"{e}")
            exit(f"Cannot compute COCOS: {e}")
        # set remark
        if cocos[key] == IDS_COCOS:
            remark = True
        # set error
        if verbose:
            error = {key: cocos}
            print(dict_to_yaml(error))
        else:
            error = {key: cocos[key]}
    else:
        exit(f"equilibrium instead of {ids.__name__}")

    return remark, error


# ----------------------------------------------------------------------
