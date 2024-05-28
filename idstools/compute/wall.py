import logging
from typing import Union

import numpy as np
from shapely.affinity import rotate, translate
from shapely.geometry import LineString, box
import time
from itertools import starmap

wallIndexMapping = {
    "VVIS": 0,
    "VVOS": 1,
    "TS": 2,
    "DIR": 3,
    "Cryostat": 4,
    "CTR1": 5,
    "CTR2": 6,
    "CTR3": 7,
    "CTR4": 8,
    "UCTS": 9,
    "FW": 0,
    "DIV": 1,
}

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

    def getVesselUnits(self):
        description2dInfos = {}
        for description2dIndex, description2d in enumerate(
            self.ids_object.description_2d
        ):
            description2dInfo = {}
            description2dInfo["name"] = description2d.type.name
            description2dInfo["description"] = description2d.type.description
            unitInfos = {}
            for vUnitIndex, vUnit in enumerate(description2d.vessel.unit):
                unitInfo = {}
                unitInfo["name"] = vUnit.name
                unitInfo["identifier"] = vUnit.identifier

                unitInfo["r"] = vUnit.annular.centreline.r
                unitInfo["z"] = vUnit.annular.centreline.z
                unitInfo["h"] = vUnit.annular.thickness
                unitInfo["closed"] = vUnit.annular.centreline.closed
                unitInfo["resistivity"] = vUnit.annular.resistivity

                unitInfo["rectangle_coordinates"] = self.getRectangleCoordinates(
                    vUnit.annular.centreline.r,
                    vUnit.annular.centreline.z,
                    vUnit.annular.thickness,
                    vUnit.annular.centreline.closed,
                )
                unitInfos[vUnitIndex] = unitInfo
            description2dInfo["vesselunits"] = unitInfos
            description2dInfos[description2dIndex] = description2dInfo

        return description2dInfos

    def getLimiterUnits(self):
        description2dInfos = {}
        for description2dIndex, description2d in enumerate(
            self.ids_object.description_2d
        ):
            description2dInfo = {}
            description2dInfo["name"] = description2d.type.name
            description2dInfo["description"] = description2d.type.description
            unitInfos = {}
            for lUnitIndex, lUnit in enumerate(description2d.limiter.unit):
                unitInfo = {}
                unitInfo["name"] = lUnit.name

                unitInfo["r"] = lUnit.outline.r
                unitInfo["z"] = lUnit.outline.z
                unitInfo["closed"] = lUnit.closed
                unitInfo["resistivity"] = lUnit.resistivity
                unitInfos[lUnitIndex] = unitInfo

            description2dInfo["limiterunits"] = unitInfos
            description2dInfos[description2dIndex] = description2dInfo
        
        return description2dInfos

    @staticmethod
    def getRectangleCoordinates(r, z, h, closed=False):
        if len(r) == 0 or len(z) == 0 or len(h) == 0:
            return None
        rectangleCoordinates = []
        n = len(r) - 1
        for i in range(n):
            x1 = r[i + 1] - r[i]
            y1 = z[i + 1] - z[i]
            d = np.sqrt(x1**2 + y1**2)
            cs = x1 / d
            sn = y1 / d

            R1 = np.array([[cs, sn], [-sn, cs]])
            a1 = np.dot(R1, (x1, y1))

            half_h = h[i] * 0.5
            p = [
                (0.0, -half_h),
                (0.0, half_h),
                (a1[0], half_h),
                (a1[0], -half_h),
            ]
            rw = []
            zw = []
            R2 = np.array([[cs, -sn], [sn, cs]])

            for item in p:
                w = np.dot(R2, item) + np.array([r[i], z[i]])
                rw.append(w[0])
                zw.append(w[1])
            if closed:
                rw.append(rw[0])
                zw.append(zw[0])

            rectangleCoordinates.append((rw, zw))
        return rectangleCoordinates

        # def get_limiter(self, iunit=0) -> Union[dict, None]:
        #     """
        #     The function `get_limiter` returns a dictionary containing the outline coordinates of a limiter unit.

        #     Args:
        #         iunit: The `iunit` parameter is an optional integer parameter that specifies the index of the limiter unit. It is used to access a specific limiter unit within the `self.ids_object.description_2d[0].limiter.unit` list. If `iunit` is not provided, it. Defaults to 0

        #     Returns:
        #         a dictionary of FW (limiter) and its data.
        #     """
        #     if len(self.ids_object.description_2d) == 0:
        #         logger.error("wall.description_2d is empty")
        #         return None
        #     if len(self.ids_object.description_2d[0].limiter.unit) <= iunit:
        #         logger.error(
        #             f"wall.description_2d[0].limiter.unit is less than iunit {iunit}"
        #         )
        #         return None

        #     r = self.ids_object.description_2d[0].limiter.unit[iunit].outline.r
        #     z = self.ids_object.description_2d[0].limiter.unit[iunit].outline.z
        #     return None if len(r) == 0 or len(z) == 0 else {"element0": [r, z]}

        # def get_wall(self) -> dict:
        #     """
        #     The function `get_wall` returns a dictionary containing data for various vessels and limiters.

        #     Returns:
        #         a dictionary containing the VV (Vacuum Vessel) and its data. The dictionary includes the VVIS, VVOS, TS, DIR, Cryostat, CTR1, CTR2, CTR3, CTR4, UCTS, FW (First Wall), and DIV (Divertor) data.
        #     """
        #     wall = {
        #         "VVIS": self.get_vessel(iunit=wallIndexMapping["VVIS"], add_endpoint=True)
        #     }

        # wall["VVOS"] = self.get_vessel(
        #     iunit=wallIndexMapping["VVOS"], add_endpoint=True
        # )
        # wall["TS"] = self.get_vessel(iunit=wallIndexMapping["TS"])
        # wall["DIR"] = self.get_vessel(iunit=wallIndexMapping["DIR"])

        # wall["Cryostat"] = self.get_vessel(iunit=wallIndexMapping["Cryostat"])
        # wall["CTR1"] = self.get_vessel(iunit=wallIndexMapping["CTR1"])
        # wall["CTR2"] = self.get_vessel(iunit=wallIndexMapping["CTR2"])
        # wall["CTR3"] = self.get_vessel(iunit=wallIndexMapping["CTR3"])
        # wall["CTR4"] = self.get_vessel(iunit=wallIndexMapping["CTR4"])
        # wall["UCTS"] = self.get_vessel(iunit=wallIndexMapping["UCTS"])

        # wall["FW"] = self.get_limiter(iunit=wallIndexMapping["FW"])
        # wall["DIV"] = self.get_limiter(iunit=wallIndexMapping["DIV"])

        return wall

    # def get_vessel(
    #     self, iunit: int = 0, add_endpoint: bool = False
    # ) -> Union[dict, None]:
    #     """
    #     The `get_vessel` function returns a dictionary containing the data of a VV (vessel) object.

    #     Args:
    #         iunit: The `iunit` parameter is an optional integer parameter that specifies the index of the VV unit for which you want to retrieve the data. By default, it is set to 0, which means the first VV unit. You can change this parameter to retrieve data for a different VV. Defaults to 0
    #         add_endpoint: The `add_endpoint` parameter is a boolean flag that determines whether or not to add an endpoint to the vessel data. If `add_endpoint` is `True`, an additional point will be added to the vessel data to close the shape. If `add_endpoint` is `False`, the vessel data. Defaults to False

    #     Returns:
    #         a dictionary containing the coordinates of the vessel elements. Each element is represented by a key-value pair in the dictionary, where the key is a string in the format "element{element_counter}" and the value is a list of two lists: rw (list of x-coordinates) and zw (list of y-coordinates).
    #     """
    #     print("get_vessel called")
    #     wallDict = self.getWall()
    #     if wallDict is None:
    #         return None
    #     r, z, h = wallDict["r"], wallDict["z"], wallDict["h"]
    #     if len(r) == 0 or len(z) == 0 or len(h) == 0:
    #         return None

    #     if add_endpoint:
    #         r = np.append(r, r[0])
    #         z = np.append(z, z[0])

    #     return element_dict
