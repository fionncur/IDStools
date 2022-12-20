import numpy as np
import sys


class EquilibriumCompute:
    def __init__(self, ids_object):
        super().__init__()
        self.ids_object = ids_object

    @staticmethod
    def get_cartesian_rz_grid(ids_object) -> dict:
        """
        Creates cartesian rz grid and returns the dictionary in below format
            plotrho
            rho2d
            r2d
            z2d
            psi2d

        Args:
            ids_object ([ids_object]): [filled ids object]

        Returns:
            dict: [Returns cartesian rz grid and returns the dictionary]
        """
        compute_object = EquilibriumCompute(ids_object)
        return compute_object.cartesian_rz_grid()

    def cartesian_rz_grid(self) -> dict:
        """
        Creates cartesian rz grid and returns the dictionary in below format
            plotrho
            rho2d
            r2d
            z2d
            psi2d
        Returns:
            [dict]: [Returns cartesian rz grid and returns the dictionary ]
        """
        if len(self.ids_object.time_slice[0].profiles_2d) == 0:
            # TODO Decide on print or raise exception
            print(
                "The equilibrium IDS is empty: len(equilibrium.time_slice[0].profiles_2d)=0",
                file=sys.stderr,
            )
            return None

        profiles_2d = self.ids_object.time_slice[0].profiles_2d[0]

        # psi(R,Z)
        if len(profiles_2d.psi) < 1:
            print(
                "equilibrium.time_slice[:].profiles_2d[0].psi could not be read",
                file=sys.stderr,
            )
            return None

        # phi(R,Z) for rho(R,Z) calculation
        if len(profiles_2d.phi) < 1:
            print(
                "equilibrium.time_slice[:].profiles_2d[0].phi could not be read",
                file=sys.stderr,
            )

        # Cartesian (R,Z) grids
        r2d = profiles_2d.r
        z2d = profiles_2d.z
        psi2d = profiles_2d.psi

        if profiles_2d.grid_type.index == 1 and np.size(r2d) == 0:
            r1d = profiles_2d.grid.dim1
            z1d = profiles_2d.grid.dim2
            nr = len(r1d)
            nz = len(z1d)
            r2d = np.empty(shape=(nr, nz))
            z2d = np.empty(shape=(nr, nz))
            for iz in range(nz):
                r2d[:, iz] = r1d
            for ir in range(nr):
                z2d[ir, :] = z1d

        if not ((np.size(r2d) == np.size(z2d)) and (np.size(r2d) == np.size(psi2d))):
            print(
                "r, z and psi have not the same dimension in equilibrium.time_slice[0].profiles_2d[0]",
                file=sys.stderr,
            )
            return None

        # prepare data
        data_object = {}
        if len(profiles_2d.phi) < 1:
            data_object["plotrho"] = False
            data_object["rho2d"] = None
        else:
            rho2d = np.sqrt(profiles_2d.phi / np.amax(profiles_2d.phi))
            data_object["plotrho"] = True
            data_object["rho2d"] = rho2d

        data_object["r2d"] = r2d
        data_object["z2d"] = z2d
        data_object["psi2d"] = psi2d
        return data_object
