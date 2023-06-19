import numpy as np


class WallCompute:
    def __init__(self, ids_object):
        self.ids_object = ids_object

    def get_vessel(self, iunit=0, add_endpoint=False) -> dict:
        """
        Returns dictionary of VV and its data

        Returns:
            dict: [dictionary of VV and its data]
        """
        vv = {}
        r = self.ids_object.description_2d[0].vessel.unit[iunit].annular.centreline.r
        z = self.ids_object.description_2d[0].vessel.unit[iunit].annular.centreline.z
        h = self.ids_object.description_2d[0].vessel.unit[iunit].annular.thickness

        if add_endpoint:
            r = np.append(r, r[0])
            z = np.append(z, z[0])

        element_dict = {}
        element_counter = 0

        for i in range(len(r) - 1):
            #
            x1 = r[i + 1] - r[i]
            y1 = z[i + 1] - z[i]
            d = np.sqrt(x1**2 + y1**2)
            cs = x1 / d
            sn = y1 / d

            R1 = np.array([[cs, sn], [-sn, cs]])
            a1 = np.dot(R1, (x1, y1))

            p = []
            p.append((0.0, -h[i] * 0.5))
            p.append((0.0, h[i] * 0.5))
            p.append((a1[0], h[i] * 0.5))
            p.append((a1[0], -h[i] * 0.5))

            rw = []
            zw = []
            R2 = np.array([[cs, -sn], [sn, cs]])
            for j in range(len(p)):
                w = np.dot(R2, p[j]) + np.array([r[i], z[i]])
                rw.append(w[0])
                zw.append(w[1])
            rw.append(rw[0])
            zw.append(zw[0])

            element_dict["element" + str(element_counter)] = [rw, zw]
            element_counter += 1

        return element_dict

    def get_limiter(self, iunit=0) -> dict:
        """
        Returns dictionary of FW and its data

        Returns:
            dict: [dictionary of FW and its data]
        """

        r = self.ids_object.description_2d[0].limiter.unit[iunit].outline.r
        z = self.ids_object.description_2d[0].limiter.unit[iunit].outline.z

        element_dict = {}
        element_dict["element0"] = [r, z]

        return element_dict

    def get_wall(self) -> dict:
        """
        Returns dictionary of VV and its data

        Returns:
            dict: [dictionary of VV and its data]
        """
        wall = {}

        wall["VVIS"] = self.get_vessel(iunit=0, add_endpoint=True)
        wall["VVOS"] = self.get_vessel(iunit=1, add_endpoint=True)
        wall["TS"] = self.get_vessel(iunit=2)
        wall["DIR"] = self.get_vessel(iunit=3)

        wall["Cryostat"] = self.get_vessel(iunit=4)
        wall["CTR1"] = self.get_vessel(iunit=5)
        wall["CTR2"] = self.get_vessel(iunit=6)
        wall["CTR3"] = self.get_vessel(iunit=7)
        wall["CTR4"] = self.get_vessel(iunit=8)
        wall["UCTS"] = self.get_vessel(iunit=9)

        wall["FW"] = self.get_limiter(iunit=0)
        wall["DIV"] = self.get_limiter(iunit=1)

        return wall
