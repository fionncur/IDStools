import logging

import numpy as np
import scipy.constants.codata as codata
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table, Column
from rich.align import Align
from idstools.compute.core_transport import CoreTransportCompute
from idstools.compute.equilibrium import EquilibriumCompute

logger = logging.getLogger(f"module.{__name__}")

QE = codata.physical_constants["elementary charge"][0]


class CoreTransportView:
    def __init__(self, ids):
        self.coreTransportCompute = CoreTransportCompute(ids)
        self.ids = ids

    def viewFluxes(self):
        """
        The `viewFluxes` function prints out flux information for electrons and ions.
        """
        fluxesDict = self.coreTransportCompute.getFluxes()
        ionTable = Table(show_header=False)
        for _, fluxDict in fluxesDict.items():
            if fluxDict["particles_flux"] is None:
                eparticles_flux = "particles(--)"
            else:
                eparticles_flux = f"particles ({fluxDict['particles_flux'] : >.6e})"
            if fluxDict["energy_flux"] is None:
                eenergy_flux = "energy(--)"
            else:
                eenergy_flux = f"energy ({fluxDict['energy_flux']: >.6e})"
            ionTable.add_row(
                f'{fluxDict["name"]} ({fluxDict["flux_multiplier"]})',
                eparticles_flux,
                eenergy_flux,
                "",
                "",
                style="bold magenta",
            )
            ionTable.add_section()
            ionTable.add_row(
                Align.right("a"),
                Align.right("z_n"),
                Align.right("z_ion"),
                Align.right("particles"),
                Align.right("energy"),
                style="bold red",
            )

            for _, ionDict in fluxDict["ions"].items():
                if ionDict["particles_flux"] is None or np.isnan(
                    ionDict["particles_flux"]
                ):
                    particles_flux = "--"
                else:
                    particles_flux = f"{ionDict['particles_flux'] : >.6e}"
                if ionDict["energy_flux"] is None or np.isnan(ionDict["energy_flux"]):
                    energy_flux = "--"
                else:
                    energy_flux = f"{ionDict['energy_flux'] : >.6e}"
                ionTable.add_row(
                    Align.right(str(ionDict["a"])),
                    Align.right(str(ionDict["z_n"])),
                    Align.right(str(ionDict["z_ion"])),
                    Align.right(particles_flux),
                    Align.right(energy_flux),
                    style="bold green",
                )
            ionTable.add_section()
        console = Console()
        console.print(ionTable)

    def viewIonsParticleFluxes(
        self,
        axes,
        idsCoreTransport,
        idsCoreProfiles,
        idsEquilibrium,
        timeIndex,
        modelIndex,
        logscale=False,
    ):
        Tm = idsCoreTransport.model[modelIndex]
        V = Tm.profiles_1d[timeIndex].grid_d.volume
        r = Tm.profiles_1d[timeIndex].grid_d.rho_tor_norm
        S = Tm.profiles_1d[timeIndex].grid_d.area
        Vp_per_S = np.gradient(V, r) / S

        eCompute = EquilibriumCompute(idsEquilibrium)
        gm3 = eCompute.getgm3(r, timeSlice=timeIndex)
        gm7 = eCompute.getgm7(r, timeSlice=timeIndex)

        counter = 0
        for T_i, C_i in zip(
            Tm.profiles_1d[-1].ion,
            idsCoreProfiles.profiles_1d[timeIndex].ion,
        ):
            self._validateIonsData(T_i, C_i, r, modelIndex)

            Gamma_i = Vp_per_S * (
                -T_i.particles.d * np.gradient(C_i.density, r) * gm3
                + C_i.density * T_i.particles.v * gm7
            )
            ax = axes[counter]
            counter = counter + 1
            ax.plot(r, Gamma_i, label="Direct evaluation")
            ax.plot(r, T_i.particles.flux, label="Transport code")
            if logscale:
                ax.set_yscale("log")
            ax.set_title(f"Particle fluxes for {T_i.element[0].z_n}/{T_i.element[0].a}")
            ax.set_xlabel("rho_tor_norm")
            ax.set_ylabel("Particle flux density")
            ax.legend()

    def viewIonsEnergyFluxes(
        self,
        axes,
        idsCoreTransport,
        idsCoreProfiles,
        idsEquilibrium,
        timeIndex,
        modelIndex,
        logscale=False,
    ):
        Tm = idsCoreTransport.model[modelIndex]
        V = Tm.profiles_1d[timeIndex].grid_d.volume
        r = Tm.profiles_1d[timeIndex].grid_d.rho_tor_norm
        S = Tm.profiles_1d[timeIndex].grid_d.area
        Vp_per_S = np.gradient(V, r) / S

        eCompute = EquilibriumCompute(idsEquilibrium)
        gm3 = eCompute.getgm3(r, timeSlice=timeIndex)
        gm7 = eCompute.getgm7(r, timeSlice=timeIndex)

        counter = 0
        for T_i, C_i in zip(
            Tm.profiles_1d[-1].ion,
            idsCoreProfiles.profiles_1d[timeIndex].ion,
        ):
            self._validateIonsData(T_i, C_i, r, modelIndex)
            Gamma_i = Vp_per_S * (
                -T_i.particles.d * np.gradient(C_i.density, r) * gm3
                + C_i.density * T_i.particles.v * gm7
            )

            ax = axes[counter]
            counter = counter + 1
            Q_i_conductive = (
                Vp_per_S
                * (
                    -T_i.energy.d * np.gradient(C_i.temperature, r) * gm3
                    + C_i.temperature * T_i.energy.v * gm7
                )
                * C_i.density
                * QE
            )
            Q_i_convective = Gamma_i * C_i.temperature * QE
            ax.plot(r, Q_i_conductive, label="Direct evaluation (conductive)")
            (base_line,) = ax.plot(
                r, Q_i_convective * 1.5, label="Direct evaluation (convective)"
            )
            ax.fill_between(
                r,
                Q_i_convective * 0.0,
                Q_i_convective * 2.5,
                facecolor=base_line.get_color(),
                alpha=0.2,
            )
            (base_line,) = ax.plot(
                r, Q_i_conductive + Q_i_convective * 1.5, label="Direct evaluation"
            )
            ax.fill_between(
                r,
                Q_i_conductive + Q_i_convective * 0.0,
                Q_i_conductive + Q_i_convective * 2.5,
                facecolor=base_line.get_color(),
                alpha=0.2,
            )
            ax.plot(r, T_i.energy.flux, label="Transport code")
            if logscale:
                ax.set_yscale("log")
            ax.set_title(f"Energy fluxes for {T_i.element[0].z_n}/{T_i.element[0].a}")
            ax.set_xlabel("rho_tor_norm")
            ax.set_ylabel("Energy flux density")
            ax.legend()

    def viewEnergyFluxesForElectrons(
        self,
        ax,
        idsCoreTransport,
        idsCoreProfiles,
        idsEquilibrium,
        timeIndex,
        modelIndex,
        logscale=False,
    ):
        Tm = idsCoreTransport.model[modelIndex]
        V = Tm.profiles_1d[timeIndex].grid_d.volume
        r = Tm.profiles_1d[timeIndex].grid_d.rho_tor_norm
        S = Tm.profiles_1d[timeIndex].grid_d.area
        Vp_per_S = np.gradient(V, r) / S

        T_e = Tm.profiles_1d[timeIndex].electrons
        C_e = idsCoreProfiles.profiles_1d[timeIndex].electrons
        self._validateElectrons(T_e, C_e, r, modelIndex)
        eCompute = EquilibriumCompute(idsEquilibrium)
        gm3 = eCompute.getgm3(r, timeSlice=timeIndex)
        gm7 = eCompute.getgm7(r, timeSlice=timeIndex)

        Q_e_conductive = (
            Vp_per_S
            * (
                -T_e.energy.d * np.gradient(C_e.temperature, r) * gm3
                + C_e.temperature * T_e.energy.v * gm7
            )
            * C_e.density
            * QE
        )
        Gamma_e = np.array(
            [t.particles.flux * t.z_ion for t in Tm.profiles_1d[-1].ion]
        ).sum(axis=0)
        Q_e_convective = Gamma_e * C_e.temperature * QE

        ax.plot(r, Q_e_conductive, label="Direct evaluation (conductive)")
        (base_line,) = ax.plot(
            r, Q_e_convective * 1.5, label="Direct evaluation (convective)"
        )
        ax.fill_between(
            r,
            Q_e_convective * 0.0,
            Q_e_convective * 2.5,
            facecolor=base_line.get_color(),
            alpha=0.2,
        )
        (base_line,) = ax.plot(
            r, Q_e_conductive + Q_e_convective * 1.5, label="Direct evaluation"
        )
        ax.fill_between(
            r,
            Q_e_conductive + Q_e_convective * 0.0,
            Q_e_conductive + Q_e_convective * 2.5,
            facecolor=base_line.get_color(),
            alpha=0.2,
        )
        ax.plot(r, T_e.energy.flux, label="Transport code")
        if logscale:
            ax.set_yscale("log")
        ax.set_title("Energy fluxes for electrons")
        ax.set_xlabel("rho_tor_norm")
        ax.set_ylabel("Energy flux density")
        ax.legend()

    def viewParticleFluxesForElectrons(
        self,
        ax,
        idsCoreTransport,
        idsCoreProfiles,
        timeIndex,
        modelIndex,
        logscale=False,
    ):
        Tm = idsCoreTransport.model[modelIndex]
        r = Tm.profiles_1d[timeIndex].grid_d.rho_tor_norm

        T_e = Tm.profiles_1d[timeIndex].electrons
        C_e = idsCoreProfiles.profiles_1d[timeIndex].electrons
        self._validateElectrons(T_e, C_e, r, modelIndex)
        Gamma_e = np.array(
            [t.particles.flux * t.z_ion for t in Tm.profiles_1d[-1].ion]
        ).sum(axis=0)

        ax.plot(r, Gamma_e, label="Ambipolar Transport code fluxes")
        ax.plot(r, T_e.particles.flux, label="Transport code")
        if logscale:
            ax.set_yscale("log")
        ax.set_title("Particle fluxes for electrons")
        ax.set_xlabel("rho_tor_norm")
        ax.set_ylabel("Particle flux density")
        ax.legend()

    def _validateElectrons(self, T_e, C_e, r, modelIndex):
        if len(r) != len(C_e.density):
            logger.critical(
                "core_profiles.profiles_1d[-1].electrons.density could not be read"
            )
            C_e.density = C_e.density[: len(r)]
        if len(r) != len(C_e.temperature):
            logger.critical(
                "core_profiles.profiles_1d[-1].electrons.temperature could not be read"
            )
            C_e.temperature = C_e.temperature[: len(r)]
        if len(T_e.particles.flux) < 1:
            logger.critical(
                f"core_transport.model[{modelIndex}].profiles_1d[-1].electrons.particles.flux could not be read"
            )
            T_e.particles.flux = np.asarray([np.nan] * r)
        if len(T_e.energy.d) < 1:
            logger.critical(
                f"core_transport.model[{modelIndex}].profiles_1d[-1].electrons.energy.d could not be read"
            )
            T_e.energy.d = np.asarray([np.nan] * r)
        if len(T_e.energy.v) < 1:
            logger.critical(
                f"core_transport.model[{modelIndex}].profiles_1d[-1].electrons.energy.v could not be read"
            )
            T_e.energy.v = np.asarray([np.nan] * r)
        if len(T_e.energy.flux) < 1:
            logger.critical(
                f"core_transport.model[{modelIndex}].profiles_1d[-1].electrons.energy.flux could not be read"
            )
            T_e.energy.flux = np.asarray([np.nan] * r)

    def _validateIonsData(self, T_i, C_i, r, modelIndex):
        if len(C_i.density) < 1:
            logger.critical(
                "core_profiles.profiles_1d[-1].ion.density could not be read"
            )
            C_i.density = np.asarray([np.nan] * r)

        if len(r) != len(C_i.density):
            logger.critical(
                "core_profiles.profiles_1d[-1].ion.density length is not the same as rho_tor_norm length, correcting the length"
            )
            C_i.density = C_i.density[: len(r)]
        if len(C_i.temperature) < 1:
            logger.critical(
                "core_profiles.profiles_1d[-1].ion.temperature could not be read"
            )
            C_i.temperature = np.asarray([np.nan] * r)
        if len(r) != len(C_i.temperature):
            logger.critical(
                "core_profiles.profiles_1d[-1].ion.temperature length is not the same as rho_tor_norm length, correcting the length"
            )
            C_i.temperature = C_i.temperature[: len(r)]

        if len(T_i.particles.d) < 1:
            logger.critical(
                f"core_transport.model[{modelIndex}].ion.particles.d could not be read"
            )
            T_i.particles.d = np.asarray([np.nan] * r)
        if len(T_i.particles.v) < 1:
            logger.critical(
                f"core_transport.model[{modelIndex}].ion.particles.v could not be read"
            )
            T_i.particles.v = np.asarray([np.nan] * r)
        if len(T_i.particles.flux) < 1:
            logger.critical(
                f"core_transport.model[{modelIndex}].ion.particles.flux could not be read"
            )
            T_i.particles.flux = np.asarray([np.nan] * r)
        if len(T_i.energy.d) < 1:
            logger.critical(
                f"core_transport.model[{modelIndex}].ion.energy.d could not be read"
            )
            T_i.energy.d = np.asarray([np.nan] * r)
        if len(T_i.energy.v) < 1:
            logger.critical(
                f"core_transport.model[{modelIndex}].ion.energy.v could not be read"
            )
            T_i.energy.v = np.asarray([np.nan] * r)
        if len(T_i.energy.flux) < 1:
            logger.critical(
                f"core_transport.model[{modelIndex}].ion.energy.flux could not be read"
            )
            T_i.energy.flux = np.asarray([np.nan] * r)
