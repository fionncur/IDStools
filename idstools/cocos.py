import logging
import traceback

try:
    import imaspy as imas
except ImportError:
    import imas
import numpy as np

# set cocos in the DD version from the environment
IDS_COCOS = int(imas.dd_zip.dd_etree().find("cocos").text)


logger = logging.getLogger(f"module.{__name__}")


class COCOS:
    """
    COCOS module in Python.

    This module provides functionality related to coordinate conventions in tokamak physics.

    References:
        O. Sauter and S. Yu. Medvedev, "Tokamak Coordinate Conventions: COCOS",Comput. Physics Commun 84 (2013), 293.
        `cocos_module.f90 (CHEASE)`.

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
            raise ValueError("Initialize COCOS with either index or values: both not given")
            return

        elif (index is not None) and (values is not None):
            raise ValueError("Initialize COCOS with either index or values: both given")
            return

        # in case of init. by index
        elif index is not None:

            COCOS = index["COCOS"]
            ipsign = index["ipsign"]
            b0sign = index["b0sign"]
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
                raise ValueError(f"error: COCOS = {COCOS} does not exist")
                return

            (
                sigma_bp,
                sigma_rphi_z,
                sigma_rhothetaphi,
                sign_q_pos,
                sign_pprime_pos,
            ) = val

            # cocos=i or 10+i have similar coordinate conventions except psi/2pi for
            # cocos=i and psi for cocos=10+i

            if COCOS >= 11:
                exp_bp = 1
            else:
                exp_bp = 0

            theta_sign_clockwise = sigma_rphi_z * sigma_rhothetaphi

            self.COCOS = COCOS
            self.sigma_ip = ipsign
            self.sigma_b0 = b0sign
            self.exp_bp = exp_bp
            self.sigma_bp = sigma_bp
            self.sigma_rphi_z = sigma_rphi_z
            self.sigma_rhothetaphi = sigma_rhothetaphi
            self.sign_q_pos = sign_q_pos
            self.sign_pprime_pos = sign_pprime_pos
            self.theta_sign_clockwise = theta_sign_clockwise

        # in case of init. by values
        else:

            sigma_ip = values["ipsign"]
            sigma_b0 = values["b0sign"]
            exp_bp = values["exp_Bp"]
            sigma_bp = values["sigma_Bp"]
            sigma_rphi_z = values["sigma_RphiZ"]
            sigma_rhothetaphi = values["sigma_rhothetaphi"]
            sign_q_pos = values["sign_q_pos"]
            sign_pprime_pos = values["sign_pprime_pos"]

            val = (
                sigma_bp,
                sigma_rphi_z,
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
                raise ValueError(f"error: COCOS Values not match {val}")
                return

            theta_sign_clockwise = sigma_rphi_z * sigma_rhothetaphi

            self.COCOS = COCOS[exp_bp]
            self.sigma_ip = sigma_ip
            self.sigma_b0 = sigma_b0
            self.exp_bp = exp_bp
            self.sigma_bp = sigma_bp
            self.sigma_rphi_z = sigma_rphi_z
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
            "sigma_Ip": self.sigma_ip,
            "sigma_B0": self.sigma_b0,
            "exp_Bp": self.exp_bp,
            "sigma_Bp": self.sigma_bp,
            "sigma_RphiZ": self.sigma_rphi_z,
            "sigma_rhothetaphi": self.sigma_rhothetaphi,
            "sign_q_pos": self.sign_q_pos,
            "sign_pprime_pos": self.sign_pprime_pos,
            "theta_sign_clockwise": self.theta_sign_clockwise,
        }

    @classmethod
    def values_coefficients(self, COCOS_in, COCOS_out, ip_in, b0_in, ipsign_out, b0sign_out):
        """
        Provide transformation values for a set of quantities for a given pair
        of input/output COCOS numbers

        Parameters
        ----------
        COCOS_in: int
            COCOS input
        COCOS_out: int
            COCOS output
        ip_in: float
            Plasma curent (toroidal component) [A]
        b0_in: float
            Vacuum toroidal field [T]
        ipsign_out: int
            desired sign of Ip in output
        b0sign_out: int
            desired sign of B0 in output

        Returns
        -------
        dict
            COCOS transformation values in type dict
        """

        # Default outputs
        sigma_ip_eff = 1.0
        sigma_b0_eff = 1.0
        sigma_bp_eff = 1.0
        sigma_rhothetaphi_eff = 1.0
        sigma_rphi_z_eff = 1.0
        exp_bp_eff = 1.0
        fact_psi = 1.0
        fact_q = 1.0
        fact_dpsi = 1.0
        fact_dtheta = 1.0

        # Check inputs
        sigma_ip_in = np.sign(ip_in)
        sigma_b0_in = np.sign(b0_in)

        # Get COCOS related parameters
        c_v_i = COCOS(index={"COCOS": COCOS_in, "ipsign": sigma_ip_in, "b0sign": sigma_b0_in}).get()
        c_v_o = COCOS(index={"COCOS": COCOS_out, "ipsign": ipsign_out, "b0sign": b0sign_out}).get()

        # Define effective variables: sigma_Ip_eff, si1gma_B0_eff, sigma_Bp_eff,
        # exp_Bp_eff as in Appendix C
        sigma_rphi_z_eff = float(c_v_o["sigma_RphiZ"] * c_v_i["sigma_RphiZ"])

        # sign(Ip) in output
        if ipsign_out == 0:
            sigma_ip_eff = sigma_rphi_z_eff  # sign folllowing transformation
        else:
            sigma_ip_eff = sigma_ip_in * float(ipsign_out)
        # sigma_Ip_out = sigma_Ip_in * sigma_Ip_eff

        # sign(B0) in output
        if b0sign_out == 0:
            sigma_b0_eff = sigma_rphi_z_eff  # sign folllowing transformation
        else:
            sigma_b0_eff = sigma_b0_in * float(b0sign_out)
        # sigma_B0_out = sigma_B0_in * sigma_B0_eff

        sigma_bp_eff = float(c_v_o["sigma_Bp"] * c_v_i["sigma_Bp"])
        exp_bp_eff = float(c_v_o["exp_Bp"] - c_v_i["exp_Bp"])
        sigma_rhothetaphi_eff = float(c_v_o["sigma_rhothetaphi"] * c_v_i["sigma_rhothetaphi"])
        #
        # Note that sign(sigma_RphiZ*sigma_rhothetaphi) gives theta in clockwise or counter-clockwise respectively
        # Thus sigma_RphiZ_eff*sigma_rhothetaphi_eff negative if the direction of
        # theta has changed from cocos_in to _out
        #
        fact_psi = sigma_ip_eff * sigma_bp_eff * (2.0 * np.pi) ** exp_bp_eff
        fact_dpsi = sigma_ip_eff * sigma_bp_eff / (2.0 * np.pi) ** exp_bp_eff
        fact_q = sigma_ip_eff * sigma_b0_eff * sigma_rhothetaphi_eff
        fact_dtheta = sigma_rphi_z_eff * sigma_rhothetaphi_eff

        self.sigma_ip_eff = sigma_ip_eff
        self.sigma_b0_eff = sigma_b0_eff
        self.sigma_bp_eff = sigma_bp_eff
        self.sigma_rhothetaphi_eff = sigma_rhothetaphi_eff
        self.sigma_rphi_z_eff = sigma_rphi_z_eff
        self.exp_bp_eff = exp_bp_eff
        self.fact_psi = fact_psi
        self.fact_q = fact_q
        self.fact_dpsi = fact_dpsi
        self.fact_dtheta = fact_dtheta

        return {
            "sigma_Ip_eff": self.sigma_ip_eff,
            "sigma_B0_eff": self.sigma_b0_eff,
            "sigma_Bp_eff": self.sigma_bp_eff,
            "sigma_rhothetaphi_eff": self.sigma_rhothetaphi_eff,
            "sigma_RphiZ_eff": self.sigma_rphi_z_eff,
            "exp_Bp_eff": self.exp_bp_eff,
            "fact_psi": self.fact_psi,
            "fact_q": self.fact_q,
            "fact_dpsi": self.fact_dpsi,
            "fact_dtheta": self.fact_dtheta,
        }


def compute_COCOS(ids, itime=None, i1=0):
    """Compute COCOS values using experimental data in IDS/equilibrium

    Parameters
    ----------
    ids: IDS
        IDS/equilibrium for COCOS estimation
    itime: int|None
        Index of struct_array time_slice in IDS/equilibrium
    i1: int=0
        Index of struct_array profiles_2d in IDS/equilibrium

    Returns
    -------
    cocos: COCOS
    """

    # COCOS Values in the middle of time sequence
    if itime is None:
        itime = int(np.floor(float(len(ids.time_slice)) / 2.0))

    # Sign(Ip) and Sign(B0) from input
    ipsign = np.sign(ids.time_slice[itime].global_quantities.ip)
    b0sign = np.sign(ids.vacuum_toroidal_field.b0[itime])

    # 1 Eq.(22)
    dpsi = ids.time_slice[itime].profiles_1d.psi[-1] - ids.time_slice[itime].profiles_1d.psi[0]
    sigma_bp = np.sign(dpsi) * ipsign

    # 2 Eq.(22)
    q = ids.time_slice[itime].profiles_1d.q
    sign_q = np.sign(np.sum(np.sign(q)))
    sign_q_pos = sign_q * ipsign * b0sign

    # 3 Eq.(22)
    sigma_rhothetaphi = sign_q_pos

    # 4 Eq.(22)
    dpressure_dpsi = ids.time_slice[itime].profiles_1d.dpressure_dpsi
    sign_pprime_pos = np.sign(np.sum(np.sign(dpressure_dpsi))) * ipsign

    # 5 sigma_RphiZ from Eq.(19)
    bz = ids.time_slice[itime].profiles_2d[i1].b_field_z
    psi2d = ids.time_slice[itime].profiles_2d[i1].psi
    r2d = ids.time_slice[itime].profiles_2d[i1].r

    dpsi2d = np.gradient(psi2d)
    dr2d = np.gradient(r2d)
    dpsi2drdr = dpsi2d[0] / dr2d[0] / r2d

    # todo - reduce num. of data for COCOS discrimination
    #      - compute rtol(s) instead of fixed ones.
    dim2 = ids.time_slice[itime].profiles_2d[i1].grid.dim2
    z_axis = ids.time_slice[itime].global_quantities.magnetic_axis.z
    psi_axis = ids.time_slice[itime].profiles_1d.psi[0]

    # grid of magnetic axis in Z
    iz = np.argmin(np.abs(dim2 - z_axis))
    # psi ref. inside LCFS
    psi_ref = psi_axis + dpsi * 0.5

    # grids close to psi ref.
    rows, cols = np.where((np.isclose(psi2d, psi_ref, rtol=0.25)) & (bz != 0))
    if (not rows.any()) or (not cols.any()):
        raise ValueError("COCOS discrimination failed, len(grids) and/or Bz is zero")

    # discard grids in private flux region)
    w = np.where(np.isclose(cols, iz, rtol=0.1))

    twopi_exp_bp_sigma_rphi_z = np.zeros(bz.shape)
    twopi_exp_bp_sigma_rphi_z = -sigma_bp * dpsi2drdr[rows[w], cols[w]] / bz[rows[w], cols[w]]
    sigma_rphi_z = np.sign(np.sum(np.sign(twopi_exp_bp_sigma_rphi_z)))

    # 6 exp_Bp from Eq.(19)
    x = np.average(twopi_exp_bp_sigma_rphi_z * sigma_rphi_z)
    exp_bp = np.where(np.isclose(x, 2.0 * np.pi, rtol=0.5), 1, 0)

    #
    values = {
        "ipsign": int(ipsign),
        "b0sign": int(b0sign),
        "exp_Bp": int(exp_bp),
        "sigma_Bp": int(sigma_bp),
        "sigma_RphiZ": int(sigma_rphi_z),
        "sigma_rhothetaphi": int(sigma_rhothetaphi),
        "sign_q_pos": int(sign_q_pos),
        "sign_pprime_pos": int(sign_pprime_pos),
    }

    cocos = COCOS(values=values).get()

    return cocos


def ids_compute_cocos(ids, itime=None, i1=0):
    """Function Interface for computing COCOS

    Parameters
    ----------
    ids: IDS
        IDS for cocos estimation
    itime: int|None
        Index of struct_array time_slice in IDS/equilibrium
    i1: int=0
        Index of struct_array profiles_2d in IDS/equilibrium

    Returns
    -------
    cocos: int
        COCOS number computed
    """

    key = "COCOS"

    if ids.metadata.name == "equilibrium":
        try:
            cocos = compute_COCOS(ids, itime, i1)
        except Exception as e:
            logger.debug(f"{e}")
            logger.error(traceback.format_exc())

    else:
        exit(f"equilibrium instead of {ids.metadata.name}")

    return cocos[key]
