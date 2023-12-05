import numpy as np
from typing import Union

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


class WallCompute:
    def __init__(self, ids_object):
        self.ids_object = ids_object

    def getWall(self, iunit: int = 0):
        if len(self.ids_object.description_2d) == 0:
            return None
        if len(self.ids_object.description_2d[0].vessel.unit) <= iunit:
            return None
        r = self.ids_object.description_2d[0].vessel.unit[iunit].annular.centreline.r
        z = self.ids_object.description_2d[0].vessel.unit[iunit].annular.centreline.z
        h = self.ids_object.description_2d[0].vessel.unit[iunit].annular.thickness
        return {"r": r, "z": z, "h": h}

    def get_vessel(
        self, iunit: int = 0, add_endpoint: bool = False
    ) -> Union[dict, None]:
        """
        The `get_vessel` function returns a dictionary containing the data of a VV (vessel) object.

        Args:
            iunit: The `iunit` parameter is an optional integer parameter that specifies the index of the VV unit for which you want to retrieve the data. By default, it is set to 0, which means the first VV unit. You can change this parameter to retrieve data for a different VV. Defaults to 0
            add_endpoint: The `add_endpoint` parameter is a boolean flag that determines whether or not to add an endpoint to the vessel data. If `add_endpoint` is `True`, an additional point will be added to the vessel data to close the shape. If `add_endpoint` is `False`, the vessel data. Defaults to False

        Returns:
            a dictionary containing the coordinates of the vessel elements. Each element is represented by a key-value pair in the dictionary, where the key is a string in the format "element{element_counter}" and the value is a list of two lists: rw (list of x-coordinates) and zw (list of y-coordinates).
        """
        wallDict = self.getWall(iunit)
        r, z, h = wallDict["r"], wallDict["z"], wallDict["h"]
        if len(r) == 0 or len(z) == 0 or len(h) == 0:
            return None

        if add_endpoint:
            r = np.append(r, r[0])
            z = np.append(z, z[0])

        element_dict = {}
        for element_counter, i in enumerate(range(len(r) - 1)):
            x1 = r[i + 1] - r[i]
            y1 = z[i + 1] - z[i]
            d = np.sqrt(x1**2 + y1**2)
            cs = x1 / d
            sn = y1 / d

            R1 = np.array([[cs, sn], [-sn, cs]])
            a1 = np.dot(R1, (x1, y1))

            p = [
                (0.0, -h[i] * 0.5),
                (0.0, h[i] * 0.5),
                (a1[0], h[i] * 0.5),
                (a1[0], -h[i] * 0.5),
            ]
            rw = []
            zw = []
            R2 = np.array([[cs, -sn], [sn, cs]])
            for item in p:
                w = np.dot(R2, item) + np.array([r[i], z[i]])
                rw.append(w[0])
                zw.append(w[1])
            rw.append(rw[0])
            zw.append(zw[0])

            element_dict[f"element{element_counter}"] = [rw, zw]
        return element_dict

    def get_limiter(self, iunit=0) -> Union[dict, None]:
        """
        The function `get_limiter` returns a dictionary containing the outline coordinates of a limiter unit.

        Args:
            iunit: The `iunit` parameter is an optional integer parameter that specifies the index of the limiter unit. It is used to access a specific limiter unit within the `self.ids_object.description_2d[0].limiter.unit` list. If `iunit` is not provided, it. Defaults to 0

        Returns:
            a dictionary of FW (limiter) and its data.
        """

        if len(self.ids_object.description_2d[0].limiter.unit) <= iunit:
            return None
        r = self.ids_object.description_2d[0].limiter.unit[iunit].outline.r
        z = self.ids_object.description_2d[0].limiter.unit[iunit].outline.z
        return None if len(r) == 0 or len(z) == 0 else {"element0": [r, z]}

    def get_wall(self) -> dict:
        """
        The function `get_wall` returns a dictionary containing data for various vessels and limiters.

        Returns:
            a dictionary containing the VV (Vacuum Vessel) and its data. The dictionary includes the VVIS, VVOS, TS, DIR, Cryostat, CTR1, CTR2, CTR3, CTR4, UCTS, FW (First Wall), and DIV (Divertor) data.
        """
        wall = {
            "VVIS": self.get_vessel(iunit=wallIndexMapping["VVIS"], add_endpoint=True)
        }

        wall["VVOS"] = self.get_vessel(
            iunit=wallIndexMapping["VVOS"], add_endpoint=True
        )
        wall["TS"] = self.get_vessel(iunit=wallIndexMapping["TS"])
        wall["DIR"] = self.get_vessel(iunit=wallIndexMapping["DIR"])

        wall["Cryostat"] = self.get_vessel(iunit=wallIndexMapping["Cryostat"])
        wall["CTR1"] = self.get_vessel(iunit=wallIndexMapping["CTR1"])
        wall["CTR2"] = self.get_vessel(iunit=wallIndexMapping["CTR2"])
        wall["CTR3"] = self.get_vessel(iunit=wallIndexMapping["CTR3"])
        wall["CTR4"] = self.get_vessel(iunit=wallIndexMapping["CTR4"])
        wall["UCTS"] = self.get_vessel(iunit=wallIndexMapping["UCTS"])

        wall["FW"] = self.get_limiter(iunit=wallIndexMapping["FW"])
        wall["DIV"] = self.get_limiter(iunit=wallIndexMapping["DIV"])

        return wall
