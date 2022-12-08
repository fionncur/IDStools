import numpy as np
import sys


class CartesionRZGridsDataInteface:
    def __init__(self) -> None:
        self.r2d = None
        self.z2d = None
        self.psi2d = None

        self.plotrho = None
        self.rho2d = None


class EquilibriumCompute:
    def __init__(self, ids_object):
        super().__init__()
        self.ids_object = ids_object

    def validate_2d_profile(self):
        if len(self.ids_object.time_slice[0].profiles_2d) == 0:
            # TODO Decide on print or raise exception
            print(
                "The equilibrium IDS is empty: len(equilibrium.time_slice[0].profiles_2d)=0",
                file=sys.stderr,
            )
            print("----> Aborted.", file=sys.stderr)
            exit()

        # phi(R,Z) for rho(R,Z) calculation
        if len(self.ids_object.time_slice[0].profiles_2d[0].phi) < 1:
            print(
                "equilibrium.time_slice[:].profiles_2d[0].phi could not be read",
                file=sys.stderr,
            )

        # psi(R,Z)
        if len(self.ids_object.time_slice[0].profiles_2d[0].psi) < 1:
            print(
                "equilibrium.time_slice[:].profiles_2d[0].psi could not be read",
                file=sys.stderr,
            )
            print("----> Aborted.", file=sys.stderr)
            exit()
        return

    def get_cartesian_r_z_grids(self):
        self.validate_2d_profile()
        # Cartesian (R,Z) grids
        data_object = CartesionRZGridsDataInteface()
        r2d = self.ids_object.time_slice[0].profiles_2d[0].r
        z2d = self.ids_object.time_slice[0].profiles_2d[0].z
        psi2d = self.ids_object.time_slice[0].profiles_2d[0].psi

        if (
            self.ids_object.time_slice[0].profiles_2d[0].grid_type.index == 1
            and np.size(r2d) == 0
        ):
            r1d = self.ids_object.time_slice[0].profiles_2d[0].grid.dim1
            z1d = self.ids_object.time_slice[0].profiles_2d[0].grid.dim2
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
            print("----> Aborted.", file=sys.stderr)
            exit()

        if len(self.ids_object.time_slice[0].profiles_2d[0].phi) < 1:
            data_object.plotrho = False
            data_object.rho2d = None
        else:
            rho2d = np.sqrt(
                self.ids_object.time_slice[0].profiles_2d[0].phi
                / np.amax(self.ids_object.time_slice[0].profiles_2d[0].phi)
            )
            data_object.plotrho = True
            data_object.rho2d = rho2d

        data_object.r2d = r2d
        data_object.z2d = z2d
        data_object.psi2d = psi2d
        return data_object
