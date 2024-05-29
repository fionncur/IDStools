""" 
This module provides compute functions and classes for equilibrium ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging
import os

from typing import Union
from idstools.database import DBMaster

import numpy as np
from imas import imasdef

logger = logging.getLogger("module")


class EquilibriumCompute:
    """This class provides compute functions for equilibrium ids"""

    def __init__(self, ids: object):
        """Initialization EquilibriumCompute object.

        Args:
            ids : equilibrium ids object
        """
        self.ids = ids

    def get2DCartesianGrid(
        self, timeSlice: int = 0, profiles2DIndex: int = 0
    ) -> Union[dict, None]:
        """
        This function returns a dictionary containing 2D Cartesian grid coordinates and psi values from
        an equilibrium IDS object.


        Args:
            timeSlice (int): The time slice index of the equilibrium data to be used for generating the 2D Cartesian grid. Defaults to 0
            profiles2DIndex (int): `profiles2DIndex` is an integer parameter that represents the index of the ``profile_2d`` to be used in the calculation. It is used to access the specific 2D profile from the list of profiles in the `time_slice` object. Defaults to 0

        Returns:
            A dictionary containing the 2D Cartesian grid coordinates (r2d and z2d) and the corresponding psi values (psi2d).

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134173,106,'public')
                connection.open()
                idsObj = connection.get('equilibrium')
                computeObj = EquilibriumCompute(idsObj)
                result = computeObj.get2DCartesianGrid(timeSlice=0)

                {'psi2d': array([[]]),
                'r2d': array([[]]),
                'z2d': array([[]])}
        """
        profiles2D = None
        try:
            profiles2D = self.ids.time_slice[timeSlice].profiles_2d[
                profiles2DIndex
            ]  # using https://docs.python.org/2/glossary.html#term-eafp style
        except IndexError:
            logger.error(
                f"equilibrium.time_slice[{timeSlice}].profiles_2d[{profiles2DIndex}] is not available"
            )
            return None

        profiles2D = self.ids.time_slice[timeSlice].profiles_2d[profiles2DIndex]
        r2d = profiles2D.r
        z2d = profiles2D.z
        psi2d = profiles2D.psi

        if profiles2D.grid_type.index == 1 and np.size(r2d) == 0:
            logger.warning(
                f"profiles_2d[{profiles2DIndex}].r is not available and grid type is 1.. Calculating from grid"
            )
            r1d = profiles2D.grid.dim1
            z1d = profiles2D.grid.dim2
            nr = len(r1d)
            nz = len(z1d)
            r2d = np.empty(shape=(nr, nz))
            z2d = np.empty(shape=(nr, nz))
            for iz in range(nz):
                r2d[:, iz] = r1d
            for ir in range(nr):
                z2d[ir, :] = z1d

        if np.all(psi2d == 0.0):
            logger.error(
                "All values of psi2d are 0. No contour levels were found within the data range, Can not plot contour"
            )
            return None
        if np.size(r2d) != np.size(z2d) or np.size(r2d) != np.size(psi2d):
            logger.error(
                f"r, z and psi have not the same dimension in equilibrium.time_slice[{timeSlice}].profiles_2d[{profiles2DIndex}]"
            )
            return None

        return {"r2d": r2d, "z2d": z2d, "psi2d": psi2d}

    def getRho2D(
        self, timeSlice: int = 0, profiles2DIndex: int = 0
    ) -> Union[np.ndarray, None]:
        """
        This function calculates rho(R,Z) using toroidal flux  and returns a dictionary containing the result.

        Args:
            timeSlice (int): The time slice is an integer value that represents the index of the time slice in the equilibrium ids. It is used to select a specific time slice for the calculation of rho(R,Z). Defaults to 0
            profiles2DIndex (int): `profiles2DIndex` is an integer parameter that represents the index of  the ``profiles_2d`` to be used for the calculation of rho(R,Z). It is used to access the `profiles_2d` list in the `time_slice` object. Defaults to 0

        Returns:
            a value containing the square root of the toroidal flux values divided by the maximum toroidal flux value, if the length of toroidal flux  is greater than 0. If the length of toroidal flux is less than 1, it returns None.

        Examples:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134173,106,'public')
                connection.open()
                idsObj = connection.get('equilibrium')
                computeObj = EquilibriumCompute(idsObj)
                result = computeObj.getRho2D(timeSlice=0)

                array([[]])
        """
        phi = None
        try:  # using https://docs.python.org/2/glossary.html#term-eafp style
            phi = self.ids.time_slice[timeSlice].profiles_2d[profiles2DIndex].phi
            if len(phi) == 0:
                logger.error(
                    f"equilibrium.time_slice[{timeSlice}].profiles_2d[{profiles2DIndex}].phi not available"
                )
                return None
        except IndexError:
            logger.error(
                f"equilibrium.time_slice[{timeSlice}].profiles_2d[{profiles2DIndex}].phi not available"
            )
            return None
        if np.isnan(phi).all() is True:
            logger.error(
                f"all values are nan for equilibrium.time_slice[{timeSlice}].profiles_2d[{profiles2DIndex}].phi "
            )
            return None
        return np.sqrt(phi / np.amax(phi))

    def getBTotal(self, timeSlice: int) -> tuple:
        """
        This function calculates the total magnetic field strength at a given time slice based on the radial, vertical, and toroidal components of the magnetic field.

        Args:
            timeSlice (int): timeSlice is an integer parameter representing the index of the time slice for which the magnetic field is being calculated from profiles 2D.

        Returns:
            Index in `profiles_2d`
            Array of total magnetic field strength (bTotal) at a given time slice, calculated using the square root of the sum of the squares of the radial, vertical, and toroidal components of the magnetic field. If there are no profiles available for the given time slice, the function returns None.

        Examples:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134173,106,'public')
                connection.open()
                idsObj = connection.get('equilibrium')
                computeObj = EquilibriumCompute(idsObj)
                indices = idsobj.getBTotal(timeSlice=0)
                (0, array([[10.99503929

        Notes:

            .. math:: bTotal = \sqrt{b\_field\_r^2 + b\_field\_z^2 + b\_field\_tor^2}

            ``profiles_2d`` has information about following fields
            ``b_field_r`` (R component of the poloidal magnetic field)
            ``b_field_z`` (Z component of the poloidal magnetic field)
            ``b_field_tor`` (Toroidal component of the magnetic field)

        """
        listOfProfiles = self.get2DProfilesIndices(timeSlice)
        bTotal = None
        profile2dIndex = -99

        if listOfProfiles is not None:
            # TODO Check if we should always pick up first profile
            profile2dIndex = listOfProfiles[0]
            bTotal = np.sqrt(
                self.ids.time_slice[timeSlice].profiles_2d[profile2dIndex].b_field_r
                ** 2
                + self.ids.time_slice[timeSlice].profiles_2d[profile2dIndex].b_field_z
                ** 2
                + self.ids.time_slice[timeSlice].profiles_2d[profile2dIndex].b_field_tor
                ** 2
            )
        else:
            print("------------------------------------------------")
            print("No rectangular R,Z grid found in equilibrium IDS")
            print("--> Abort.")
            print("------------------------------------------------")
        return profile2dIndex, bTotal

    def get2DProfilesIndices(self, timeSlice: int, gridType: int = 1) -> list:
        """Return the indices of ``profiles_2d`` of the specified grid type

        Args:
            timeSlice (int): time slice index
            gridType (int, optional): grid type. Defaults to 1.

        Returns:
            list: list of indices of the 2D profiles at a given time slice. If no such 2D profiles are found, it returns None

        Raises:
            AttributeError: The ``Raises`` section is a list of all exceptions that are relevant to the interface.

        Notes:
            Multiple 2D representations of the equilibrium are stored in ``profiles_2d``.
            Various grid types are available like rectangular, inverse etc. read more on profiles_2d(i1) section

        See also:
            :meth:`getFluxSurfaces`
            :meth:`getBTotal`

        Examples:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134173,106,'public')
                connection.open()
                idsObj = connection.get('equilibrium')
                computeObj = EquilibriumCompute(idsObj)
                indices = idsobj.get2DProfilesIndices(timeSlice=0, gridType=1)

                [0]
        """
        return [
            index
            for index in range(len(self.ids.time_slice[timeSlice].profiles_2d))
            if self.ids.time_slice[timeSlice].profiles_2d[index].grid_type.index
            == gridType
        ] or None

    def getFluxSurfaces(self, timeSlice: int) -> dict:
        """
        This function returns a dictionary containing 2D profiles and rho values for a given time slice.

        Args:
            timeSlice (int): The time slice parameter represents the time step at which the flux surfaces are to be calculated.

        Returns:
            a dictionary containing information about flux surfaces at a specific time slice. The dictionary includes a 2D Cartesian grid, a 2D profile index, and a 2D array of rho values. If no profiles are found, the function returns None.
        """
        GRID_TYPE_RECTANGULAR = 1
        listOfProfiles = self.get2DProfilesIndices(timeSlice, GRID_TYPE_RECTANGULAR)
        if listOfProfiles is None:
            return None

        logger.debug(f"list Of rectangualar profiles found : {listOfProfiles}")
        profile2dIndex = listOfProfiles[0]

        resultDict = self.get2DCartesianGrid(timeSlice, profile2dIndex)
        rho2d = self.getRho2D(timeSlice, profile2dIndex)
        if rho2d is None:
            rho2d = []
        resultDict["rho2d"] = rho2d
        return resultDict

    def getIP(self) -> list:
        """
        This function returns a list of Plasma current (toroidal component) values for each time slice.

        Returns:
            a list of plasma currents for each time slice in `self.ids.time_slice`. The plasma current is
        calculated by multiplying the global quantity `ip` by -1.0e-6.

        Examples:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134173,106,'public')
                connection.open()
                idsObj = connection.get('equilibrium')
                computeObj = EquilibriumCompute(idsObj)
                result = computeObj.getIP()

                array([[]])
        """
        return [
            -self.ids.time_slice[timeIndex].global_quantities.ip * 1.0e-6
            for timeIndex in range(len(self.ids.time_slice))
        ]

    def getTopView(self, timeSlice: int = 0) -> dict:
        """
        The function returns data for plotting the top view of a 2D shape.

        Args:
            timeSlice (int): timeSlice is an index of time_slice. If not specified, it defaults to 0. Defaults to 0

        Returns:
            The function `getTopView` returns a dictionary `topViewDict` containing the following keys

            - "r0": the geometric axis r of the boundary at the given `timeSlice`
            - "amin": the minor radius of the boundary at the given `timeSlice`
            - "phit": an array of 100 evenly spaced values between 0 and 2 * pi
            - "xpla": left x-coordinate of a point in polar coordinates
            - "ypla": left y-coordinate of a point in polar coordinates
            - "xplap": right x-coordinate of a point in polar coordinates
            - "yplap": right y-coordinate of a point in polar coordinates

        """
        # TODO Correct documentation and naming of return variables
        topViewDict = {}
        topViewDict["r0"] = r0 = self.ids.time_slice[
            timeSlice
        ].boundary.geometric_axis.r
        topViewDict["amin"] = amin = self.ids.time_slice[
            timeSlice
        ].boundary.minor_radius
        topViewDict["phit"] = phit = np.linspace(0, 2 * np.pi, 100)
        topViewDict["xpla"] = (r0 - amin) * np.cos(phit)
        topViewDict["ypla"] = (r0 - amin) * np.sin(phit)
        topViewDict["xplap"] = (r0 + amin) * np.cos(phit)
        topViewDict["yplap"] = (r0 + amin) * np.sin(phit)
        return topViewDict

    def getmrho(self, timeSlice: int = 0):
        mrho = 0
        for i in range(len(self.ids.time_slice[0].profiles_1d.rho_tor_norm)):
            if self.ids.time_slice[0].profiles_1d.rho_tor_norm[i] < 0:
                mrho = mrho + 1

        return mrho

    def getgm3(self, r, timeSlice: int = 0):
        rho_tor_sep = self.ids.time_slice[timeSlice].profiles_1d.rho_tor[timeSlice]
        gm3 = (
            np.interp(
                r,
                self.ids.time_slice[timeSlice].profiles_1d.rho_tor_norm,
                self.ids.time_slice[timeSlice].profiles_1d.gm3,
            )
            / rho_tor_sep**2
        )
        return gm3

    def getgm7(self, r, timeSlice: int = 0):
        rho_tor_sep = self.ids.time_slice[timeSlice].profiles_1d.rho_tor[timeSlice]
        gm7 = (
            np.interp(
                r,
                self.ids.time_slice[timeSlice].profiles_1d.rho_tor_norm,
                self.ids.time_slice[timeSlice].profiles_1d.gm7,
            )
            / rho_tor_sep
        )
        return gm7

    def rescale(self, rescaleFactor):
        """Rescale the magnetic field in an equilibrium
        Args:
            equil (equilibrium IDS): initial equilibrium
            rescaleFactor (float): rescaling factor for magnetic field
        Returns:
            equilibrium IDS: rescaled equilibrium
        """
        import distutils.version as version
        from copy import deepcopy

        try:
            dd_version = self.ids.ids_properties.version_put.data_dictionary
        except Exception as e:
            dd_version = "0.0.0"

        equout = deepcopy(self.ids)

        imas_version = DBMaster.getDDVersion()

        equout.ids_properties.version_put.data_dictionary = imas_version

        for itime in range(len(self.ids.vacuum_toroidal_field.b0)):
            equout.vacuum_toroidal_field.b0[itime] = (
                self.ids.vacuum_toroidal_field.b0[itime] * rescaleFactor
            )

        for itime in range(len(self.ids.time_slice)):
            if imasdef.isFieldValid(self.ids.time_slice[itime].boundary.psi):
                equout.time_slice[itime].boundary.psi = (
                    self.ids.time_slice[itime].boundary.psi * rescaleFactor
                )

            if imasdef.isFieldValid(self.ids.time_slice[itime].boundary_separatrix.psi):
                equout.time_slice[itime].boundary_separatrix.psi = (
                    self.ids.time_slice[itime].boundary_separatrix.psi * rescaleFactor
                )

            if version.StrictVersion(dd_version) > version.StrictVersion("3.31.0"):
                if imasdef.isFieldValid(
                    self.ids.time_slice[itime].boundary_secondary_separatrix.psi
                ):
                    equout.time_slice[itime].boundary_secondary_separatrix.psi = (
                        self.ids.time_slice[itime].boundary_secondary_separatrix.psi
                        * rescaleFactor
                    )

            if imasdef.isFieldValid(
                self.ids.time_slice[itime].constraints.b_field_tor_vacuum_r.measured
            ):
                equout.time_slice[itime].constraints.b_field_tor_vacuum_r.measured = (
                    self.ids.time_slice[itime].constraints.b_field_tor_vacuum_r.measured
                    * rescaleFactor
                )

            if imasdef.isFieldValid(
                self.ids.time_slice[
                    itime
                ].constraints.b_field_tor_vacuum_r.reconstructed
            ):
                equout.time_slice[
                    itime
                ].constraints.b_field_tor_vacuum_r.reconstructed = (
                    self.ids.time_slice[
                        itime
                    ].constraints.b_field_tor_vacuum_r.reconstructed
                    * rescaleFactor
                )

            for i1 in range(len(self.ids.time_slice[itime].constraints.bpol_probe)):
                equout.time_slice[itime].constraints.bpol_probe[i1].measured = (
                    self.ids.time_slice[itime].constraints.bpol_probe[i1].measured
                    * rescaleFactor
                )
                equout.time_slice[itime].constraints.bpol_probe[i1].reconstructed = (
                    self.ids.time_slice[itime].constraints.bpol_probe[i1].reconstructed
                    * rescaleFactor
                )

            if imasdef.isFieldValid(
                self.ids.time_slice[itime].constraints.diamagnetic_flux.measured
            ):
                equout.time_slice[itime].constraints.diamagnetic_flux.measured = (
                    self.ids.time_slice[itime].constraints.diamagnetic_flux.measured
                    * rescaleFactor
                )

            if imasdef.isFieldValid(
                self.ids.time_slice[itime].constraints.diamagnetic_flux.reconstructed
            ):
                equout.time_slice[itime].constraints.diamagnetic_flux.reconstructed = (
                    self.ids.time_slice[
                        itime
                    ].constraints.diamagnetic_flux.reconstructed
                    * rescaleFactor
                )

            for i1 in range(len(self.ids.time_slice[itime].constraints.faraday_angle)):
                equout.time_slice[itime].constraints.faraday_angle[i1].measured = (
                    self.ids.time_slice[itime].constraints.faraday_angle[i1].measured
                    * rescaleFactor
                )
                equout.time_slice[itime].constraints.faraday_angle[i1].reconstructed = (
                    self.ids.time_slice[itime]
                    .constraints.faraday_angle[i1]
                    .reconstructed
                    * rescaleFactor
                )

            for i1 in range(len(self.ids.time_slice[itime].constraints.flux_loop)):
                equout.time_slice[itime].constraints.flux_loop[i1].measured = (
                    self.ids.time_slice[itime].constraints.flux_loop[i1].measured
                    * rescaleFactor
                )
                equout.time_slice[itime].constraints.flux_loop[i1].reconstructed = (
                    self.ids.time_slice[itime].constraints.flux_loop[i1].reconstructed
                    * rescaleFactor
                )

            if imasdef.isFieldValid(self.ids.time_slice[itime].constraints.ip.measured):
                equout.time_slice[itime].constraints.ip.imeasured = (
                    self.ids.time_slice[itime].constraints.ip.measured * rescaleFactor
                )

            if imasdef.isFieldValid(
                self.ids.time_slice[itime].constraints.ip.reconstructed
            ):
                equout.time_slice[itime].constraints.ip.reconstructed = (
                    self.ids.time_slice[itime].constraints.ip.reconstructed
                    * rescaleFactor
                )

            if imasdef.isFieldValid(self.ids.time_slice[itime].global_quantities.ip):
                equout.time_slice[itime].global_quantities.ip = (
                    self.ids.time_slice[itime].global_quantities.ip * rescaleFactor
                )

            if imasdef.isFieldValid(
                self.ids.time_slice[itime].global_quantities.psi_axis
            ):
                equout.time_slice[itime].global_quantities.psi_axis = (
                    self.ids.time_slice[itime].global_quantities.psi_axis
                    * rescaleFactor
                )

            if imasdef.isFieldValid(
                self.ids.time_slice[itime].global_quantities.psi_boundary
            ):
                equout.time_slice[itime].global_quantities.psi_boundary = (
                    self.ids.time_slice[itime].global_quantities.psi_boundary
                    * rescaleFactor
                )

            if imasdef.isFieldValid(
                self.ids.time_slice[itime].global_quantities.magnetic_axis.b_field_tor
            ):
                equout.time_slice[itime].global_quantities.magnetic_axis.b_field_tor = (
                    self.ids.time_slice[
                        itime
                    ].global_quantities.magnetic_axis.b_field_tor
                    * rescaleFactor
                )

            if version.StrictVersion(dd_version) > version.StrictVersion("3.14.0"):
                if imasdef.isFieldValid(
                    self.ids.time_slice[itime].global_quantities.energy_mhd
                ):
                    equout.time_slice[itime].global_quantities.energy_mhd = (
                        self.ids.time_slice[itime].global_quantities.energy_mhd
                        * rescaleFactor**2
                    )
            else:
                if imasdef.isFieldValid(
                    self.ids.time_slice[itime].global_quantities.w_mhd
                ):
                    equout.time_slice[itime].global_quantities.energy_mhd = (
                        self.ids.time_slice[itime].global_quantities.w_mhd
                        * rescaleFactor**2
                    )

            if version.StrictVersion(dd_version) > version.StrictVersion("3.31.0"):
                if imasdef.isFieldValid(
                    self.ids.time_slice[itime].global_quantities.psi_external_average
                ):
                    equout.time_slice[itime].global_quantities.psi_external_average = (
                        self.ids.time_slice[
                            itime
                        ].global_quantities.psi_external_average
                        * rescaleFactor
                    )

            for i1d in range(len(self.ids.time_slice[itime].profiles_1d.psi)):
                equout.time_slice[itime].profiles_1d.psi[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.psi[i1d] * rescaleFactor
                )

            for i1d in range(len(self.ids.time_slice[itime].profiles_1d.phi)):
                equout.time_slice[itime].profiles_1d.phi[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.phi[i1d] * rescaleFactor
                )

            for i1d in range(len(self.ids.time_slice[itime].profiles_1d.pressure)):
                equout.time_slice[itime].profiles_1d.pressure[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.pressure[i1d]
                    * rescaleFactor**2
                )

            for i1d in range(len(self.ids.time_slice[itime].profiles_1d.f)):
                equout.time_slice[itime].profiles_1d.f[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.f[i1d] * rescaleFactor
                )

            for i1d in range(
                len(self.ids.time_slice[itime].profiles_1d.dpressure_dpsi)
            ):
                equout.time_slice[itime].profiles_1d.dpressure_dpsi[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.dpressure_dpsi[i1d]
                    * rescaleFactor
                )

            for i1d in range(len(self.ids.time_slice[itime].profiles_1d.f_df_dpsi)):
                equout.time_slice[itime].profiles_1d.f_df_dpsi[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.f_df_dpsi[i1d]
                    * rescaleFactor
                )

            for i1d in range(len(self.ids.time_slice[itime].profiles_1d.j_tor)):
                equout.time_slice[itime].profiles_1d.j_tor[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.j_tor[i1d] * rescaleFactor
                )

            for i1d in range(len(self.ids.time_slice[itime].profiles_1d.j_parallel)):
                equout.time_slice[itime].profiles_1d.j_parallel[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.j_parallel[i1d]
                    * rescaleFactor
                )

            for i1d in range(len(self.ids.time_slice[itime].profiles_1d.dpsi_drho_tor)):
                equout.time_slice[itime].profiles_1d.dpsi_drho_tor[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.dpsi_drho_tor[i1d]
                    * rescaleFactor
                )

            for i1d in range(len(self.ids.time_slice[itime].profiles_1d.dvolume_dpsi)):
                equout.time_slice[itime].profiles_1d.dvolume_dpsi[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.dvolume_dpsi[i1d]
                    / rescaleFactor
                )

            for i1d in range(len(self.ids.time_slice[itime].profiles_1d.darea_dpsi)):
                equout.time_slice[itime].profiles_1d.darea_dpsi[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.darea_dpsi[i1d]
                    / rescaleFactor
                )

            for i1d in range(len(self.ids.time_slice[itime].profiles_1d.gm4)):
                equout.time_slice[itime].profiles_1d.gm4[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.gm4[i1d] / rescaleFactor**2
                )

            for i1d in range(len(self.ids.time_slice[itime].profiles_1d.gm5)):
                equout.time_slice[itime].profiles_1d.gm5[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.gm5[i1d] * rescaleFactor**2
                )

            for i1d in range(len(self.ids.time_slice[itime].profiles_1d.gm6)):
                equout.time_slice[itime].profiles_1d.gm6[i1d] = (
                    self.ids.time_slice[itime].profiles_1d.gm6[i1d] / rescaleFactor**2
                )

            if version.StrictVersion(dd_version) > version.StrictVersion("3.5.0"):
                for i1d in range(
                    len(self.ids.time_slice[itime].profiles_1d.b_field_average)
                ):
                    equout.time_slice[itime].profiles_1d.b_field_average[i1d] = (
                        self.ids.time_slice[itime].profiles_1d.b_field_average[i1d]
                        * rescaleFactor
                    )
            else:
                for i1d in range(len(self.ids.time_slice[itime].profiles_1d.b_average)):
                    equout.time_slice[itime].profiles_1d.b_field_average[i1d] = (
                        abs(self.ids.time_slice[itime].profiles_1d.b_average[i1d])
                        * rescaleFactor
                    )

            if version.StrictVersion(dd_version) > version.StrictVersion("3.5.0"):
                for i1d in range(
                    len(self.ids.time_slice[itime].profiles_1d.b_field_min)
                ):
                    equout.time_slice[itime].profiles_1d.b_field_min[i1d] = (
                        self.ids.time_slice[itime].profiles_1d.b_field_min[i1d]
                        * rescaleFactor
                    )
            else:
                for i1d in range(len(self.ids.time_slice[itime].profiles_1d.b_min)):
                    equout.time_slice[itime].profiles_1d.b_field_min[i1d] = (
                        abs(self.ids.time_slice[itime].profiles_1d.b_min[i1d])
                        * rescaleFactor
                    )

            if version.StrictVersion(dd_version) > version.StrictVersion("3.5.0"):
                for i1d in range(
                    len(self.ids.time_slice[itime].profiles_1d.b_field_max)
                ):
                    equout.time_slice[itime].profiles_1d.b_field_max[i1d] = (
                        self.ids.time_slice[itime].profiles_1d.b_field_max[i1d]
                        * rescaleFactor
                    )
            else:
                for i1d in range(len(self.ids.time_slice[itime].profiles_1d.b_max)):
                    equout.time_slice[itime].profiles_1d.b_field_max[i1d] = (
                        abs(self.ids.time_slice[itime].profiles_1d.b_max[i1d])
                        * rescaleFactor
                    )

            for i2d in range(len(self.ids.time_slice[itime].profiles_2d)):
                for ir in range(len(self.ids.time_slice[itime].profiles_2d[i2d].psi)):
                    for iz in range(
                        len(self.ids.time_slice[itime].profiles_2d[i2d].psi[ir])
                    ):
                        equout.time_slice[itime].profiles_2d[i2d].psi[ir][iz] = (
                            self.ids.time_slice[itime].profiles_2d[i2d].psi[ir][iz]
                            * rescaleFactor
                        )

                for ir in range(len(self.ids.time_slice[itime].profiles_2d[i2d].phi)):
                    for iz in range(
                        len(self.ids.time_slice[itime].profiles_2d[i2d].phi[ir])
                    ):
                        equout.time_slice[itime].profiles_2d[i2d].phi[ir][iz] = (
                            self.ids.time_slice[itime].profiles_2d[i2d].phi[ir][iz]
                            * rescaleFactor
                        )

                for ir in range(len(self.ids.time_slice[itime].profiles_2d[i2d].j_tor)):
                    for iz in range(
                        len(self.ids.time_slice[itime].profiles_2d[i2d].j_tor[ir])
                    ):
                        equout.time_slice[itime].profiles_2d[i2d].j_tor[ir][iz] = (
                            self.ids.time_slice[itime].profiles_2d[i2d].j_tor[ir][iz]
                            * rescaleFactor
                        )

                for ir in range(
                    len(self.ids.time_slice[itime].profiles_2d[i2d].j_parallel)
                ):
                    for iz in range(
                        len(self.ids.time_slice[itime].profiles_2d[i2d].j_parallel[ir])
                    ):
                        equout.time_slice[itime].profiles_2d[i2d].j_parallel[ir][iz] = (
                            self.ids.time_slice[itime]
                            .profiles_2d[i2d]
                            .j_parallel[ir][iz]
                            * rescaleFactor
                        )

                if version.StrictVersion(dd_version) > version.StrictVersion("3.5.0"):
                    for ir in range(
                        len(self.ids.time_slice[itime].profiles_2d[i2d].b_field_r)
                    ):
                        for iz in range(
                            len(
                                self.ids.time_slice[itime]
                                .profiles_2d[i2d]
                                .b_field_r[ir]
                            )
                        ):
                            equout.time_slice[itime].profiles_2d[i2d].b_field_r[ir][
                                iz
                            ] = (
                                self.ids.time_slice[itime]
                                .profiles_2d[i2d]
                                .b_field_r[ir][iz]
                                * rescaleFactor
                            )
                else:
                    for ir in range(
                        len(self.ids.time_slice[itime].profiles_2d[i2d].b_r)
                    ):
                        for iz in range(
                            len(self.ids.time_slice[itime].profiles_2d[i2d].b_r[ir])
                        ):
                            equout.time_slice[itime].profiles_2d[i2d].b_field_r[ir][
                                iz
                            ] = (
                                self.ids.time_slice[itime].profiles_2d[i2d].b_r[ir][iz]
                                * rescaleFactor
                            )

                if version.StrictVersion(dd_version) > version.StrictVersion("3.5.0"):
                    for ir in range(
                        len(self.ids.time_slice[itime].profiles_2d[i2d].b_field_z)
                    ):
                        for iz in range(
                            len(
                                self.ids.time_slice[itime]
                                .profiles_2d[i2d]
                                .b_field_z[ir]
                            )
                        ):
                            equout.time_slice[itime].profiles_2d[i2d].b_field_z[ir][
                                iz
                            ] = (
                                self.ids.time_slice[itime]
                                .profiles_2d[i2d]
                                .b_field_z[ir][iz]
                                * rescaleFactor
                            )
                else:
                    for ir in range(
                        len(self.ids.time_slice[itime].profiles_2d[i2d].b_z)
                    ):
                        for iz in range(
                            len(self.ids.time_slice[itime].profiles_2d[i2d].b_z[ir])
                        ):
                            equout.time_slice[itime].profiles_2d[i2d].b_field_z[ir][
                                iz
                            ] = (
                                self.ids.time_slice[itime].profiles_2d[i2d].b_z[ir][iz]
                                * rescaleFactor
                            )

                if version.StrictVersion(dd_version) > version.StrictVersion("3.5.0"):
                    for ir in range(
                        len(self.ids.time_slice[itime].profiles_2d[i2d].b_field_tor)
                    ):
                        for iz in range(
                            len(
                                self.ids.time_slice[itime]
                                .profiles_2d[i2d]
                                .b_field_tor[ir]
                            )
                        ):
                            equout.time_slice[itime].profiles_2d[i2d].b_field_tor[ir][
                                iz
                            ] = (
                                self.ids.time_slice[itime]
                                .profiles_2d[i2d]
                                .b_field_tor[ir][iz]
                                * rescaleFactor
                            )
                else:
                    for ir in range(
                        len(self.ids.time_slice[itime].profiles_2d[i2d].b_tor)
                    ):
                        for iz in range(
                            len(self.ids.time_slice[itime].profiles_2d[i2d].b_tor[ir])
                        ):
                            equout.time_slice[itime].profiles_2d[i2d].b_field_tor[ir][
                                iz
                            ] = (
                                self.ids.time_slice[itime]
                                .profiles_2d[i2d]
                                .b_tor[ir][iz]
                                * rescaleFactor
                            )

            for iggd in range(len(self.ids.time_slice[itime].ggd)):
                for i2 in range(len(self.ids.time_slice[itime].ggd[iggd].psi)):
                    for i in range(
                        len(self.ids.time_slice[itime].ggd[iggd].psi[i2].values)
                    ):
                        equout.time_slice[itime].ggd[iggd].psi[i2].values[i] = (
                            self.ids.time_slice[itime].ggd[iggd].psi[i2].values[i]
                            * rescaleFactor
                        )
                        for j in range(
                            len(self.ids.time_slice[itime].ggd[iggd].psi[i2].values[i])
                        ):
                            equout.time_slice[itime].ggd[iggd].psi[i2].coefficients[i][
                                j
                            ] = (
                                self.ids.time_slice[itime]
                                .ggd[iggd]
                                .psi[i2]
                                .coefficients[i][j]
                                * rescaleFactor
                            )

                    for i in range(
                        len(self.ids.time_slice[itime].ggd[iggd].phi[i2].values)
                    ):
                        equout.time_slice[itime].ggd[iggd].phi[i2].values[i] = (
                            self.ids.time_slice[itime].ggd[iggd].phi[i2].values[i]
                            * rescaleFactor
                        )
                        for j in range(
                            len(self.ids.time_slice[itime].ggd[iggd].phi[i2].values[i])
                        ):
                            equout.time_slice[itime].ggd[iggd].phi[i2].coefficients[i][
                                j
                            ] = (
                                self.ids.time_slice[itime]
                                .ggd[iggd]
                                .phi[i2]
                                .coefficients[i][j]
                                * rescaleFactor
                            )

                    for i in range(
                        len(self.ids.time_slice[itime].ggd[iggd].j_tor[i2].values)
                    ):
                        equout.time_slice[itime].ggd[iggd].j_tor[i2].values[i] = (
                            self.ids.time_slice[itime].ggd[iggd].j_tor[i2].values[i]
                            * rescaleFactor
                        )
                        for j in range(
                            len(
                                self.ids.time_slice[itime].ggd[iggd].j_tor[i2].values[i]
                            )
                        ):
                            equout.time_slice[itime].ggd[iggd].j_tor[i2].coefficients[
                                i
                            ][j] = (
                                self.ids.time_slice[itime]
                                .ggd[iggd]
                                .j_tor[i2]
                                .coefficients[i][j]
                                * rescaleFactor
                            )

                    for i in range(
                        len(self.ids.time_slice[itime].ggd[iggd].j_parallel[i2].values)
                    ):
                        equout.time_slice[itime].ggd[iggd].j_parallel[i2].values[i] = (
                            self.ids.time_slice[itime]
                            .ggd[iggd]
                            .j_parallel[i2]
                            .values[i]
                            * rescaleFactor
                        )
                        for j in range(
                            len(
                                self.ids.time_slice[itime]
                                .ggd[iggd]
                                .j_parallel[i2]
                                .values[i]
                            )
                        ):
                            equout.time_slice[itime].ggd[iggd].j_parallel[
                                i2
                            ].coefficients[i][j] = (
                                self.ids.time_slice[itime]
                                .ggd[iggd]
                                .j_parallel[i2]
                                .coefficients[i][j]
                                * rescaleFactor
                            )

                    for i in range(
                        len(self.ids.time_slice[itime].ggd[iggd].b_field_r[i2].values)
                    ):
                        equout.time_slice[itime].ggd[iggd].b_field_r[i2].values[i] = (
                            self.ids.time_slice[itime].ggd[iggd].b_field_r[i2].values[i]
                            * rescaleFactor
                        )
                        for j in range(
                            len(
                                self.ids.time_slice[itime]
                                .ggd[iggd]
                                .b_field_r[i2]
                                .values[i]
                            )
                        ):
                            equout.time_slice[itime].ggd[iggd].b_field_r[
                                i2
                            ].coefficients[i][j] = (
                                self.ids.time_slice[itime]
                                .ggd[iggd]
                                .b_field_r[i2]
                                .coefficients[i][j]
                                * rescaleFactor
                            )

                    for i in range(
                        len(self.ids.time_slice[itime].ggd[iggd].b_field_z[i2].values)
                    ):
                        equout.time_slice[itime].ggd[iggd].b_field_z[i2].values[i] = (
                            self.ids.time_slice[itime].ggd[iggd].b_field_z[i2].values[i]
                            * rescaleFactor
                        )
                        for j in range(
                            len(
                                self.ids.time_slice[itime]
                                .ggd[iggd]
                                .b_field_z[i2]
                                .values[i]
                            )
                        ):
                            equout.time_slice[itime].ggd[iggd].b_field_z[
                                i2
                            ].coefficients[i][j] = (
                                self.ids.time_slice[itime]
                                .ggd[iggd]
                                .b_field_z[i2]
                                .coefficients[i][j]
                                * rescaleFactor
                            )

                    for i in range(
                        len(self.ids.time_slice[itime].ggd[iggd].b_field_tor[i2].values)
                    ):
                        equout.time_slice[itime].ggd[iggd].b_field_tor[i2].values[i] = (
                            self.ids.time_slice[itime]
                            .ggd[iggd]
                            .b_field_tor[i2]
                            .values[i]
                            * rescaleFactor
                        )
                        for j in range(
                            len(
                                self.ids.time_slice[itime]
                                .ggd[iggd]
                                .b_field_tor[i2]
                                .values[i]
                            )
                        ):
                            equout.time_slice[itime].ggd[iggd].b_field_tor[
                                i2
                            ].coefficients[i][j] = (
                                self.ids.time_slice[itime]
                                .ggd[iggd]
                                .b_field_tor[i2]
                                .coefficients[i][j]
                                * rescaleFactor
                            )

        equout.ids_properties.comment = (
            self.ids.ids_properties.comment
            + " (field rescaled by "
            + str(rescaleFactor)
            + ")"
        )
        return equout

    def z_shift(self, shift):
        """Rigidly shift an equilibrium
        Args:
            equil (equilibrium IDS): initial equilibrium
            shift (float): vertical shift in meters
        Returns:
            equilibrium IDS: vertically shifted equilibrium
        """
        import distutils.version as version
        from copy import deepcopy

        equout = deepcopy(self.ids)
        for itime in range(len(self.ids.time_slice)):
            for iz in range(len(self.ids.time_slice[itime].boundary.outline.z)):
                equout.time_slice[itime].boundary.outline.z[iz] = (
                    self.ids.time_slice[itime].boundary.outline.z[iz] + shift
                )

            for iz in range(len(self.ids.time_slice[itime].boundary.lcfs.z)):
                equout.time_slice[itime].boundary.lcfs.z[iz] = (
                    self.ids.time_slice[itime].boundary.lcfs.z[iz] + shift
                )
            equout.time_slice[itime].boundary.geometric_axis.z = (
                self.ids.time_slice[itime].boundary.geometric_axis.z + shift
            )

            for ixpt in range(len(self.ids.time_slice[itime].boundary.x_point)):
                equout.time_slice[itime].boundary.x_point[ixpt].z = (
                    self.ids.time_slice[itime].boundary.x_point[ixpt].z + shift
                )

            for istr in range(len(self.ids.time_slice[itime].boundary.strike_point)):
                equout.time_slice[itime].boundary.strike_point[istr].z = (
                    self.ids.time_slice[itime].boundary.strike_point[istr].z + shift
                )
            equout.time_slice[itime].boundary.active_limiter_point.z = (
                self.ids.time_slice[itime].boundary.active_limiter_point.z + shift
            )

            for iz in range(
                len(self.ids.time_slice[itime].boundary_separatrix.outline.z)
            ):
                equout.time_slice[itime].boundary_separatrix.outline.z[iz] = (
                    self.ids.time_slice[itime].boundary_separatrix.outline.z[iz] + shift
                )
            equout.time_slice[itime].boundary_separatrix.geometric_axis.z = (
                self.ids.time_slice[itime].boundary_separatrix.geometric_axis.z + shift
            )

            for ixpt in range(
                len(self.ids.time_slice[itime].boundary_separatrix.x_point)
            ):
                equout.time_slice[itime].boundary_separatrix.x_point[ixpt].z = (
                    self.ids.time_slice[itime].boundary_separatrix.x_point[ixpt].z
                    + shift
                )

            for istr in range(
                len(self.ids.time_slice[itime].boundary_separatrix.strike_point)
            ):
                equout.time_slice[itime].boundary_separatrix.strike_point[istr].z = (
                    self.ids.time_slice[itime].boundary_separatrix.strike_point[istr].z
                    + shift
                )
            equout.time_slice[itime].boundary_separatrix.active_limiter_point.z = (
                self.ids.time_slice[itime].boundary_separatrix.active_limiter_point.z
                + shift
            )
            equout.time_slice[itime].boundary_separatrix.closest_wall_point.z = (
                self.ids.time_slice[itime].boundary_separatrix.closest_wall_point.z
                + shift
            )
            equout.time_slice[itime].boundary_separatrix.dr_dz_zero_point.z = (
                self.ids.time_slice[itime].boundary_separatrix.dr_dz_zero_point.z
                + shift
            )

            for iz in range(
                len(self.ids.time_slice[itime].boundary_secondary_separatrix.outline.z)
            ):
                equout.time_slice[itime].boundary_secondary_separatrix.outline.z[iz] = (
                    self.ids.time_slice[itime].boundary_secondary_separatrix.outline.z[
                        iz
                    ]
                    + shift
                )

            for ixpt in range(
                len(self.ids.time_slice[itime].boundary_secondary_separatrix.x_point)
            ):
                equout.time_slice[itime].boundary_secondary_separatrix.x_point[
                    ixpt
                ].z = (
                    self.ids.time_slice[itime]
                    .boundary_secondary_separatrix.x_point[ixpt]
                    .z
                    + shift
                )

            for istr in range(
                len(
                    self.ids.time_slice[
                        itime
                    ].boundary_secondary_separatrix.strike_point
                )
            ):
                equout.time_slice[itime].boundary_secondary_separatrix.strike_point[
                    istr
                ].z = (
                    self.ids.time_slice[itime]
                    .boundary_secondary_separatrix.strike_point[istr]
                    .z
                    + shift
                )

            for iq in range(len(self.ids.time_slice[itime].constraints.q)):
                equout.time_slice[itime].constraints.q[iq].position.z = (
                    self.ids.time_slice[itime].constraints.q[iq].position.z + shift
                )

            for ixpt in range(len(self.ids.time_slice[itime].constraints.x_point)):
                equout.time_slice[itime].constraints.x_point[
                    ixpt
                ].position_measured.z = (
                    self.ids.time_slice[itime]
                    .constraints.x_point[ixpt]
                    .position_measured.z
                    + shift
                )
                equout.time_slice[itime].constraints.x_point[
                    ixpt
                ].position_reconstructed.z = (
                    self.ids.time_slice[itime]
                    .constraints.x_point[ixpt]
                    .position_reconstructed.z
                    + shift
                )

            for istr in range(len(self.ids.time_slice[itime].constraints.strike_point)):
                equout.time_slice[itime].constraints.strike_point[
                    istr
                ].position_measured.z = (
                    self.ids.time_slice[itime]
                    .constraints.strike_point[istr]
                    .position_measured.z
                    + shift
                )
            equout.time_slice[itime].global_quantities.magnetic_axis.z = (
                self.ids.time_slice[itime].global_quantities.magnetic_axis.z + shift
            )

            for iz in range(
                len(self.ids.time_slice[itime].profiles_1d.geometric_axis.z)
            ):
                equout.time_slice[itime].profiles_1d.geometric_axis.z[iz] = (
                    self.ids.time_slice[itime].profiles_1d.geometric_axis.z[iz] + shift
                )

            for i2d in range(len(self.ids.time_slice[itime].profiles_2d)):
                if self.ids.time_slice[itime].profiles_2d[i2d].grid_type == 1:
                    for iz in range(
                        len(self.ids.time_slice[itime].profiles_2d[i2d].grid.dim2)
                    ):
                        equout.time_slice[itime].profiles_2d[i2d].grid.dim2[iz] = (
                            self.ids.time_slice[itime].profiles_2d[i2d].grid.dim2[iz]
                            + shift
                        )

                for i1 in range(len(self.ids.time_slice[itime].profiles_2d[i2d].z)):
                    for i2 in range(
                        len(self.ids.time_slice[itime].profiles_2d[i2d].z[i1])
                    ):
                        equout.time_slice[itime].profiles_2d[i2d].z[i1][i2] = (
                            self.ids.time_slice[itime].profiles_2d[i2d].z[i1][i2]
                            + shift
                        )

            for iggd in range(len(self.ids.time_slice[itime].ggd)):
                for iz in range(len(self.ids.time_slice[itime].ggd[iggd].z)):
                    for i in range(
                        len(self.ids.time_slice[itime].ggd[iggd].z[iz].values)
                    ):
                        equout.time_slice[itime].ggd[iggd].z[iz].values[i] = (
                            self.ids.time_slice[itime].ggd[iggd].z[iz].values[i] + shift
                        )

            if self.ids.time_slice[itime].coordinate_system.grid_type == 1:
                for iz in range(
                    len(self.ids.time_slice[itime].coordinate_system.grid.dim2)
                ):
                    equout.time_slice[itime].coordinate_system.grid.dim2[iz] = (
                        self.ids.time_slice[itime].coordinate_system.grid.dim2[iz]
                        + shift
                    )

            for i1 in range(len(self.ids.time_slice[itime].coordinate_system.z)):
                for i2 in range(
                    len(self.ids.time_slice[itime].coordinate_system.z[i1])
                ):
                    equout.time_slice[itime].coordinate_system.z[i1][i2] = (
                        self.ids.time_slice[itime].coordinate_system.z[i1][i2] + shift
                    )

        equout.ids_properties.comment = (
            self.ids.ids_properties.comment
            + " (shifted vertically by "
            + str(shift)
            + " m)"
        )
        return equout

    # def getEquilibriumQuantities(self):
    #     """
    #     The function "getEquilibriumQuantities" returns a dictionary containing the 2D profiles of r, z,  and psi.

    #     Returns:
    #         a dictionary with keys "r2d", "z2d", and "psi2d", and their corresponding values are the  variables r2d, z2d, and psi2d, respectively.
    #     """
    #     r2d   = self.ids.time_slice[0].profiles_2d[0].r
    #     z2d   = self.ids.time_slice[0].profiles_2d[0].z
    #     psi2d = self.ids.time_slice[0].profiles_2d[0].psi

    #     return({"r2d":r2d, "z2d", z2d, "psi2d", psi2d})
