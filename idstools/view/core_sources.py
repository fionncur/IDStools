import logging

import numpy as np
from rich.align import Align
from rich.console import Console
from rich.table import Table

from idstools.compute.core_sources import CoreSourcesCompute

logger = logging.getLogger(f"module.{__name__}")


class CoreSourcesView:
    def __init__(self, ids):
        self.coreSourcesCompute = CoreSourcesCompute(ids)
        self.ids = ids

    def viewSources(self):
        """
        The `viewSources` function prints information about sources, including their name, electron
        flux, energy flux, and ion flux.
        """
        sourcesDict = self.coreSourcesCompute.getFluxInfoFromSources()
        ionTable = Table(show_header=False)
        for _, sourceDict in sourcesDict.items():
            # electrons
            if sourceDict["particles_flux"] is None:
                eparticles_flux = "particles(--)"
            else:
                eparticles_flux = f"particles ({sourceDict['particles_flux'] : >.6e})"
            if sourceDict["energy_flux"] is None:
                eenergy_flux = "energy(--)"
            else:
                eenergy_flux = f"energy ({sourceDict['energy_flux']: >.6e})"
            ionTable.add_row(
                f'{sourceDict["name"]}',
                eparticles_flux,
                eenergy_flux,
                "",
                "",
                style="bold magenta",
            )
            # ions
            ionTable.add_section()
            ionTable.add_row(
                Align.right("a"),
                Align.right("z_n"),
                Align.right("z_ion"),
                Align.right("particles"),
                Align.right("energy"),
                style="bold red",
            )

            for _, ionDict in sourceDict["ions"].items():
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

    def viewPowerProfiles(self, ax, *args, **kwargs):
        """
        The function `viewPowerProfiles` plots power profiles for different sources

        Args:
            ax: The parameter `ax` is an instance of the `Axes` class from the `matplotlib.pyplot` module. It represents the axes on which the power profiles will be plotted.
        """
        if self.coreSourcesCompute.isActiveSourceAvailable():
            rho_tor_norm = self.coreSourcesCompute.getRhoTorNorm()
            singleAndTotalElectronsProfiles = (
                self.coreSourcesCompute.getSingleAndTotalElectronsProfiles()
            )
            singleAndTotalIonProfiles = (
                self.coreSourcesCompute.getSingleAndTotalIonProfiles()
            )
            sourceNames = self.coreSourcesCompute.getSourceNames()
            ax.set_title("Power Profiles [MW/M3]")
            ax.plot(
                rho_tor_norm,
                singleAndTotalElectronsProfiles["totalElectronPowerProfile"] * 1.0e-6,
                label=r"Total to electrons",
            )
            ax.plot(
                rho_tor_norm,
                singleAndTotalIonProfiles["totalIonPowerProfile"] * 1.0e-6,
                "--",
                label=r"Total to ions",
            )
            for isource, name in sourceNames.items():
                ax.plot(
                    rho_tor_norm,
                    singleAndTotalElectronsProfiles["singleElectronPowerProfile"][
                        isource
                    ]
                    * 1.0e-6,
                    label=name + " [" + str(isource) + "]" + " to electrons",
                )
                ax.plot(
                    rho_tor_norm,
                    singleAndTotalIonProfiles["singleIonPowerProfile"][isource]
                    * 1.0e-6,
                    "--",
                    label=name + " [" + str(isource) + "]" + " to ions",
                )
            ax.set_ylabel("Power to bulk $\mathrm{[MW/m^{3}]}$")
            ax.set_xlabel("Normalized toroidal flux coordinate")
            # set legend
            legend = ax.legend()
            frame = legend.get_frame()
            frame.set_facecolor("0.95")
            for label in legend.get_texts():
                label.set_fontsize(7)
            for label in legend.get_lines():
                label.set_linewidth(1.5)
            return 0
        else:
            logger.warning("viewPowerProfiles:No active sources available")
        return -1

    def viewParticlesProfiles(self, ax, *args, **kwargs):
        """
        The function `viewParticlesProfiles` plots particle density profiles for electrons and ions at different sources as a function of normalized toroidal flux coordinate.

        Args:
            ax: The parameter `ax` is an instance of the `Axes` class from the `matplotlib.pyplot` module. It represents the axes on which the particles profiles will be plotted.
        """
        if self.coreSourcesCompute.isActiveSourceAvailable():
            rho_tor_norm = self.coreSourcesCompute.getRhoTorNorm()
            singleAndTotalElectronsProfiles = (
                self.coreSourcesCompute.getSingleAndTotalElectronsProfiles()
            )
            singleAndTotalIonProfiles = (
                self.coreSourcesCompute.getSingleAndTotalIonProfiles()
            )
            sourceNames = self.coreSourcesCompute.getSourceNames()
            ax.set_title("PARTICLES PROFILES [/M3/S]")
            ax.plot(
                rho_tor_norm,
                singleAndTotalElectronsProfiles["totalElectronParticlesProfile"]
                * 1.0e-6,
                label=r"Total to electrons",
            )
            ax.plot(
                rho_tor_norm,
                singleAndTotalIonProfiles["totalIonParticlesProfile"] * 1.0e-6,
                "--",
                label=r"Total to ions",
            )
            for isource, name in sourceNames.items():
                ax.plot(
                    rho_tor_norm,
                    singleAndTotalElectronsProfiles["singleElectronParticlesProfile"][
                        isource
                    ]
                    * 1.0e-6,
                    label=name + " [" + str(isource) + "]" + " electrons",
                )
                ax.plot(
                    rho_tor_norm,
                    singleAndTotalIonProfiles["singleIonParticlesProfile"][isource]
                    * 1.0e-6,
                    "--",
                    label=name + " [" + str(isource) + "]" + " ions",
                )
            ax.set_ylabel("Density $\mathrm{[m^{-3}.s^{-1}]}$")
            ax.set_xlabel("Normalized toroidal flux coordinate")
            # set legend
            legend = ax.legend()
            frame = legend.get_frame()
            frame.set_facecolor("0.95")
            for label in legend.get_texts():
                label.set_fontsize(7)
            for label in legend.get_lines():
                label.set_linewidth(1.5)
            return 0
        else:
            logger.warning("viewParticlesProfiles:No active sources available")
        return -1

    def viewCurrentProfiles(self, ax, *args, **kwargs):
        """
        The function `viewCurrentProfiles` plots current profiles.

        Args:
            ax: The parameter `ax` is an instance of the `Axes` class from the `matplotlib.pyplot` module. It represents the axes on which the current profiles will be plotted.
        """
        if self.coreSourcesCompute.isActiveSourceAvailable():
            rho_tor_norm = self.coreSourcesCompute.getRhoTorNorm()
            singleAndTotalElectronsAndIonsProfiles = (
                self.coreSourcesCompute.getSingleAndTotalElectronsAndIonsProfiles()
            )
            sourceNames = self.coreSourcesCompute.getSourceNames()
            ax.set_title("CURRENT PROFILES [KA/M2]")
            ax.plot(
                rho_tor_norm,
                singleAndTotalElectronsAndIonsProfiles["totalCurrentProfile"] * 1.0e-3,
                label=r"Total current",
            )
            for isource, name in sourceNames.items():
                if (
                    len(
                        singleAndTotalElectronsAndIonsProfiles["singleCurrentProfile"][
                            isource
                        ]
                    )
                    > 0
                ):
                    ax.plot(
                        rho_tor_norm,
                        singleAndTotalElectronsAndIonsProfiles["singleCurrentProfile"][
                            isource
                        ]
                        * 1.0e-3,
                        label=name + str(isource),
                    )
            ax.set_ylabel("Current density $\mathrm{[kA/m^{2}]}$")
            ax.set_xlabel("Normalized toroidal flux coordinate")
            # set legend
            legend = ax.legend()
            frame = legend.get_frame()
            frame.set_facecolor("0.95")
            for label in legend.get_texts():
                label.set_fontsize(7)
            for label in legend.get_lines():
                label.set_linewidth(1.5)
            return 0
        else:
            logger.warning("viewCurrentProfiles:No active sources available")
        return -1

    def viewPowerAndParticleWaveforms(self, ax, *args, **kwargs):
        """
        The function `viewPowerAndParticleWaveforms` plots power waveforms for different sources and particles over time.

        Args:
            ax: The parameter `ax` is an instance of the `Axes` class from the `matplotlib.pyplot` module. It represents the axes on which the waveforms will be plotted.
        """
        if self.coreSourcesCompute.isActiveSourceAvailable():
            ntime = len(self.ids.time)
            if ntime == 1:
                logger.warning("Only one time slice --> Waveforms not displayed")
            else:
                timeArray = self.ids.time
                singleAndTotalElectronsIonsWaveforms = (
                    self.coreSourcesCompute.getSingleAndTotalElectronsIonsWaveforms()
                )
                singleAndTotalElectronsWaveforms = (
                    self.coreSourcesCompute.getSingleAndTotalElectronsWaveforms()
                )
                singleAndTotalIonsWaveforms = (
                    self.coreSourcesCompute.getSingleAndTotalIonsWaveforms()
                )
                sourceNames = self.coreSourcesCompute.getSourceNames()
                ax.set_title("POWER AND PARTICLE WAVEFORMS")
                ax.plot(
                    timeArray,
                    singleAndTotalElectronsIonsWaveforms["total_power_waveform"]
                    * 1.0e-6,
                    label=r"Total electrons+ions",
                )
                ax.plot(
                    timeArray,
                    singleAndTotalElectronsWaveforms["total_electron_power_waveform"]
                    * 1.0e-6,
                    label=r"Total electrons",
                )
                ax.plot(
                    timeArray,
                    singleAndTotalIonsWaveforms["total_ion_power_waveform"] * 1.0e-6,
                    label=r"Total ions",
                )

                for isource, name in sourceNames.items():
                    ax.plot(
                        timeArray,
                        singleAndTotalElectronsIonsWaveforms["single_power_waveform"][
                            isource
                        ]
                        * 1.0e-6,
                        label=name + " [" + str(isource) + "]" + " electrons+ions",
                    )
                    ax.plot(
                        timeArray,
                        singleAndTotalElectronsWaveforms[
                            "single_electron_power_waveform"
                        ][isource]
                        * 1.0e-6,
                        label=name + " [" + str(isource) + "]" + " electrons",
                    )
                    ax.plot(
                        timeArray,
                        singleAndTotalIonsWaveforms["single_ion_power_waveform"][
                            isource
                        ]
                        * 1.0e-6,
                        label=name + " [" + str(isource) + "]" + " ions",
                    )
                ax.set_ylabel("Power waveforms $\mathrm{[MW]}$")
                ax.set_xlabel("Time (s)")
                # set legend
                legend = ax.legend()
                frame = legend.get_frame()
                frame.set_facecolor("0.95")
                for label in legend.get_texts():
                    label.set_fontsize(7)
                for label in legend.get_lines():
                    label.set_linewidth(1.5)
                return 0
        else:
            logger.warning("viewPowerAndParticleWaveforms:No active sources available")
        return -1

    def viewParticlesWaveform(self, ax, *args, **kwargs):
        """
        The function `viewParticlesWaveform` plots the waveforms of particles (electrons and ions) over time.

        Args:
            ax: The parameter "ax" is an instance of the matplotlib Axes class. It represents the axes on which the waveform plot will be drawn.
        """
        if self.coreSourcesCompute.isActiveSourceAvailable():
            ntime = len(self.ids.time)
            if ntime == 1:
                logger.warning("Only one time slice --> Waveforms not displayed")
            else:
                timeArray = self.ids.time
                singleAndTotalElectronsIonsWaveforms = (
                    self.coreSourcesCompute.getSingleAndTotalElectronsIonsWaveforms()
                )

                singleAndTotalElectronsWaveforms = (
                    self.coreSourcesCompute.getSingleAndTotalElectronsWaveforms()
                )

                singleAndTotalIonsWaveforms = (
                    self.coreSourcesCompute.getSingleAndTotalIonsWaveforms()
                )

                sourceNames = self.coreSourcesCompute.getSourceNames()
                ax.set_title("PARTICLES WAVEFORM")
                ax.plot(
                    timeArray,
                    singleAndTotalElectronsIonsWaveforms["total_particles_waveform"],
                    label=r"Total electrons+ions",
                )
                ax.plot(
                    timeArray,
                    singleAndTotalElectronsWaveforms[
                        "total_electron_particles_waveform"
                    ],
                    label=r"Total electrons",
                )
                ax.plot(
                    timeArray,
                    singleAndTotalIonsWaveforms["total_ion_particles_waveform"],
                    label=r"Total ions",
                )

                for isource, name in sourceNames.items():
                    ax.plot(
                        timeArray,
                        singleAndTotalElectronsIonsWaveforms[
                            "single_particles_waveform"
                        ][isource],
                        label=name + " [" + str(isource) + "]" + " electrons+ions",
                    )
                    ax.plot(
                        timeArray,
                        singleAndTotalElectronsWaveforms[
                            "single_electron_particles_waveform"
                        ][isource],
                        label=name + " [" + str(isource) + "]" + " electrons",
                    )
                    ax.plot(
                        timeArray,
                        singleAndTotalIonsWaveforms["single_ion_particles_waveform"][
                            isource
                        ],
                        label=name + " [" + str(isource) + "]" + " ions",
                    )
                ax.set_ylabel("Particles waveforms $\mathrm{[s^{-1}]}$")
                ax.set_xlabel("Time (s)")
                # set legend
                legend = ax.legend()
                frame = legend.get_frame()
                frame.set_facecolor("0.95")
                for label in legend.get_texts():
                    label.set_fontsize(7)
                for label in legend.get_lines():
                    label.set_linewidth(1.5)
                return 0
        else:
            logger.warning("viewParticlesWaveform:No active sources available")
        return -1

    def viewCurrentWaveform(self, ax, *args, **kwargs):
        """
        The function `viewCurrentWaveform` plots the current waveform for different sources and displays it.

        Args:
            ax: The parameter `ax` is an instance of the `Axes` class from the `matplotlib.pyplot` module. It represents the axes on which the waveform plot will be drawn.
        """
        if self.coreSourcesCompute.isActiveSourceAvailable():
            ntime = len(self.ids.time)
            if ntime == 1:
                logger.warning("Only one time slice --> Waveforms not displayed")
            else:
                timeArray = self.ids.time
                singleAndTotalCurrentTorque = (
                    self.coreSourcesCompute.getSingleAndTotalCurrentTorque()
                )
                sourceNames = self.coreSourcesCompute.getSourceNames()
                ax.set_title("CURRENT WAVEFORM")
                ax.plot(
                    timeArray,
                    singleAndTotalCurrentTorque["total_current_waveform"] * 1.0e-3,
                    label=r"Total electrons+ions",
                )

                for isource, name in sourceNames.items():
                    ax.plot(
                        timeArray,
                        singleAndTotalCurrentTorque["single_current_waveform"][isource]
                        * 1.0e-3,
                        label=name + " [" + str(isource) + "]" + " electrons+ions",
                    )

                ax.set_ylabel("Current waveforms $\mathrm{[kA.m]}$")
                ax.set_xlabel("Time (s)")
                # set legend
                legend = ax.legend()
                frame = legend.get_frame()
                frame.set_facecolor("0.95")
                for label in legend.get_texts():
                    label.set_fontsize(7)
                for label in legend.get_lines():
                    label.set_linewidth(1.5)
                return 0
        else:
            logger.warning("viewCurrentWaveform:No active sources available")
        return -1

    def viewTorqueWaveform(self, ax, *args, **kwargs):
        """
        The function `viewTorqueWaveform` plots torque waveforms for different sources over time.

        Args:
            ax: The parameter "ax" is an instance of the matplotlib Axes class. It represents the axes on which the torque waveform plot will be drawn.
        """

        if self.coreSourcesCompute.isActiveSourceAvailable():
            ntime = len(self.ids.time)
            if ntime == 1:
                logger.warning("Only one time slice --> Waveforms not displayed")
            else:
                timeArray = self.ids.time
                singleAndTotalCurrentTorque = (
                    self.coreSourcesCompute.getSingleAndTotalCurrentTorque()
                )
                sourceNames = self.coreSourcesCompute.getSourceNames()
                # TORQUE WAVEFORM
                ax.set_title("TORQUE WAVEFORM")
                ax.plot(
                    timeArray,
                    singleAndTotalCurrentTorque["total_torque_waveform"],
                    label=r"Total electrons+ions",
                )
                for isource, name in sourceNames.items():
                    ax.plot(
                        timeArray,
                        singleAndTotalCurrentTorque["single_torque_waveform"][isource],
                        label=name + " [" + str(isource) + "]" + " electrons+ions",
                    )

                ax.set_ylabel("Torque waveforms $\mathrm{[kg.m^2.s^{-2}]}$")
                ax.set_xlabel("Time (s)")
                # set legend
                legend = ax.legend()
                frame = legend.get_frame()
                frame.set_facecolor("0.95")
                for label in legend.get_texts():
                    label.set_fontsize(7)
                for label in legend.get_lines():
                    label.set_linewidth(1.5)
                return 0
        else:
            logger.warning("viewTorqueWaveform:No active sources available")
        return -1
