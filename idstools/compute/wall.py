import logging
import time

import numpy as np

from idstools.utils.utility_functions import get_slice_from_array

logger = logging.getLogger(f"module.{__name__}")


def timeit_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function {func.__name__} took {elapsed_time:.4f} seconds")
        return result

    return wrapper


class WallCompute:
    def __init__(self, ids_object):
        self.ids_object = ids_object

    def get_vessel_units(self, select_description2d=":", select_unit=":", name_filter=None):
        """
        Retrieve vessel units information from the IDS object.

        Parameters
        ----------
        select_description2d : str, optional
            A slice notation string to filter the description_2d list. Default is ":".
        select_unit : str, optional
            A slice notation string to filter the units list. Default is ":".
        name_filter : str, optional
            A string to filter units by name or identifier. Default is None.

        Returns
        -------
        dict
            A dictionary containing information about the vessel units.
            The keys are the indices of the description_2d elements, and the values
            are dictionaries containing the name, description, and vessel units information.
        """
        description_2ds = list(self.ids_object.description_2d)
        if select_description2d is not None:
            description_2ds = get_slice_from_array(description_2ds, select_description2d)
        description2d_infos = {}
        for description2d_index, description2d in enumerate(description_2ds):
            description2d_info = {}
            description2d_info["name"] = description2d.type.name
            description2d_info["description"] = description2d.type.description

            units = list(description2d.vessel.unit)
            if select_unit is not None:
                units = get_slice_from_array(units, select_unit)
            unit_infos = {}
            if units:
                for v_unit_index, v_unit in enumerate(units):
                    unit_info = {}

                    unit_info["name"] = v_unit.name
                    if hasattr(v_unit, "identifier"):
                        unit_info["identifier"] = v_unit.identifier
                    else:
                        unit_info["identifier"] = ""
                    if hasattr(v_unit, "description"):
                        unit_info["description"] = v_unit.description
                    else:
                        unit_info["description"] = ""
                    if not v_unit.annular.centreline.r.has_value:
                        logger.warning(
                            f"{description2d_info['name']}-{unit_info['name']} has empty annular.centreline.r"
                        )
                    unit_info["r"] = v_unit.annular.centreline.r
                    if not v_unit.annular.centreline.z.has_value:
                        logger.warning(
                            f"{description2d_info['name']}-{unit_info['name']} has empty annular.centreline.z"
                        )
                    unit_info["z"] = v_unit.annular.centreline.z
                    if not v_unit.annular.thickness.has_value:
                        logger.warning(f"{description2d_info['name']}-{unit_info['name']} has empty annular.thickness")
                    unit_info["h"] = v_unit.annular.thickness
                    if hasattr(v_unit.annular.centreline, "closed"):
                        unit_info["closed"] = v_unit.annular.centreline.closed
                        if v_unit.annular.centreline.closed:
                            unit_info["r"] = np.append(unit_info["r"], unit_info["r"][0])
                            unit_info["z"] = np.append(unit_info["z"], unit_info["z"][0])
                    else:
                        unit_info["closed"] = False
                    unit_info["resistivity"] = v_unit.annular.resistivity

                    unit_info["rectangle_coordinates"] = self.get_rectangle_coordinates(
                        v_unit.annular.centreline.r,
                        v_unit.annular.centreline.z,
                        v_unit.annular.thickness,
                        unit_info["closed"],
                    )
                    if name_filter is not None:
                        if (
                            name_filter.lower() in v_unit.name.lower()
                            or name_filter.lower() in v_unit.identifier.lower()
                        ):
                            unit_infos[v_unit_index] = unit_info
                    else:
                        unit_infos[v_unit_index] = unit_info
            description2d_info["vesselunits"] = unit_infos
            description2d_infos[description2d_index] = description2d_info

        return description2d_infos

    def get_limiter_units(self, select_description2d=":", select_unit=":"):
        """
        Retrieve information about limiter units from the IDS object.

        Parameters:
        -----------
        select_description2d : str, optional
            A slice notation string to select specific description_2d entries. Default is ":" (select all).
        select_unit : str, optional
            A slice notation string to select specific units within each description_2d. Default is ":" (select all).

        Returns:
        --------
        description2d_infos : dict
            A dictionary where keys are indices of description_2d entries and values are dictionaries containing:
                - "name" : str
                    The name of the description_2d type.
                - "description" : str
                    The description of the description_2d type.
                - "limiterunits" : dict
                    A dictionary where keys are indices of units and values are dictionaries containing:
                        - "name" : str
                            The name of the unit.
                        - "description" : str
                            The description of the unit (empty string if not available).
                        - "r" : numpy.ndarray
                            The r-coordinates of the unit's outline.
                        - "z" : numpy.ndarray
                            The z-coordinates of the unit's outline.
                        - "closed" : bool
                            Indicates if the unit is closed (default is False if not available).
                        - "resistivity" : float
                            The resistivity of the unit.
        """
        description_2ds = list(self.ids_object.description_2d)
        if select_description2d is not None:
            description_2ds = get_slice_from_array(description_2ds, select_description2d)
        description2d_infos = {}
        for description2d_index, description2d in enumerate(description_2ds):
            description2d_info = {}
            description2d_info["name"] = description2d.type.name
            description2d_info["description"] = description2d.type.description

            units = list(description2d.limiter.unit)
            if select_unit is not None:
                units = get_slice_from_array(units, select_unit)
            unit_infos = {}
            if units:
                for l_unit_index, l_unit in enumerate(units):
                    unit_info = {}
                    unit_info["name"] = l_unit.name
                    if hasattr(l_unit, "description"):
                        unit_info["description"] = l_unit.description
                    else:
                        unit_info["description"] = ""
                    unit_info["r"] = l_unit.outline.r
                    unit_info["z"] = l_unit.outline.z
                    if hasattr(l_unit, "closed"):
                        unit_info["closed"] = l_unit.closed
                        if l_unit.closed:
                            unit_info["r"] = np.append(unit_info["r"], unit_info["r"][0])
                            unit_info["z"] = np.append(unit_info["z"], unit_info["z"][0])
                    else:
                        unit_info["closed"] = False
                    unit_info["resistivity"] = l_unit.resistivity
                    if unit_info["closed"] is True:
                        unit_info["r"] = np.append(unit_info["r"], unit_info["r"][0])
                        unit_info["z"] = np.append(unit_info["z"], unit_info["z"][0])
                    unit_infos[l_unit_index] = unit_info

            description2d_info["limiterunits"] = unit_infos
            description2d_infos[description2d_index] = description2d_info

        return description2d_infos

    def get_inner_wall(self):
        """
        Retrieves the inner wall coordinates from the IDS object.

        This method extracts the radial (r) and vertical (z) coordinates of the
        inner wall outline from the first limiter unit in the IDS object's
        2D description. It appends the first coordinate to the end of the array
        to close the loop of the wall outline.

        Returns:
            tuple: A tuple containing two numpy arrays:
                rw (numpy.ndarray): Radial coordinates of the inner wall.
                zw (numpy.ndarray): Vertical coordinates of the inner wall.

            If an error occurs during extraction, returns None.
        """
        try:
            rw = self.ids_object.description_2d[0].limiter.unit[0].outline.r
            zw = self.ids_object.description_2d[0].limiter.unit[0].outline.z

            if not hasattr(rw, "has_value") or not rw.has_value or len(rw) == 0:
                logger.warning("Inner wall r coordinates are empty")
                return None

            if not hasattr(zw, "has_value") or not zw.has_value or len(zw) == 0:
                logger.warning("Inner wall z coordinates are empty")
                return None

            rw = np.array(rw)
            zw = np.array(zw)

            if len(rw) != len(zw):
                logger.error(f"Mismatched array lengths: r={len(rw)}, z={len(zw)}")
                return None

            rw = np.concatenate((rw, [rw[0]]))
            zw = np.concatenate((zw, [zw[0]]))

        except Exception as e:
            logger.error(f"Exception occurred, detailed error {e}")
            return None
        return rw, zw

    @staticmethod
    def get_rectangle_coordinates(r, z, h, closed=False):
        """
        The function `get_rectangle_coordinates` calculates the coordinates of rectangles based on input
        parameters.

        Args:
            r: The parameter `r` in the `get_rectangle_coordinates` function represents the x-coordinates
                of the corners of the rectangles.
            z: The `z` parameter in the `get_rectangle_coordinates` function represents the vertical
                coordinates of the corners of rectangles. It is used to define the vertical positions of the
                rectangle vertices in the 3D space.
            h: The `h` parameter in the `get_rectangle_coordinates` function represents the height of the
                rectangle at each point. It is a list containing the height values for each rectangle.
            closed: The `closed` parameter in the `get_rectangle_coordinates` function is a boolean
                parameter that determines whether the rectangle should be closed or not. If `closed` is set to
                `True`, the function will close the rectangle by connecting the last point to the first point.
                If `closed` is set. Defaults to False

        Returns:
            The function `get_rectangle_coordinates` returns a list of tuples, where each tuple contains
            two lists. The two lists in each tuple represent the x and y coordinates of the vertices of a
            rectangle in 2D space.
        """
        if len(r) == 0 or len(z) == 0 or len(h) == 0:
            return None
        rectangle_coordinates = []

        if closed == 1:
            r = np.append(r, r[0])
            z = np.append(z, z[0])
            h = np.append(h, h[0])

        for i in range(len(r) - 1):
            x1 = r[i + 1] - r[i]
            y1 = z[i + 1] - z[i]
            d = np.sqrt(x1**2 + y1**2)
            cs = x1 / d
            sn = y1 / d

            r1 = np.array([[cs, sn], [-sn, cs]])
            a1 = np.dot(r1, (x1, y1))

            half_h = h[i] * 0.5
            p = [
                (0.0, -half_h),
                (0.0, half_h),
                (a1[0], half_h),
                (a1[0], -half_h),
            ]
            rw = []
            zw = []
            r2 = np.array([[cs, -sn], [sn, cs]])

            for item in p:
                w = np.dot(r2, item) + np.array([r[i], z[i]])
                rw.append(w[0])
                zw.append(w[1])

            rw.append(rw[0])
            zw.append(zw[0])

            rectangle_coordinates.append((rw, zw))
        return rectangle_coordinates
