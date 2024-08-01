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

    @staticmethod
    def get_rectangle_coordinates(r, z, h, closed=False):
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
