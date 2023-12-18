""" 
This module provides compute functions and classes for equilibrium ids data

`more about equilibrium ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/equilibrium.html>`_.

"""
import logging
import numpy as np

logger = logging.getLogger("module")


class EquilibriumCompute:
    """This class provides compute functions for equilibrium ids"""

    def __init__(self, ids: object):
        """Initialization EquilibriumCompute object.

        Args:
            ids : equilibrium ids object
        """
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
                f"equilibrium.time_slice[{timeSlice}].profiles_2d[{profiles2DIndex}] not available"
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

        if np.all(psi2d==0.0):
            logger.error("All values of psi2d are 0. No contour levels were found within the data range, Can not plot contour")
            return None
        if np.size(r2d) != np.size(z2d) or np.size(r2d) != np.size(psi2d):
            logger.error(
                f"r, z and psi have not the same dimension in equilibrium.time_slice[{timeSlice}].profiles_2d[{profiles2DIndex}]"
            )
            return None

        return {"r2d": r2d, "z2d": z2d, "psi2d": psi2d}

    def getRho2D(self, timeSlice: int = 0, profiles2DIndex: int = 0) -> np.ndarray:
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
        profiles2D_phi = None
        try:  # using https://docs.python.org/2/glossary.html#term-eafp style
            profiles2D_phi = (
                self.ids.time_slice[timeSlice].profiles_2d[profiles2DIndex].phi
            )
            if len(profiles2D_phi) == 0:
                raise IndexError
        except IndexError:
            logger.error(
                f"equilibrium.time_slice[{timeSlice}].profiles_2d[{profiles2DIndex}].phi not available"
            )
            return None
        if np.isnan(profiles2D_phi).all() is not True:
            return None
        return np.sqrt(profiles2D_phi / np.amax(profiles2D_phi))

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
