import logging
import time

import numpy as np

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

    def get_vessel_units(self, name_filter=None):
        """
        The function `get_vessel_units` retrieves information about vessel units based on a name filter.

        Args:
            name_filter: The `get_vessel_units` method is used to retrieve information about vessel units
                based on a name filter. The method iterates through the description_2d objects and extracts
                details about each vessel unit, including its name, description, and various properties such as
                coordinates, thickness, resistivity, etc

        Returns:
            The function `get_vessel_units` returns a dictionary containing information about vessel
            units. The dictionary is structured with nested dictionaries for each description 2D object,
            which in turn contain information about the vessel units within that description 2D object. The
            information includes the name, description, and various properties of each vessel unit such as
            name, identifier, dimensions, resistivity, and rectangle coordinates. The
        """
        description2d_infos = {}
        for description2d_index, description2d in enumerate(self.ids_object.description_2d):
            description2d_info = {}
            description2d_info["name"] = description2d.type.name
            description2d_info["description"] = description2d.type.description
            unit_infos = {}
            for v_unit_index, v_unit in enumerate(description2d.vessel.unit):
                unit_info = {}
                unit_info["name"] = v_unit.name
                unit_info["identifier"] = v_unit.identifier

                unit_info["r"] = v_unit.annular.centreline.r
                unit_info["z"] = v_unit.annular.centreline.z
                unit_info["h"] = v_unit.annular.thickness
                unit_info["closed"] = v_unit.annular.centreline.closed
                unit_info["resistivity"] = v_unit.annular.resistivity

                unit_info["rectangle_coordinates"] = self.get_rectangle_coordinates(
                    v_unit.annular.centreline.r,
                    v_unit.annular.centreline.z,
                    v_unit.annular.thickness,
                    v_unit.annular.centreline.closed,
                )
                if name_filter is not None:
                    if name_filter.lower() in v_unit.name.lower() or name_filter.lower() in v_unit.identifier.lower():
                        unit_infos[v_unit_index] = unit_info
                else:
                    unit_infos[v_unit_index] = unit_info
            description2d_info["vesselunits"] = unit_infos
            description2d_infos[description2d_index] = description2d_info

        return description2d_infos

    def get_limiter_units(self):
        """
        This `get_limiter_units` function retrieves information about limiter units from a given object.

        Returns:
            The `get_limiter_units` method returns a dictionary containing information about limiter
            units. The dictionary has keys corresponding to the index of the description 2D objects and
            values containing information about each description 2D object. Each description 2D object
            contains the name and description of the type, as well as information about the limiter units
            associated with it.
        """
        description2d_infos = {}
        for description2d_index, description2d in enumerate(self.ids_object.description_2d):
            description2d_info = {}
            description2d_info["name"] = description2d.type.name
            description2d_info["description"] = description2d.type.description
            unit_infos = {}
            for l_unit_index, l_unit in enumerate(description2d.limiter.unit):
                unit_info = {}
                unit_info["name"] = l_unit.name
                unit_info["r"] = l_unit.outline.r
                unit_info["z"] = l_unit.outline.z
                unit_info["closed"] = l_unit.closed
                unit_info["resistivity"] = l_unit.resistivity
                if l_unit.closed == 1:
                    unit_info["r"] = np.append(unit_info["r"], unit_info["r"][0])
                    unit_info["z"] = np.append(unit_info["z"], unit_info["z"][0])
                unit_infos[l_unit_index] = unit_info

            description2d_info["limiterunits"] = unit_infos
            description2d_infos[description2d_index] = description2d_info

        return description2d_infos

    def get_inner_wall(self):
        try:
            rw = self.ids_object.description_2d[0].limiter.unit[0].outline.r
            zw = self.ids_object.description_2d[0].limiter.unit[0].outline.z
            # append first value to end of array
            rw = np.concatenate((rw, [rw[0]]))
            zw = np.concatenate((zw, [zw[0]]))
        except Exception as _:  # noqa: F841
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
