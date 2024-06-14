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

    def getVesselUnits(self, nameFilter=None):
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
                if nameFilter is not None:
                    if (
                        nameFilter.lower() in vUnit.name.lower()
                        or nameFilter.lower() in vUnit.identifier.lower()
                    ):
                        unitInfos[vUnitIndex] = unitInfo
                else:
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
                if lUnit.closed == 1:
                    unitInfo["r"] = np.append(unitInfo["r"], unitInfo["r"][0])
                    unitInfo["z"] = np.append(unitInfo["z"], unitInfo["z"][0])
                unitInfos[lUnitIndex] = unitInfo

            description2dInfo["limiterunits"] = unitInfos
            description2dInfos[description2dIndex] = description2dInfo

        return description2dInfos

    @staticmethod
    def getRectangleCoordinates(r, z, h, closed=False):
        if len(r) == 0 or len(z) == 0 or len(h) == 0:
            return None
        rectangleCoordinates = []

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

            # if closed:
            # rw.append(rw[0])
            # zw.append(zw[0])

            rectangleCoordinates.append((rw, zw))
        return rectangleCoordinates
