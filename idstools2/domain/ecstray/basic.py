import numpy as np

from idstools2.compute.equilibrium.basic import EquilibriumCompute
from idstools2.compute.waves.basic import WavesCompute
from idstools2.compute.common.basic import nearest


class EcStrayCompute:
    def __init__(self, equilibrium_ids, core_profiles_ids, waves_ids):
        super().__init__()
        self.equilibrium_ids = equilibrium_ids
        self.core_profiles_ids = core_profiles_ids
        self.waves_ids = waves_ids

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if value < 0:
            raise ValueError("Value is not appropriate")
        self._index = value

    def get_resonance_layer(self, time_index_wv, time_index_eq):
        # TODO Why different time slices
        eqcomputeobj = EquilibriumCompute(self.equilibrium_ids)

        ieq_rect, b_tot = eqcomputeobj.getBTotal(time_index_eq)
        r = eqcomputeobj.ids.time_slice[time_index_eq].profiles_2d[ieq_rect].grid.dim1
        z = eqcomputeobj.ids.time_slice[time_index_eq].profiles_2d[ieq_rect].grid.dim2
        wavecompute = WavesCompute(self.waves_ids)
        wavecompute.index = 0
        B_res = wavecompute.get_B_res(time_index_wv)
        n_harm = [1, 2, 3, 4]

        [nr, nz] = np.shape(b_tot)
        b_err = 10 / nr
        res_layer = {}
        for i_harm in range(len(n_harm)):
            res_layer[i_harm] = {}
            res_layer[i_harm]["r"] = []
            res_layer[i_harm]["z"] = []
            for iz in range(nz):
                [ir, rloc] = nearest(b_tot[:, iz], B_res[i_harm])
                if np.abs(b_tot[ir, iz] - B_res[i_harm]) < b_err:
                    res_layer[i_harm]["r"].append(r[ir])
                    res_layer[i_harm]["z"].append(z[iz])

        return res_layer

    def get_cutoff_layer(self, time_index_wv=0, time_index_cp=0, time_index_eq=0):
        from scipy import constants, interpolate

        wavecompute = WavesCompute(self.waves_ids)
        omega_ec = wavecompute.get_omega_ec(time_index_wv)

        # Find (R,Z) rectangular grid of B-field
        eqcomputeobj = EquilibriumCompute(self.equilibrium_ids)
        ieq_rect, b_tot = eqcomputeobj.getBTotal(time_index_eq)

        # B(R,Z) evaluation
        r = (
            self.equilibrium_ids.time_slice[time_index_eq]
            .profiles_2d[ieq_rect]
            .grid.dim1
        )
        z = (
            self.equilibrium_ids.time_slice[time_index_eq]
            .profiles_2d[ieq_rect]
            .grid.dim2
        )

        # Ne(psi) in core_profiles IDS
        rho1d_cp = self.core_profiles_ids.profiles_1d[time_index_cp].grid.rho_tor_norm
        psi1d_cp = (
            self.core_profiles_ids.profiles_1d[time_index_cp].grid.psi
            - self.core_profiles_ids.profiles_1d[time_index_cp].grid.psi[-1]
        ) / (
            self.core_profiles_ids.profiles_1d[time_index_cp].grid.psi[0]
            - self.core_profiles_ids.profiles_1d[time_index_cp].grid.psi[-1]
        )
        ne_cp = self.core_profiles_ids.profiles_1d[time_index_cp].electrons.density

        # Ne(psi) interpolated over equilibrium IDS
        rho1d_eq = self.equilibrium_ids.time_slice[
            time_index_eq
        ].profiles_1d.rho_tor_norm
        psi1d_eq = (
            self.equilibrium_ids.time_slice[time_index_eq].profiles_1d.psi
            - self.equilibrium_ids.time_slice[time_index_eq].profiles_1d.psi[-1]
        ) / (
            self.equilibrium_ids.time_slice[time_index_eq].profiles_1d.psi[0]
            - self.equilibrium_ids.time_slice[time_index_eq].profiles_1d.psi[-1]
        )
        ne_eq = np.zeros(len(psi1d_eq))
        ne_interp = interpolate.interp1d(psi1d_cp, ne_cp, kind="linear")
        for i in range(len(psi1d_eq)):
            ne_eq[i] = float(ne_interp(psi1d_eq[i]))

        # Ne(R,Z) deduced for each point over B(R,Z) in equilibrium IDS
        psi1d_eq = self.equilibrium_ids.time_slice[time_index_eq].profiles_1d.psi
        psi2d_eq = (
            self.equilibrium_ids.time_slice[time_index_eq].profiles_2d[ieq_rect].psi
        )
        ne_from_psi = interpolate.interp1d(psi1d_eq, ne_eq, kind="linear")
        ne2d_eq = np.zeros(np.shape(psi2d_eq))
        omega_r = np.zeros(np.shape(psi2d_eq))
        for ir in range(len(r)):
            for iz in range(len(z)):
                try:  # Inside LCFS
                    ne2d_eq[ir, iz] = ne_from_psi(psi2d_eq[ir, iz])
                    # omega_R = sqrt[(eB/m_e/2)**2 + n_e *e**2/(epsilon_0*m_e)] + eB/m_e/2
                    omega_r[ir, iz] = np.sqrt(
                        (constants.e * b_tot[ir, iz] / (2 * constants.m_e)) ** 2
                        + ne2d_eq[ir, iz]
                        * constants.e**2
                        / (constants.epsilon_0 * constants.m_e)
                    ) + constants.e * b_tot[ir, iz] / (2 * constants.m_e)
                except:  # Not defined outside LCFS
                    ne2d_eq[ir, iz] = -1  # np.NaN
                    omega_r[ir, iz] = -1  # np.NaN

        # Find (R,Z) where omega_R = omega_EC (within the tolerance omega_err)
        [nr, nz] = np.shape(omega_r)
        omega_err = 100 / nr

        cutoff_layer = {}
        cutoff_layer["r"] = []
        cutoff_layer["z"] = []
        for iz in range(nz):
            [ir, rloc] = nearest(omega_r[:, iz], omega_ec)
            if np.abs((omega_r[ir, iz] - omega_ec) / omega_r[ir, iz]) < omega_err:
                cutoff_layer["r"].append(r[ir])
                cutoff_layer["z"].append(z[iz])

        # import pdb
        # pdb.set_trace()

        return cutoff_layer
