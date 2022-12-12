#!/usr/bin/env python
from os import getenv, path
from sys import exit
import re
import argparse
import numpy as np
import cerberus
import yaml
from xml.etree import ElementTree as ET
import imas


IMAS_PREFIX = "IMAS_PREFIX"
FILE_IDSDef = getenv(IMAS_PREFIX) + "/include/IDSDef.xml"
TARGET_TAG = "IDS"
report_buf = {}
ids_header = "ids."
idx_header = "idx."
IDS_COCOS = 11
args_verbose = False
args_check_all = True

# Initialization for yaml Dumper
yaml.Dumper.ignore_aliases = lambda *args: True

# Validation Schema for COCOS using IDS/equilibrium
required_fields_eq = {
    "ids.ids_properties.homogeneous_time": {"min": 0, "max": 2},
    "ids.time_slice": {"minlength": 1},
    "ids.time_slice[itime].global_quantities.ip": {
        "empty": False,
        "ids_gt": -9e40,
        "ids_nan": False,
        "ids_inf": False,
    },
    "ids.vacuum_toroidal_field.b0": {
        "empty": False,
        "ids_nan": False,
        "ids_inf": False,
    },
    "ids.time_slice[itime].profiles_1d.psi": {
        "empty": False,
        "ids_nan": False,
        "ids_inf": False,
    },
    "ids.time_slice[itime].profiles_1d.q": {
        "empty": False,
        "ids_nan": False,
        "ids_inf": False,
    },
    "ids.time_slice[itime].profiles_1d.dpressure_dpsi": {
        "empty": False,
        "ids_nan": False,
        "ids_inf": False,
    },
    "ids.time_slice[itime].profiles_2d": {"minlength": 1},
    "ids.time_slice[itime].profiles_2d[0].b_field_z": {
        "empty": False,
        "ids_nan": False,
        "ids_inf": False,
    },
    "ids.time_slice[itime].profiles_2d[0].psi": {
        "empty": False,
        "ids_nan": False,
        "ids_inf": False,
    },
    "ids.time_slice[itime].profiles_2d[0].r": {
        "empty": False,
        "ids_nan": False,
        "ids_inf": False,
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


# ----------------------------------------------------------------------


# FUNCTION TO FIND THE INDEX OF THE DESIRED TIME SLICE IN THE TIME ARRAY
def find_nearest(a, a0):
    """
    Element in nd array 'a' closest to the scalar value 'a0'
    """

    idx = np.abs(a - a0).argmin()
    return a.flat[idx], idx


def find_time(timevec, time):
    """
    Return time slice and its index in time vector
    """

    if len(timevec) > 1:
        if time >= 0:
            [tc, it] = find_nearest(timevec, time)
        else:
            it = int(len(timevec) / 2)
            tc = timevec[it]
        time = tc
    else:
        if len(timevec) > 0:
            tc = timevec[0]
        else:
            tc = 0
        it = 0
        time = tc

    return time, it


# ----------------------------------------------------------------------


class COCOS:
    """
    COCOS module in Python

    [1] O. Sauter and S.Yu. Medvevdev, "Tokamak Coordinate Conventions : COCOS",
        Comput. Physics Commun. 184 (2013) 293
    [2] cocos_module.f90 (CHEASE)

    Attributes
    ----------
    COCOS: int
    sigma_Ip: int
    sigma_B0: int
    exp_Bp: int
    sigma_Bp: int
    sigma_RphiZ: int
    sigma_rhothetaphi: int
    sign_q_pos: int
    sign_pprime_pos: int
    theta_sign_clockwise: int
    """

    def __init__(self, index=None, values=None):
        """
        Initialize COCOS index using values, or values using COCOS index

        Parameters
        ----------
        index: dict=None
            COCOS index with signs of Ip and B0, e.g. index={"COCOS": 11}
        values: dict=None
            COCOS values
        """

        if (index is None) and (values is None):
            raise ValueError(
                "Initialize COCOS with either index or values: both not given"
            )
            return

        elif (index is not None) and (values is not None):
            raise ValueError("Initialize COCOS with either index or values: both given")
            return

        # in case of init. by index
        elif index is not None:

            COCOS = index["COCOS"]
            #
            # Parameters from Table I
            #
            if COCOS in [1, 11]:
                # ITER, Boozer are cocos=11
                val = (+1, +1, +1, +1, -1)
            elif COCOS in [2, 12]:
                # CHEASE, ONETWO, Hinton-Hazeltine, LION is cocos=2
                val = (+1, -1, +1, +1, -1)
            elif COCOS in [3, 13]:
                # Freidberg, CAXE, KINX are cocos=3
                # EU-ITM up to end of 2011 is COCOS=13
                val = (-1, +1, -1, -1, +1)
            elif COCOS in [4, 14]:
                #
                val = (-1, -1, -1, -1, +1)
            elif COCOS in [5, 15]:
                #
                val = (+1, +1, -1, -1, -1)
            elif COCOS in [6, 16]:
                #
                val = (+1, -1, -1, -1, -1)
            elif COCOS in [7, 17]:
                # TCV psitbx is cocos=7
                val = (-1, +1, +1, +1, +1)
            elif COCOS in [8, 18]:
                #
                val = (-1, -1, +1, +1, +1)
            else:
                # Should not be here since all cases defined
                raise ValueError("error: COCOS = {} does not exist".format(COCOS))
                return

            (
                sigma_Bp,
                sigma_RphiZ,
                sigma_rhothetaphi,
                sign_q_pos,
                sign_pprime_pos,
            ) = val

            # cocos=i or 10+i have similar coordinate conventions except psi/2pi for
            # cocos=i and psi for cocos=10+i

            if COCOS >= 11:
                exp_Bp = 1
            else:
                exp_Bp = 0

            theta_sign_clockwise = sigma_RphiZ * sigma_rhothetaphi

            self.COCOS = COCOS
            self.exp_Bp = exp_Bp
            self.sigma_Bp = sigma_Bp
            self.sigma_RphiZ = sigma_RphiZ
            self.sigma_rhothetaphi = sigma_rhothetaphi
            self.sign_q_pos = sign_q_pos
            self.sign_pprime_pos = sign_pprime_pos
            self.theta_sign_clockwise = theta_sign_clockwise

        # in case of init. by values
        else:

            exp_Bp = values["exp_Bp"]
            sigma_Bp = values["sigma_Bp"]
            sigma_RphiZ = values["sigma_RphiZ"]
            sigma_rhothetaphi = values["sigma_rhothetaphi"]
            sign_q_pos = values["sign_q_pos"]
            sign_pprime_pos = values["sign_pprime_pos"]

            val = (
                sigma_Bp,
                sigma_RphiZ,
                sigma_rhothetaphi,
                sign_q_pos,
                sign_pprime_pos,
            )

            #
            # Parameters from Table I
            #
            if val == (+1, +1, +1, +1, -1):
                # ITER, Boozer are cocos=11
                COCOS = [1, 11]
            elif val == (+1, -1, +1, +1, -1):
                # CHEASE, ONETWO, Hinton-Hazeltine, LION is cocos=2
                COCOS = [2, 12]
            elif val == (-1, +1, -1, -1, +1):
                # Freidberg, CAXE, KINX are cocos=3
                # EU-ITM up to end of 2011 is COCOS=13
                COCOS = [3, 13]
            elif val == (-1, -1, -1, -1, +1):
                #
                COCOS = [4, 14]
            elif val == (+1, +1, -1, -1, -1):
                #
                COCOS = [5, 15]
            elif val == (+1, -1, -1, -1, -1):
                #
                COCOS = [6, 16]
            elif val == (-1, +1, +1, +1, +1):
                #
                COCOS = [7, 17]
            elif val == (-1, -1, +1, +1, +1):
                #
                COCOS = [8, 18]
            else:
                # Should not be here since all cases defined
                raise ValueError("error: COCOS Values not match {}".format(val))
                return

            theta_sign_clockwise = sigma_RphiZ * sigma_rhothetaphi

            self.COCOS = COCOS[exp_Bp]
            self.exp_Bp = exp_Bp
            self.sigma_Bp = sigma_Bp
            self.sigma_RphiZ = sigma_RphiZ
            self.sigma_rhothetaphi = sigma_rhothetaphi
            self.sign_q_pos = sign_q_pos
            self.sign_pprime_pos = sign_pprime_pos
            self.theta_sign_clockwise = theta_sign_clockwise

    def get(self):
        """
        Return COCOS index and values

        Returns
        -------
        dict
            COCOS index and values in type dict
        """

        return {
            "COCOS": self.COCOS,
            "exp_Bp": self.exp_Bp,
            "sigma_Bp": self.sigma_Bp,
            "sigma_RphiZ": self.sigma_RphiZ,
            "sigma_rhothetaphi": self.sigma_rhothetaphi,
            "sign_q_pos": self.sign_q_pos,
            "sign_pprime_pos": self.sign_pprime_pos,
            "theta_sign_clockwise": self.theta_sign_clockwise,
        }

    @classmethod
    def values_coefficients(
        self, COCOS_in, COCOS_out, Ip_in, B0_in, Ipsign_out, B0sign_out
    ):
        """
        Provide transformation values for a set of quantities for a given pair
        of input/output COCOS numbers

        Parameters
        ----------
        COCOS_in: int
            COCOS input
        COCOS_out: int
            COCOS output
        Ip_in: float
            Plasma curent (toroidal component) [A]
        B0_in: float
            Vacuum toroidal field [T]
        Ipsign_out: int
            desired sign of Ip in output
        B0sign_out: int
            desired sign of B0 in output

        Returns
        -------
        dict
            COCOS transformation values in type dict
        """

        # Default outputs
        sigma_Ip_eff = 1.0
        sigma_B0_eff = 1.0
        sigma_Bp_eff = 1.0
        sigma_rhothetaphi_eff = 1.0
        sigma_RphiZ_eff = 1.0
        exp_Bp_eff = 1.0
        fact_psi = 1.0
        fact_q = 1.0
        fact_dpsi = 1.0
        fact_dtheta = 1.0

        # Check inputs
        sigma_Ip_in = np.sign(Ip_in)
        sigma_B0_in = np.sign(B0_in)

        # Get COCOS related parameters
        CVI = COCOS(index={"COCOS": COCOS_in}).get()
        CVO = COCOS(index={"COCOS": COCOS_out}).get()

        # Define effective variables: sigma_Ip_eff, si1gma_B0_eff, sigma_Bp_eff,
        # exp_Bp_eff as in Appendix C
        sigma_RphiZ_eff = float(CVO["sigma_RphiZ"] * CVI["sigma_RphiZ"])

        # sign(Ip) in output
        if Ipsign_out == 0:
            sigma_Ip_eff = sigma_RphiZ_eff  # sign folllowing transformation
        else:
            sigma_Ip_eff = sigma_Ip_in * float(Ipsign_out)
        sigma_Ip_out = sigma_Ip_in * sigma_Ip_eff

        # sign(B0) in output
        if B0sign_out == 0:
            sigma_B0_eff = sigma_RphiZ_eff  # sign folllowing transformation
        else:
            sigma_B0_eff = sigma_B0_in * float(B0sign_out)
        sigma_B0_out = sigma_B0_in * sigma_B0_eff

        sigma_Bp_eff = float(CVO["sigma_Bp"] * CVI["sigma_Bp"])
        exp_Bp_eff = float(CVO["exp_Bp"] - CVI["exp_Bp"])
        sigma_rhothetaphi_eff = float(
            CVO["sigma_rhothetaphi"] * CVI["sigma_rhothetaphi"]
        )
        #
        # Note that sign(sigma_RphiZ*sigma_rhothetaphi) gives theta in clockwise or count    er-clockwise respectively
        # Thus sigma_RphiZ_eff*sigma_rhothetaphi_eff negative if the direction of theta h    as changed from cocos_in to _out
        #
        fact_psi = sigma_Ip_eff * sigma_Bp_eff * (2.0 * np.pi) ** exp_Bp_eff
        fact_dpsi = sigma_Ip_eff * sigma_Bp_eff / (2.0 * np.pi) ** exp_Bp_eff
        fact_q = sigma_Ip_eff * sigma_B0_eff * sigma_rhothetaphi_eff
        fact_dtheta = sigma_RphiZ_eff * sigma_rhothetaphi_eff

        self.sigma_Ip_eff = sigma_Ip_eff
        self.sigma_B0_eff = sigma_B0_eff
        self.sigma_Bp_eff = sigma_Bp_eff
        self.sigma_rhothetaphi_eff = sigma_rhothetaphi_eff
        self.sigma_RphiZ_eff = sigma_RphiZ_eff
        self.exp_Bp_eff = exp_Bp_eff
        self.fact_psi = fact_psi
        self.fact_q = fact_q
        self.fact_dpsi = fact_dpsi
        self.fact_dtheta = fact_dtheta

        return {
            "sigma_Ip_eff": self.sigma_Ip_eff,
            "sigma_B0_eff": self.sigma_B0_eff,
            "sigma_Bp_eff": self.sigma_Bp_eff,
            "sigma_rhothetaphi_eff": self.sigma_rhothetaphi_eff,
            "sigma_RphiZ_eff": self.sigma_RphiZ_eff,
            "exp_Bp_eff": self.exp_Bp_eff,
            "fact_psi": self.fact_psi,
            "fact_q": self.fact_q,
            "fact_dpsi": self.fact_dpsi,
            "fact_dtheta": self.fact_dtheta,
        }


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

    global report_buf

    result = re.search("^(\d)\.\.\.(\d)$", p)
    if result is not None:  # constant coordinate definition (e.g. 1...3)
        return "range(" + str(result.group(2)) + ")"

    else:  # other coordinate definition
        if rm_last_bracket == True:
            p = p[: p.rfind("(")]
        p = re.sub("\((\w+)\)", r"(" + idx_header + "\\1)", p)
        p = p.replace("/", ".")
        p = p.replace("(", "[")
        p = p.replace(")", "]")

        if idx is not None:
            keys = idx.data.keys()
            for k in keys:
                s = idx_header + k
                p = p.replace(s, str(eval(s)))

        if header:
            return ids_header + p
        else:
            return p


# ----------------------------------------------------------------------


class IdxDict(dict):
    """
    Class for DD Sub-Indices (e.g. itime, i1, ..., etc.)

    Attributes
    ----------
    data: dict
        Keep subscripts of IDS field as type dict
    """

    def __init__(self, p):
        """
        Parameters
        ----------
        path_doc: str
            Field path
        """

        idict = []

        for m in re.finditer("\((\w+)\)", p):  # find subscripts and set as attribute
            it = m.group()[1:-1]
            idict.append("'" + it + "': None")  # initial value = None

        d = eval("{" + ",".join(idict) + "}")
        super(IdxDict, self).__setattr__("data", d)

    def __setattr__(self, k, v):
        """
        Parameters
        ----------
        k: str
            Names of subsript for IDS array
        v: dict
            Values of subsript for IDS array
        """

        self.data[k] = v

    def __getattr__(self, k):
        """
        Parameters
        ----------
        k: str
            Names of subsript for IDS array
        """

        try:
            return self.data[k]
        except KeyError:
            raise AttributeError


# ----------------------------------------------------------------------


class IDSValidator(cerberus.Validator):
    """
    Cerberus-Validator extended with custom rules for IDS

    Attributes
    ----------
    cocos: COCOS
        COCOS for validation
    shape: list
        data shape
    coord: list
        name of coordinate
    ndim: int
        number of dimension
    """

    cocos = {}
    # shape = []
    # coord = []
    ndim = None

    def set_cocos(self, cocos):
        """ """
        self.cocos = cocos

    def set_dim(self, field, ids, data, idx):
        """ """
        dtype = re.search("^(INT|FLT)_([1-9])D$", field.get("data_type"))
        if dtype is not None:
            self.shape = []
            self.coord = []
            self.ndim = int(dtype.group(2))
            #
            for i in range(data.ndim):
                c = path2py(field.get("coordinate" + str(i + 1)), header=True)
                homogeneous_time = ids.ids_properties.homogeneous_time
                #
                if re.search("1\.\.\.", c):
                    lcrd = data.shape[i]
                else:
                    try:
                        crd = eval(c)
                        lcrd = len(crd)
                    except:
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
                self._error(field, "Must be smaller than {}".format(max_value))
        except ValueError:
            pass

    def _validate_ids_ge(self, min_value, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            if np.any(v < min_value):
                self._error(field, "Must be larger than {}".format(min_value))
        except ValueError:
            pass

    def _validate_ids_lt(self, max_value, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            if np.any(v >= max_value):
                self._error(field, "Must be smaller than {}".format(max_value))
        except ValueError:
            pass

    def _validate_ids_gt(self, min_value, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            if np.any(v <= min_value):
                self._error(field, "Must be larger than {}".format(min_value))
        except ValueError:
            pass

    def _validate_ids_psi_like(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            psi_like = self.cocos["sigma_Ip"] * self.cocos["sigma_Bp"]
            if np.sign(v[-1] - v[0]) != psi_like:
                if not constraint:
                    self._error(field, "Sign expected as {}".format(psi_like))
        except ValueError:
            pass

    def _validate_ids_b0_like(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            b0_like = self.cocos["sigma_B0"]
            if np.any(np.sign(v) != b0_like):
                if not constraint:
                    self._error(field, "Sign expected as {}".format(b0_like))
        except ValueError:
            pass

    def _validate_ids_dodpsi_like(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            dodpsi_like = -self.cocos["sigma_Ip"] * self.cocos["sigma_Bp"]
            if np.any(np.sign(v) != dodpsi_like):
                if not constraint:
                    self._error(field, "Sign expected as {}".format(dodpsi_like))
        except ValueError:
            pass

    def _validate_ids_q_like(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            q_like = (
                self.cocos["sigma_Ip"]
                * self.cocos["sigma_B0"]
                * self.cocos["sigma_rhothetaphi"]
            )
            if np.any(np.sign(v) != q_like):
                if not constraint:
                    self._error(field, "Sign expected as {}".format(q_like))
        except ValueError:
            pass

    def _validate_ids_ip_like(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            ip_like = self.cocos["sigma_Ip"]
            if any(np.sign(v) != ip_like):
                if not constraint:
                    self._error(field, "Sign expected as {}".format(ip_like))
        except ValueError:
            pass

    def _validate_ids_dPdpsi_like(self, constraint, field, value):
        """{'nullable': False }"""
        try:
            v = np.atleast_1d(value).flatten()
            dodpsi_like = -self.cocos["sigma_Ip"] * self.cocos["sigma_Bp"]
            if np.sign(np.sum(np.sign(v))) != dodpsi_like:
                if not constraint:
                    self._error(field, "avg(Sign) expected as {}".format(dodpsi_like))
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


# ----------------------------------------------------------------------


def validator(field, path_doc, ids, schema, cocos, idx):
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
    idx: IdxDict=None
        DD Sub-Indices (e.g. itime, i1, ..., etc.)

    Returns
    -------
    remark: boolean
    """
    global report_buf

    data_size = 0

    p = path2py(path_doc, header=True)

    # eval for target data
    try:
        data = eval(p)
    except:
        print("eval error on key {}, skipped".format(p))
        return

    # eval for schema value in case of validation between data
    for key, value in schema[path_doc].items():
        if isinstance(value, str):
            val = re.sub("_([a-z]+\w+)_", idx_header + r"\1", value)
            val = val.replace(ids.__name__ + ".", ids_header)
            try:
                schema[path_doc][key] = eval(val)
            except:
                print("eval error on value {}, ignored".format(val))

    # Initialization
    v_ids = IDSValidator({path_doc: schema[path_doc]})
    v_ids.set_dim(field, ids, data, idx)
    v_ids.set_cocos(cocos)

    # Validation
    d = {path_doc: data}
    remark = v_ids.validate(d)
    errors = v_ids.errors

    # Report
    if args_verbose:
        report = {}
        report["remark"] = remark
        report["errors"] = errors
        report_buf.update({path2py(path_doc, idx=idx): report})
    else:
        if not remark:
            report_buf.update({path2py(path_doc, idx=idx): errors[list(errors)[0]]})

    # Result
    return remark


# ----------------------------------------------------------------------


def path_iterator(field, nodes, ids, schema, cocos, idx=None, level=0):
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
    idx: IdxDict=None
        DD Sub-Indices (e.g. itime, i1, ..., etc.)
    level: int=0
        Depth of node in target field
    """

    p = "/".join(nodes[: level + 1])
    if level < len(nodes) - 1:
        result = re.search("(\w+)(\(\w+\))$", p)

        # for dynamic array (e.g. path(itime)/to(i1)/array(i2))
        if result is not None:
            try:
                wk = eval(path2py(p, rm_last_bracket=True, header=True))
                for i in range(len(wk)):
                    idxname = result.group(2)[1:-1]
                    # increment the index in global scope
                    exec(idxname + "=" + str(i), idx.data)
                    path_iterator(
                        field,
                        nodes,
                        ids,
                        schema,
                        cocos,
                        idx=idx,
                        level=level + 1,
                    )
                    if not args_check_all:
                        break
            except:
                pass

        # for node (e.g. path(itime)/to(i1)/node)
        else:
            path_iterator(field, nodes, ids, schema, cocos, idx=idx, level=level + 1)

    else:
        validator(field, p, ids, schema, cocos, idx)


# ----------------------------------------------------------------------


def validate_COCOS(ids, schema, itime, cocos=None):
    """Compute COCOS values using stored data in IDS/equilibrium

    Parameters
    ----------
    ids: IDS
        IDS for COCOS estimation
    cocos_check: COCOS=None
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
        except:
            print("eval error on key {}".format(key))
            return

        remark = v_ids.validate({key: data})
        errors = v_ids.errors
        if not remark:
            raise ValueError(errors)
            # return
            pass


# ----------------------------------------------------------------------


def compute_COCOS(ids, cocos_check=None):
    """Compute COCOS values using experimental data in IDS/equilibrium

    Parameters
    ----------
    ids: IDS
        IDS for COCOS estimation
    cocos_check: COCOS=None
        Validate IDS wrt COCOS if given

    Returns
    -------
    cocos: COCOS
    """

    # COCOS Values in the middle of time sequence
    itime = int(np.floor(float(len(ids.time_slice)) / 2.0))

    # Check IDS/eq
    validate_COCOS(ids, required_fields_eq, itime)
    if cocos_check:
        validate_COCOS(ids, required_fields_cocos, itime, cocos=cocos_check)

    # Sign(Ip) and Sign(B0) from input
    ipsign = np.sign(ids.time_slice[itime].global_quantities.ip)
    b0sign = np.sign(ids.vacuum_toroidal_field.b0[0])

    # Eq.(22)
    dpsi = (
        ids.time_slice[itime].profiles_1d.psi[-1]
        - ids.time_slice[itime].profiles_1d.psi[0]
    )
    sigma_Bp = np.sign(dpsi) * ipsign

    # Eq.(22)
    q = ids.time_slice[itime].profiles_1d.q
    sign_q = np.sign(np.sum(np.sign(q)))
    sign_q_pos = sign_q * ipsign * b0sign

    # Eq.(22)
    sigma_rhothetaphi = sign_q_pos

    # Eq.(22)
    dpressure_dpsi = ids.time_slice[itime].profiles_1d.dpressure_dpsi
    sign_pprime_pos = np.sign(np.sum(np.sign(dpressure_dpsi))) * ipsign

    # sigma_RphiZ from Eq.(19)
    bz = ids.time_slice[itime].profiles_2d[0].b_field_z
    psi2d = ids.time_slice[itime].profiles_2d[0].psi
    r2d = ids.time_slice[itime].profiles_2d[0].r

    dpsi2d = np.gradient(psi2d)
    dr2d = np.gradient(r2d)
    dpsi2drdr = dpsi2d[0] / dr2d[0] / r2d

    # todo - reduce num. of data for COCOS discrimination
    #      - compute rtol(s) instead of fixed ones.
    dim2 = ids.time_slice[itime].profiles_2d[0].grid.dim2
    z_axis = ids.time_slice[itime].global_quantities.magnetic_axis.z
    psi_axis = ids.time_slice[itime].profiles_1d.psi[0]

    # grid of magnetic axis in Z
    iz = np.argmin(np.absolute(dim2 - z_axis))
    # psi ref. inside LCFS
    psi_ref = psi_axis + dpsi * 0.75

    # grids close to psi ref.
    rows, cols = np.where((np.isclose(psi2d, psi_ref, rtol=0.2)) & (bz !=0))
    # discard grids in private flux region)
    w = np.where(np.isclose(cols, iz, rtol=0.1))

    twopi_expBp_sigma_RphiZ = np.zeros(bz.shape)
    twopi_expBp_sigma_RphiZ = (
        -sigma_Bp * dpsi2drdr[rows[w], cols[w]] / bz[rows[w], cols[w]]
    )
    sigma_RphiZ = np.sign(np.sum(np.sign(twopi_expBp_sigma_RphiZ)))

    # exp_Bp from Eq.(19)
    x = np.average(twopi_expBp_sigma_RphiZ * sigma_RphiZ)
    exp_Bp = np.where(np.isclose(x, 2.0 * np.pi, rtol=0.5), 1, 0)

    #
    values = {
        "exp_Bp": int(exp_Bp),
        "sigma_Bp": int(sigma_Bp),
        "sigma_RphiZ": int(sigma_RphiZ),
        "sigma_rhothetaphi": int(sigma_rhothetaphi),
        "sign_q_pos": int(sign_q_pos),
        "sign_pprime_pos": int(sign_pprime_pos),
    }

    cocos = COCOS(values=values).get()

    return cocos


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


def load_XML(fpath):
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
        exit("file not found:{}".format(fpath))

    return root


# ----------------------------------------------------------------------


def load_YAML(fpath):
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
    except:
        exit("can not open file:{}".format(fpath))
    try:
        d = yaml.safe_load(f)
    except:
        exit("invalid yaml in:{}".format(fpath))

    return d


# ----------------------------------------------------------------------


def load_DD(idsname):
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

    root = load_XML(FILE_IDSDef)
    dd = [dd for dd in root if dd.get("name") == idsname][0]

    return dd


# ----------------------------------------------------------------------


def eval_IDSs(s):
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

    global report_buf
    idsname = ids.__name__
    maxoc = ids.getMaxOccurrences()
    buf = {}
    dictw = {}

    # Initialization of IDS Occurrence
    if isinstance(occ, int):
        if occ in range(maxoc):
            range_oc = [occ]
        else:
            exit("value error:{}".format(occ))
    else:
        exit("type error:{}".format(occ))

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
                        idx=IdxDict(path),
                    )

            if args_verbose:
                if bool(report_buf):
                    dictw["remark"] = all(
                        {report_buf[x]["remark"] for x in report_buf.keys()}
                    )
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
        ddo = load_DD(idsname)
    else:
        exit("type error:{}".format(dd))

    for field in ddo.iter():
        data_type = field.attrib.get("data_type")
        path_doc = field.attrib.get("path_doc")

        # validata for data_type = INT_*D and FLT_*D
        if data_type and re.search("^(INT|FLT)_([1-9])D$", data_type) is not None:

            # skip validation for error_upper and error_lower
            if re.search("_error_(upper|lower)", path_doc) is None:
                d[path_doc] = rule

    schema = {idsname: d}

    return schema, ddo


# ----------------------------------------------------------------------


def ids_validator(
    ids, schema, dd=None, occ=0, ipsign=-1, b0sign=-1, verbose=False, check_all=True
):
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
        schema = load_YAML(schema)
    else:
        exit("type error:{}".format(schema))

    # DD Initialization for Target IDS
    if ET.iselement(dd):
        pass
    elif dd is None:
        dd = load_DD(ids.__name__)
    else:
        exit("type error:{}".format(dd))

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

    return eval_IDSs(dict_to_yaml(out)), out


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


def ids_cocos_check(ids, verbose=False):
    """Function Interface for IDS Validation on COCOS

    Parameters
    ----------
    ids: IDS
        IDS for validation
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
            cocos = compute_COCOS(ids)
        except Exception as e:
            exit("Cannot compute COCOS: {}".format(e))
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
        exit("equilibrium instead of {}".format(ids.__name__))

    return remark, error


# ----------------------------------------------------------------------


def ids_compute_cocos(ids):
    """Function Interface for computing COCOS

    Parameters
    ----------
    ids: IDS
        IDS for cocos estimation

    Returns
    -------
    cocos: int
        COCOS number computed
    """

    key = "COCOS"

    if ids.__name__ == "equilibrium":
        try:
            cocos = compute_COCOS(ids)
        except Exception as e:
            exit("Cannot compute COCOS: {}".format(e))
    else:
        exit("equilibrium instead of {}".format(ids.__name__))

    return cocos[key]


# ----------------------------------------------------------------------
