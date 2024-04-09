#!/usr/bin/env python
from sys import version
import os
import datetime
import numpy as np
from statistics import median
import logging
from pprint import pformat
from fortranformat import FortranRecordReader

import imas
from database_tools.idschk import IDS_COCOS, COCOS, compute_COCOS


logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------


class GEQDSK:
    """
    GEQDSK module for IMAS

    [1] L.L. Lao, "G EQDSK FORMAT", https://w3.pppl.gov/ntcc/TORAY/G_EQDSK.pdf
    [2] O. Sauter and S.Yu. Medvedev, "Tokamak Coordinate Conventions : COCOS",
        Comput. Physics Commun. 184 (2013) 293

    Attributes
    ----------
    fpath: str
        Path to GEQDSK file
    data: OrderedDict
        Information in GEQDSK file
    cocos: COCOS
        Class COCOS computed from input
    coef: dict
        COCOS Transformation coefficients regarding IDS default (COCOS=11)
    """

    def __init__(self, fpath, ipsign_out, b0sign_out, cocos_in):
        """
        Read GEQDSK file and set COCOS transformation coefficients

        Parameters
        ----------
        fpath: str
            Path to GEQDSK file
        ipsign_out: int
            Desired sign(Ip) in output
        b0sign_out: int
            Desired sign(B0) in output
        cocos_in: int
            Coerce input COCOS
        """

        # 1. Register name of GEQDSK file
        self.fpath = os.path.expanduser(os.path.expandvars(fpath))
        logger.debug("GEQDSK fpath: \n%s", pformat(self.fpath, indent=2))

        # 2. Read GEQDSK file
        self.data = self._load(self.fpath)
        logger.debug(
            "GEQDSK data: \n%s", pformat(self.data, indent=2, sort_dicts=False)
        )

        # 3. Confer COCOS
        if cocos_in:
            self.cocos = COCOS(
                index={
                    "COCOS": cocos_in,
                    "ipsign": np.sign(self.data["CURRENT"]),
                    "b0sign": np.sign(self.data["BCENTR"]),
                }
            )
        else:
            self.cocos = self._set_cocos(self.data)

        logger.info(
            "GEQDSK COCOS: \n%s",
            pformat(self.cocos.__dict__, indent=2, sort_dicts=False),
        )

        # 4. Compute transformation coeff.
        self.coef = self.cocos.values_coefficients(
            self.cocos.COCOS,
            IDS_COCOS,
            self.data["CURRENT"],
            self.data["BCENTR"],
            ipsign_out,
            b0sign_out,
        )
        logger.info(
            "GEQDSK Transformation Coeff.: \n%s",
            pformat(self.coef, indent=2, sort_dicts=False),
        )

    def _load(self, fpath):
        """
        Read GEQDSK

        Parameters
        ----------
        fpath: str
            Path to GEQDSK file

        Returns
        -------
        dict
            Information in GEQDSK file
        """

        if not os.path.exists(fpath):
            raise FileNotFoundError(fpath)

        if os.stat(fpath).st_size == 0:
            raise IOError(f"file size is zero: {fpath}")

        try:
            fp = open(fpath, "r")
        except OSError:
            raise IOError(f"cannot open/read file: {fpath}")

        fmt00 = FortranRecordReader("6a8,3i4")
        fmt20 = FortranRecordReader("5e16.9")
        fmt22 = FortranRecordReader("2i5")

        data = {}

        #
        header = fp.readline().rstrip()
        rec = fmt00.read(header)
        data["CASE"] = rec[0:6]
        if len(header) != 60:
            logger.warning(f"irregular length of header: {len(header)}")
            header = header.split()
            data["IDUM"] = int(header[-3])
            data["NW"] = nw = int(header[-2])
            data["NH"] = nh = int(header[-1])
        else:
            data["IDUM"] = int(header[48:52])
            data["NW"] = nw = int(header[52:56])
            data["NH"] = nh = int(header[56:60])

        #
        rec = np.float64(fmt20.read(fp.readline()))
        data["RDIM"] = rec[0]
        data["ZDIM"] = rec[1]
        data["RCENTR"] = rec[2]
        data["RLEFT"] = rec[3]
        data["ZMID"] = rec[4]

        #
        rec = np.float64(fmt20.read(fp.readline()))
        data["RMAXIS"] = rec[0]
        data["ZMAXIS"] = rec[1]
        data["SIMAG"] = rec[2]
        data["SIBRY"] = rec[3]
        data["BCENTR"] = rec[4]

        #
        rec = np.float64(fmt20.read(fp.readline()))
        data["CURRENT"] = rec[0]
        #data["SIMAG"] = rec[1]
        data["XDUM"] = rec[2]
        #data["RMAXIS"] = rec[3]
        data["XDUM"] = rec[4]

        #
        rec = np.float64(fmt20.read(fp.readline()))
        #data["ZMAXIS"] = rec[0]
        data["XDUM"] = rec[1]
        #data["SIBRY"] = rec[2]
        data["XDUM"] = rec[3]
        data["XDUM"] = rec[4]

        #
        data["FPOL"] = self._read1d(fp, nw, fmt20)
        data["PRES"] = self._read1d(fp, nw, fmt20)
        data["FFPRIM"] = self._read1d(fp, nw, fmt20)
        data["PPRIME"] = self._read1d(fp, nw, fmt20)
        data["PSIRZ"] = np.reshape(self._read1d(fp, nw * nh, fmt20), (nh, nw))
        data["QPSI"] = self._read1d(fp, nw, fmt20)

        #
        rec = [0, 0]
        try:
            rec = np.int32(fmt22.read(fp.readline()))
        except:
            pass
        data["NBBBS"] = nbbbs = rec[0]
        data["LIMITR"] = limitr = rec[1]

        #
        if nbbbs > 0:
            bbbs = np.reshape(self._read1d(fp, 2 * nbbbs, fmt20), (nbbbs, 2))
            data["RBBBS"] = bbbs[:, 0]
            data["ZBBBS"] = bbbs[:, 1]
        else:
            data["RBBBS"] = []
            data["ZBBBS"] = []

        #
        if limitr > 0:
            lim = np.reshape(self._read1d(fp, 2 * limitr, fmt20), (limitr, 2))
            data["RLIM"] = lim[:, 0]
            data["ZLIM"] = lim[:, 1]
        else:
            data["RLIM"] = []
            data["ZLIM"] = []

        return data

    def _read1d(self, fp, nlen, fmt):
        """
        Read array with specified format in Fortran

        Parameters
        ----------
        fp: _io.TextIOWrapper
            file pointer
        nlen: int
            length of record
        fmt: FortranRecordReader

        Returns
        -------
        numpy.ndarray, dtype=numpy.float64
        """

        ret = np.zeros(nlen, dtype=np.float64)
        i = 0
        while i < nlen - 1:
            fdata = fmt.read(fp.readline())
            i2 = min(i + len(fdata), nlen)
            ret[i:i2] = fdata[: i2 - i]
            i = i2

        if i < nlen:
            fdata = fmt.read(fp.readline())
            ret[i:] = fdata[: nlen - i]

        return ret

    def _set_cocos(self, g):
        """
        Compute COCOS for GEQDSK file and Return class COCOS

        Parameters
        ----------
        g: dict
            Information of GEQDSK file

        Returns
        -------
        COCOS
            COCOS index and values
        """

        # Sign(Ip) and Sign(B0) from input
        sigma_ip = np.sign(g["CURRENT"])
        sigma_b0 = np.sign(g["BCENTR"])

        # PSIRZ divided by 2*pi [1], Table 1(a) [2]
        exp_Bp = 0

        # Eq.(22) [2]
        sign_psi_edge_axis = np.sign(g["SIBRY"] - g["SIMAG"])
        sigma_Bp = int(sign_psi_edge_axis * sigma_ip)

        # Right-handed cylindrical coordinate system [1], Table 1(a) [2]
        sigma_RphiZ = int(+1)

        # Eq.(22), Table 1(b) [2]
        x = np.sign(median(g["QPSI"]))
        if x > 0.0:
            sign_q = int(+1)
        elif x < 0.0:
            sign_q = int(-1)
        else:
            sign_q = int(0)  # raise ValueError in Class COCOS
        sign_q_pos = int(sign_q * sigma_ip * sigma_b0)

        # Eq.(22) [2]
        sigma_rhothetaphi = int(sign_q * sigma_ip * sigma_b0)

        # Eq.(22), Table 1(b) [2]
        x = np.sign(median(g["PPRIME"]))
        if x > 0.0:
            sign_pprime = int(+1)
        elif x < 0.0:
            sign_pprime = int(-1)
        else:
            sign_pprime = int(0)  # raise ValueError in Class COCOS
        sign_pprime_pos = int(sign_pprime * sigma_ip)

        values = {
            "exp_Bp": exp_Bp,
            "sigma_Bp": sigma_Bp,
            "sigma_RphiZ": sigma_RphiZ,
            "sigma_rhothetaphi": sigma_rhothetaphi,
            "sign_q_pos": sign_q_pos,
            "sign_pprime_pos": sign_pprime_pos,
            "ipsign": sigma_ip,
            "b0sign": sigma_b0,
        }

        return COCOS(values=values)


# ----------------------------------------------------------------------


def map_GEQDSK_to_IDS(geqdsk, eq):
    """
    Convert GEQDSK file into IDS/equilibrium

    Parameters
    ----------
    geqdsk: GEQDSK
        Class GEQDSK
    eq: imas_*_ual_*.equilibrium.equilibrium ('*' corresponds to IMAS/UAL ver.)
        IDS/equilibrium

    Returns
    ----------
    None
    """

    def set_timebase(ids):
        """ """

        ids.time.resize(1)
        ids.time[0] = -1.0

    def common_properties(ids):
        """ """

        ids.ids_properties.homogeneous_time = 1
        ids.ids_properties.creation_date = datetime.datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )
        ids.ids_properties.provider = os.getenv("USER")
        ids.ids_properties.version_put.data_dictionary = os.getenv("IMAS_VERSION")
        ids.ids_properties.version_put.access_layer = os.getenv("UAL_VERSION")
        ids.ids_properties.version_put.access_layer_language = version

        ids.ids_properties.provenance.node.resize(1)
        ids.ids_properties.provenance.node[0].sources.append(geqdsk.fpath)

        ids.code.name = "IDStools/eqdsk2ids"
        ids.code.repository = "https://git.iter.org/projects/IMAS/repos/idstools/browse"
        ids.code.output_flag.resize(1)
        ids.code.output_flag[0] = 0

    # Abbrev.
    gdsk = geqdsk.data
    coef = geqdsk.coef

    # IDS_COCOS
    cocos = COCOS(index={"COCOS": IDS_COCOS, "ipsign": +1, "b0sign": +1})

    # IDS info.
    common_properties(eq)

    # Set time
    set_timebase(eq)

    # 0D
    eq.time_slice.resize(1)
    eq.time_slice[0].global_quantities.ip = gdsk["CURRENT"] * coef["sigma_Ip_eff"]
    eq.time_slice[0].global_quantities.magnetic_axis.r = gdsk["RMAXIS"]
    eq.time_slice[0].global_quantities.magnetic_axis.z = gdsk["ZMAXIS"]
    eq.time_slice[0].global_quantities.psi_axis = gdsk["SIMAG"] * coef["fact_psi"]
    eq.time_slice[0].global_quantities.psi_boundary = gdsk["SIBRY"] * coef["fact_psi"]

    # vacuume_toroidal_field
    eq.vacuum_toroidal_field.r0 = gdsk["RCENTR"]
    eq.vacuum_toroidal_field.b0.resize(1)
    eq.vacuum_toroidal_field.b0[0] = gdsk["BCENTR"] * coef["sigma_B0_eff"]

    # 1D
    nw = gdsk["NW"]
    nh = gdsk["NH"]
    eq.time_slice[0].profiles_1d.dpressure_dpsi.resize(nw)
    eq.time_slice[0].profiles_1d.f_df_dpsi.resize(nw)
    eq.time_slice[0].profiles_1d.f.resize(nw)
    eq.time_slice[0].profiles_1d.pressure.resize(nw)
    eq.time_slice[0].profiles_1d.q.resize(nw)
    eq.time_slice[0].profiles_1d.psi.resize(nw)

    eq.time_slice[0].profiles_1d.dpressure_dpsi = gdsk["PPRIME"] / coef["fact_psi"]
    eq.time_slice[0].profiles_1d.f_df_dpsi = gdsk["FFPRIM"] / coef["fact_psi"]
    eq.time_slice[0].profiles_1d.f = gdsk["FPOL"] * coef["sigma_B0_eff"]
    eq.time_slice[0].profiles_1d.pressure = gdsk["PRES"]
    eq.time_slice[0].profiles_1d.q = gdsk["QPSI"] * coef["fact_q"]
    simag = gdsk["SIMAG"]
    sibry = gdsk["SIBRY"]
    for i in range(nw):
        eq.time_slice[0].profiles_1d.psi[i] = (
            (1.0 - float(i) / float(nw - 1)) * (simag - sibry) + sibry
        ) * coef["fact_psi"]

    # Boundary
    if gdsk["NBBBS"] > 0:
        eq.time_slice[0].boundary.outline.r.resize(gdsk["NBBBS"])
        eq.time_slice[0].boundary.outline.z.resize(gdsk["NBBBS"])
        eq.time_slice[0].boundary.outline.r = gdsk["RBBBS"]
        eq.time_slice[0].boundary.outline.z = gdsk["ZBBBS"]

    # 2D
    eq.time_slice[0].profiles_2d.resize(1)
    eq.time_slice[0].profiles_2d[0].grid_type.index = 1
    eq.time_slice[0].profiles_2d[0].grid.dim1.resize(nw)
    eq.time_slice[0].profiles_2d[0].grid.dim2.resize(nh)
    eq.time_slice[0].profiles_2d[0].psi.resize(nw, nh)
    eq.time_slice[0].profiles_2d[0].r.resize(nw, nh)
    eq.time_slice[0].profiles_2d[0].z.resize(nw, nh)
    eq.time_slice[0].profiles_2d[0].b_field_r.resize(nw, nh)
    eq.time_slice[0].profiles_2d[0].b_field_z.resize(nw, nh)
    for i in range(nw):
        eq.time_slice[0].profiles_2d[0].grid.dim1[i] = (
            float(i) / float(nw - 1) * gdsk["RDIM"] + gdsk["RLEFT"]
        )
    for j in range(nh):
        eq.time_slice[0].profiles_2d[0].grid.dim2[j] = (
            float(j) / float(nh - 1) * gdsk["ZDIM"] - 0.5 * gdsk["ZDIM"] + gdsk["ZMID"]
        )
    for j in range(nh):
        for i in range(nw):
            eq.time_slice[0].profiles_2d[0].psi[i, j] = (
                gdsk["PSIRZ"][j, i] * coef["fact_psi"]
            )
    for j in range(nh):
        for i in range(nw):
            eq.time_slice[0].profiles_2d[0].r[i, j] = (
                eq.time_slice[0].profiles_2d[0].grid.dim1[i]
            )
            eq.time_slice[0].profiles_2d[0].z[i, j] = (
                eq.time_slice[0].profiles_2d[0].grid.dim2[j]
            )
    # Eq. (19)
    fact = cocos.sigma_RphiZ * cocos.sigma_Bp / (2.0 * np.pi) ** cocos.exp_Bp
    dim1 = eq.time_slice[0].profiles_2d[0].grid.dim1
    dim2 = eq.time_slice[0].profiles_2d[0].grid.dim2
    for i in range(nw):
        psi = eq.time_slice[0].profiles_2d[0].psi[i, :]
        br = np.gradient(psi, dim2, edge_order=2) / dim1[i]
        eq.time_slice[0].profiles_2d[0].b_field_r[i, :] = br[:] * fact
    for j in range(nh):
        psi = eq.time_slice[0].profiles_2d[0].psi[:, j]
        bz = np.gradient(psi, dim1, edge_order=2) / dim1[:]
        eq.time_slice[0].profiles_2d[0].b_field_z[:, j] = bz[:] * fact * -1.0

    logger.debug("IDS/equilibrium: \n%s", pformat(eq, indent=2, sort_dicts=False))


# ----------------------------------------------------------------------


def geqdsk2ids(fpath, ipsign=0, b0sign=0, cocos_in=None):
    """
    Functional Interface of GEQDSK Converter (geqdsk2ids)

    Parameters
    ----------
    fpath: str
        Path to GEQDSK file
    ipsign_out: int=0, optional
        Desired sign(Ip) in output
    b0sign_out: int=0, optional
        Desired sign(B0) in output
    cocos_in: int=None, optional
        Coerce input COCOS

    Returns
    -------
    eq: imas_*_ual_*.equilibrium.equilibrium ('*' corresponds to IMAS/UAL ver.)
        IDS/equilibrium
    """

    # Read GEQDSK file
    logger.info("loading GEQDSK file ...")
    geqdsk = GEQDSK(fpath, ipsign, b0sign, cocos_in)

    # Map GEQDSK to IDS/equilibrium
    logger.info("mapping GEQDSK to IDS/equilibrium ...")
    eq = imas.equilibrium()
    map_GEQDSK_to_IDS(geqdsk, eq)

    # COCOS Check
    cocos = compute_COCOS(eq)
    logger.info("IDS COCOS: \n%s", pformat(cocos, indent=2))

    # Check if COCOS is equal to IDS_COCOS
    if cocos["COCOS"] != IDS_COCOS:
        logger.warning("COCOS Target= {}, Output= {}, Input= {}".format(IDS_COCOS, cocos["COCOS"], geqdsk.cocos.COCOS))
        raise SystemExit("Terminated due to COCOS mismatch in output. Try to coerce COCOS or use another value with '--cocos_in' option.")
    return eq


# ----------------------------------------------------------------------


def eqdsk2ids(gfile=None, afile=None, ipsign=0, b0sign=0, cocos_in=None):
    """
    Functional Interface of EQDSK Converter (eqdsk2ids)

    Parameters
    ----------
    gfile: str
        Path to GEQDSK file
    afile: str
        Path to AEQDSK file (*not in use)
    ipsign_out: int=0, optional
        Desired sign(Ip) in output
    b0sign_out: int=0, optional
        Desired sign(B0) in output
    cocos_in: int=None, optional
        Coerce input COCOS

    Returns
    -------
    eq: imas_*_ual_*.equilibrium.equilibrium ('*' corresponds to IMAS/UAL ver.)
        IDS/equilibrium
    """

    # option "afile" not yet implemented
    if gfile is not None:
        return geqdsk2ids(gfile, ipsign=ipsign, b0sign=b0sign, cocos_in=cocos_in)
    else:
        return None
