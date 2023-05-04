import numpy as np
import sys


class WavesCompute:
    def __init__(self, ids_object):
        super().__init__()
        self.ids_object = ids_object
        self._index = 0

        self.n_harm = [1, 2, 3, 4]

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if value < 0:
            raise ValueError("Value is not appropriate")
        self._index = value

    @staticmethod
    def get_object(ids_object) -> object:
        """[summary]

        Args:
            ids_object ([type]): [description]

        Returns:
            dict: [description]
        """
        compute_object = WavesCompute(ids_object)
        return compute_object

    def get_B_res(self, wave_index=0):
        """
            B-field at the resonance for three first harmonics

        Args:
            index (int, optional): [description]. Defaults to 0.

        Returns:
            [type]: [description]
        """
        ec_frequency = (
            self.ids_object.coherent_wave[0].global_quantities[wave_index].frequency
        )

        # B-field at the resonance for three first harmonics
        B_res = [0] * len(self.n_harm)
        for i_harm in range(len(self.n_harm)):
            B_res[i_harm] = (
                2 * np.pi * ec_frequency * 9.1e-31 / 1.6e-19 / self.n_harm[i_harm]
            )
        return B_res

    def get_beam_array(self):
        nbeam = len(self.ids_object.coherent_wave)

        beam_array = np.linspace(0, nbeam - 1, nbeam)
        return beam_array

    def get_omega_ec(self, time_index):
        from scipy import constants, interpolate

        omega_ec = (
            2
            * constants.pi
            * self.ids_object.coherent_wave[0].global_quantities[time_index].frequency
        )
        return omega_ec

    def read_beam_tracing(self, beam_tracing_index):

        beam_tracing = {}

        # Read beam tracing information from the output waves IDS
        nbeam = len(self.ids_object.coherent_wave)

        # Count number of active beams and their number of rays
        is_active = [0] * nbeam
        nray_array = [0] * nbeam
        for ibeam in range(nbeam):
            nray_array[ibeam] = len(
                self.ids_object.coherent_wave[ibeam]
                .beam_tracing[beam_tracing_index]
                .beam
            )
            for iray in range(nray_array[ibeam]):
                if (
                    self.ids_object.coherent_wave[ibeam]
                    .beam_tracing[beam_tracing_index]
                    .beam[iray]
                    .power_initial
                    > 0
                ):
                    is_active[ibeam] = 1
        nbeam_active = sum(is_active)

        # We assume the same number of rays for each beam, to simplify (and this is usually the case)
        nray = max(nray_array)
        stdarrlen = max(
            max(
                [
                    [
                        len(
                            self.ids_object.coherent_wave[ibeam]
                            .beam_tracing[beam_tracing_index]
                            .beam[iray]
                            .position.r
                        )
                        for iray in range(nray)
                    ]
                    for ibeam in range(nbeam)
                ]
            )
        )
        len_ray = np.array(
            [[0.0 for iray in range(nray)] for ibeam in range(nbeam)]
        ).astype(int)
        x_ray = np.array(
            [
                [[0.0 for ix in range(stdarrlen)] for iray in range(nray)]
                for ibeam in range(nbeam)
            ]
        )
        y_ray, z_ray, r_ray, phi_ray = (
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
        )
        central_ray_power = np.array(
            [[0.0 for ix in range(stdarrlen)] for ibeam in range(nbeam)]
        )
        central_ray_powerpar, central_ray_powerperp, central_ray_length = (
            np.ndarray.copy(central_ray_power),
            np.ndarray.copy(central_ray_power),
            np.ndarray.copy(central_ray_power),
        )
        wr = []
        for ibeam in range(nbeam):
            if is_active[ibeam] == 1:
                iray = -1
                for irray in range(nray):
                    iray = iray + 1
                    if (
                        self.ids_object.coherent_wave[ibeam]
                        .beam_tracing[beam_tracing_index]
                        .beam[iray]
                        .power_initial
                        != 0
                    ):
                        wr = (
                            self.ids_object.coherent_wave[ibeam]
                            .beam_tracing[beam_tracing_index]
                            .beam[iray]
                            .position.r
                        )
                        wphi = (
                            self.ids_object.coherent_wave[ibeam]
                            .beam_tracing[beam_tracing_index]
                            .beam[iray]
                            .position.phi
                        )
                        wz = (
                            self.ids_object.coherent_wave[ibeam]
                            .beam_tracing[beam_tracing_index]
                            .beam[iray]
                            .position.z
                        )
                        len_ray[ibeam, iray] = len(wr)
                        r_ray[ibeam, iray, : len(wr)] = np.array(wr)
                        phi_ray[ibeam, iray, : len(wphi)] = np.array(wphi)
                        z_ray[ibeam, iray, : len(wz)] = np.array(wz)
                        x_ray[ibeam, iray, :] = r_ray[ibeam, iray, :] * np.cos(
                            phi_ray[ibeam, iray, :]
                        )
                        y_ray[ibeam, iray, :] = r_ray[ibeam, iray, :] * np.sin(
                            phi_ray[ibeam, iray, :]
                        )
                npath = len(
                    self.ids_object.coherent_wave[ibeam]
                    .beam_tracing[beam_tracing_index]
                    .beam[0]
                    .electrons.power
                )
                if (
                    len(
                        self.ids_object.coherent_wave[ibeam]
                        .beam_tracing[beam_tracing_index]
                        .beam[0]
                        .electrons.power
                    )
                    > 0
                ):
                    central_ray_power[ibeam, 0:npath] = (
                        self.ids_object.coherent_wave[ibeam]
                        .beam_tracing[beam_tracing_index]
                        .beam[0]
                        .electrons.power
                    )
                if (
                    len(
                        self.ids_object.coherent_wave[ibeam]
                        .beam_tracing[beam_tracing_index]
                        .beam[0]
                        .power_flow_norm.parallel
                    )
                    > 0
                ):
                    central_ray_powerpar[ibeam, 0:npath] = (
                        self.ids_object.coherent_wave[ibeam]
                        .beam_tracing[beam_tracing_index]
                        .beam[0]
                        .power_flow_norm.parallel
                    )
                if (
                    len(
                        self.ids_object.coherent_wave[ibeam]
                        .beam_tracing[beam_tracing_index]
                        .beam[0]
                        .power_flow_norm.perpendicular
                    )
                    > 0
                ):
                    central_ray_powerperp[ibeam, 0:npath] = (
                        self.ids_object.coherent_wave[ibeam]
                        .beam_tracing[beam_tracing_index]
                        .beam[0]
                        .power_flow_norm.perpendicular
                    )
                if (
                    len(
                        self.ids_object.coherent_wave[ibeam]
                        .beam_tracing[beam_tracing_index]
                        .beam[0]
                        .length
                    )
                    > 0
                ):
                    central_ray_length[ibeam, 0:npath] = (
                        self.ids_object.coherent_wave[ibeam]
                        .beam_tracing[beam_tracing_index]
                        .beam[0]
                        .length
                    )

        beam_tracing["nbeam"] = nbeam
        beam_tracing["nbeam_active"] = nbeam_active
        beam_tracing["nray"] = nray
        beam_tracing["is_active"] = is_active
        beam_tracing["len_ray"] = len_ray
        beam_tracing["x_ray"] = x_ray
        beam_tracing["y_ray"] = y_ray
        beam_tracing["z_ray"] = z_ray
        beam_tracing["r_ray"] = r_ray
        beam_tracing["phi_ray"] = phi_ray[:, :, : len(wr)]
        beam_tracing["central_ray_power"] = central_ray_power
        beam_tracing["central_ray_powerpar"] = central_ray_powerpar
        beam_tracing["central_ray_powerperp"] = central_ray_powerperp
        beam_tracing["central_ray_length"] = central_ray_length

        return beam_tracing
