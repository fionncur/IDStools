""" 
* :py:class:`EquilibriumCompute`
This module provides functions and classes for equilibrium ids data


`more about equilibrium ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/equilibrium.html>`_


"""

import numpy as np
import sys


class EquilibriumCompute:
    """This class provides compute functions for equilibrium ids"""

    def __init__(self, ids: object):
        """Initialization EquilibriumCompute object.

        Args:
            ids_object : equilibrium ids object
        """
        super().__init__()
        self.ids = ids

    def get2DCartesianGrid(self, timeSlice: int = 0, profiles2DIndex: int = 0) -> dict:
        """
        This function returns a dictionary containing 2D Cartesian grid coordinates and psi values from
        an equilibrium IDS object.

        Args:
            timeSlice (int): The time slice index of the equilibrium data to be used for generating the 2D Cartesian grid. Defaults to 0
            profiles2DIndex (int): `profiles2DIndex` is an integer parameter that represents the index of the ``profile_2d`` to be used in the calculation. It is used to access the specific 2D profile from the list of profiles in the `time_slice` object. Defaults to 0

        Returns:
            A dictionary containing the 2D Cartesian grid coordinates (r2d and z2d) and the corresponding psi values (psi2d).

        Examples:
            >>> idsobj = EquilibriumCompute()
            >>> a = idsobj.get2DProfiles(timeSlice=0)
            [1,2]

            >>> idsobj = EquilibriumCompute()
            >>> a = idsobj.get2DProfiles(timeSlice=2, gridType=1) # Here gridType is rectangular
            [1,2]
        """
        if len(self.ids.time_slice[timeSlice].profiles_2d) == 0:
            print(
                "The equilibrium IDS is empty: len(equilibrium.time_slice[0].profiles_2d)=0",
                file=sys.stderr,
            )
            return None

        if len(self.ids.time_slice[timeSlice].profiles_2d[profiles2DIndex].psi) < 1:
            print(
                f"equilibrium.time_slice[:].profiles_2d[{profiles2DIndex}].psi could not be read",
                file=sys.stderr,
            )
            return None

        profiles2D = self.ids.time_slice[timeSlice].profiles_2d[profiles2DIndex]
        r2d = profiles2D.r
        z2d = profiles2D.z
        psi2d = profiles2D.psi

        if profiles2D.grid_type.index == 1 and np.size(r2d) == 0:
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

        if np.size(r2d) != np.size(z2d) or np.size(r2d) != np.size(psi2d):
            print(
                f"r, z and psi have not the same dimension in equilibrium.time_slice[{timeSlice}].profiles_2d[{profiles2DIndex}]",
                file=sys.stderr,
            )
            return None

        return {"r2d": r2d, "z2d": z2d, "psi2d": psi2d}

    def getRho2D(self, timeSlice: int = 0, profiles2DIndex: int = 0) -> dict:
        """
        This function calculates rho(R,Z) using toroidal flux  and returns a dictionary containing the result.

        Args:
            timeSlice (int): The time slice is an integer value that represents the index of the time slice in the equilibrium ids. It is used to select a specific time slice for the calculation of rho(R,Z). Defaults to 0
            profiles2DIndex (int): `profiles2DIndex` is an integer parameter that represents the index of  the ``profiles_2d`` to be used for the calculation of rho(R,Z). It is used to access the `profiles_2d` list in the `time_slice` object. Defaults to 0

        Returns:
            a value containing the square root of the toroidal flux values divided by the maximum toroidal flux value, if the length of toroidal flux  is greater than 0. If the length of toroidal flux is less than 1, it returns None.

        Examples:
            >>> idsobj = EquilibriumCompute()
            >>> a = idsobj.get2DProfiles(timeSlice=0)
            [1,2]

            >>> idsobj = EquilibriumCompute()
            >>> a = idsobj.get2DProfiles(timeSlice=2, gridType=1) # Here gridType is rectangular
            [1,2]
        """
        if len(self.ids.time_slice[timeSlice].profiles_2d[profiles2DIndex].phi) < 1:
            print(
                "equilibrium.time_slice[:].profiles_2d[profiles2DIndex].phi could not be read",
                file=sys.stderr,
            )

        profiles2D = self.ids.time_slice[timeSlice].profiles_2d[profiles2DIndex]
        return (
            None
            if len(profiles2D.phi) < 1
            else np.sqrt(profiles2D.phi / np.amax(profiles2D.phi))
        )

    def getBTotal(self, timeSlice: int) -> float:
        """
        This function calculates the total magnetic field strength at a given time slice based on the radial, vertical, and toroidal components of the magnetic field.

        Args:
            timeSlice (int): timeSlice is an integer parameter representing the index of the time slice for which the magnetic field is being calculated from profiles 2D.

        Returns:
            the total magnetic field strength (bTotal) at a given time slice, calculated using the square root of the sum of the squares of the radial, vertical, and toroidal components of the magnetic field. If there are no profiles available for the given time slice, the function returns None.

        Examples:
            >>> idsobj = EquilibriumCompute()
            >>> a = idsobj.get2DProfiles(timeSlice=0)
            [1,2]

            >>> idsobj = EquilibriumCompute()
            >>> a = idsobj.get2DProfiles(timeSlice=2, gridType=1) # Here gridType is rectangular
            [1,2]

        Notes:
            ``profiles_2d`` has information about following fields
            ``b_field_r`` (R component of the poloidal magnetic field)
            ``b_field_r`` (Z component of the poloidal magnetic field)
            ``b_field_tor`` (Toroidal component of the magnetic field)

            `more about equilibrium ids https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/equilibrium.html`_

        """
        listOfProfiles = self.get2DProfiles(timeSlice)
        bTotal = None
        if listOfProfiles is not None:
            profile2dIndex = listOfProfiles[0]
            bTotal = np.sqrt(
                self.ids.time_slice[timeSlice].profiles_2d[profile2dIndex].b_field_r
                ** 2
                + self.ids.time_slice[timeSlice].profiles_2d[profile2dIndex].b_field_z
                ** 2
                + self.ids.time_slice[timeSlice].profiles_2d[profile2dIndex].b_field_tor
                ** 2
            )
        return profile2dIndex, bTotal

    def get2DProfiles(self, timeSlice: int, gridType: int = 1) -> list:
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

            `more about equilibrium ids https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/equilibrium.html`_

        See Also:
            getBTotal : Get total magnetic field

        Examples:
            >>> idsobj = EquilibriumCompute()
            >>> a = idsobj.get2DProfiles(timeSlice=0)
            [1,2]

            >>> idsobj = EquilibriumCompute()
            >>> a = idsobj.get2DProfiles(timeSlice=2, gridType=1) # Here gridType is rectangular
            [1,2]
        """
        return [
            index
            for index in range(len(self.ids.time_slice[timeSlice].profiles_2d))
            if self.ids.time_slice[timeSlice].profiles_2d[index].grid_type.index
            == gridType
        ] or None

    def getFluxSurfaces(self, timeSlice: int) -> dict:
        listOfProfiles = self.get2DProfiles(timeSlice)
        if listOfProfiles is None:
            return None
        profile2dIndex = listOfProfiles[0]
        # Reading in 2d structures
        r2d = np.array(self.ids.time_slice[timeSlice].profiles_2d[profile2dIndex].r)
        z2d = np.array(self.ids.time_slice[timeSlice].profiles_2d[profile2dIndex].z)
        psi2d = np.array(self.ids.time_slice[timeSlice].profiles_2d[profile2dIndex].psi)
        if len(self.ids.time_slice[timeSlice].profiles_2d[profile2dIndex].phi) > 0:
            rho2d = np.sqrt(
                self.ids.time_slice[timeSlice].profiles_2d[profile2dIndex].phi
                / np.amax(
                    self.ids.time_slice[timeSlice].profiles_2d[profile2dIndex].phi
                )
            )
        else:
            rho2d = []

        return {"r2d": r2d, "z2d": z2d, "rho2d": rho2d, "psi2d": psi2d}

    def get_waveform_ip(self):
        """
        This function returns the waveform IP and time array from a given set of time slices.

        Returns:
            two lists: `ip` and `time_array`. The `ip` list contains the negative values of the global quantities `ip` multiplied by 1.0e-6, and the `time_array` list contains the time values from `self.ids.time` corresponding to each `ip` value.
        """

        ntime = len(self.ids.time_slice)
        time_array = []
        ip = []
        for itime in range(ntime):
            time_array.append(self.ids.time[itime])
            ip.append(-self.ids.time_slice[itime].global_quantities.ip * 1.0e-6)

        return ip, time_array

    def get_ip(self):
        ip = []
        ntime = len(self.ids.time_slice)
        for itime in range(ntime):
            ip.append(-self.ids.time_slice[itime].global_quantities.ip * 1.0e-6)
        return ip

    def get_top_view(self, time_index):
        data = {}
        data["r0"] = r0 = self.ids.time_slice[time_index].boundary.geometric_axis.r
        data["amin"] = amin = self.ids.time_slice[time_index].boundary.minor_radius
        data["phit"] = phit = np.linspace(0, 2 * np.pi, 100)
        data["xpla"] = (r0 - amin) * np.cos(phit)
        data["ypla"] = (r0 - amin) * np.sin(phit)
        data["xplap"] = (r0 + amin) * np.cos(phit)
        data["yplap"] = (r0 + amin) * np.sin(phit)
        return data
