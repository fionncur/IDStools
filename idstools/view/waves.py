from idstools.compute.common import findMaxima, findMinima, findfwhm
from idstools.view.common import BasePlot
from idstools.compute.waves import WavesCompute

import numpy as np
import logging

logger = logging.getLogger(f"module.{__name__}")


class WavesView:
    def __init__(self, ids):
        self.wavesCompute = WavesCompute(ids)
        self.ids = ids

    def plotPolViewTraces(self, ax, timeIndex, color="b", style="-", label="", fontsize=9, labelpad=-1):
        beamTracingDict = self.wavesCompute.getBeamTracing(timeIndex)
        beamDataLengthForEachWave = beamTracingDict["beamDataLengthForEachWave"]

        lengthData = beamTracingDict["length"]
        r_rayData = beamTracingDict["r_ray"]
        z_rayData = beamTracingDict["z_ray"]
        displayLabelOnce = True
        for i in range(len(lengthData)):
            for j in range(len(lengthData[i])):
                length = beamDataLengthForEachWave[i][j]
                r_ray = r_rayData[i][j]
                z_ray = z_rayData[i][j]
                ax.plot(
                    r_ray[:length],
                    z_ray[:length],
                    color=color,
                    linestyle=style,
                    label=label,
                )
                if displayLabelOnce is True:
                    displayLabelOnce = False
                    label = ""

    def plotTopViewTraces(self, ax, timeIndex, color="b", style="-", label="", fontsize=9, labelpad=-1):
        ax.set_title("Top View (X,Y)", fontsize=fontsize)
        ax.set_xlabel("X [m]")
        ax.set_ylabel("Y [m]")

        beamTracingDict = self.wavesCompute.getBeamTracing(timeIndex)
        beamDataLengthForEachWave = beamTracingDict["beamDataLengthForEachWave"]
        lengthData = beamTracingDict["length"]
        x_rayData = beamTracingDict["x_ray"]
        y_rayData = beamTracingDict["y_ray"]
        displayLabelOnce = True
        for i in range(len(lengthData)):
            for j in range(len(lengthData[i])):
                length = beamDataLengthForEachWave[i][j]
                x_ray = x_rayData[i][j]
                y_ray = y_rayData[i][j]

                ax.plot(
                    x_ray[:length],
                    y_ray[:length],
                    color=color,
                    linestyle=style,
                    label=label,
                )
                if displayLabelOnce is True:
                    displayLabelOnce = False
                    label = ""

    def plotElectronPower(self, ax, timeIndex, color="b", style="-", label="", fontsize=9, labelpad=-1):
        ax.set_title("Power along the beams", fontsize=fontsize)
        ax.set_xlabel("Path length [m]")
        ax.set_ylabel("P$_{electrons}$ [MW]")

        beamTracingDict = self.wavesCompute.getBeamTracing(timeIndex)
        beamElectronsLengthForEachWave = beamTracingDict["beamElectronsLengthForEachWave"]

        lengthData = beamTracingDict["length"]
        electronspowerData = beamTracingDict["electronspower"]
        displayLabelOnce = True
        label = "Electrons Power [W]"
        for i in range(len(lengthData)):
            for j in range(len(lengthData[i])):
                dlength = beamElectronsLengthForEachWave[i][j]
                length = lengthData[i][j]
                electronspower = electronspowerData[i][j]

                ax.plot(
                    length[:dlength],
                    electronspower[:dlength] * 1.0e-6,
                    color=color,
                    linestyle=style,
                    label=label,
                )
                if displayLabelOnce is True:
                    displayLabelOnce = False
                    label = ""
        ax.legend()

    def plotPowerFlowNormal(self, ax, timeIndex, color="b", style="-", label="", fontsize=9, labelpad=-1):
        ax.set_title("Power flow to the magnetic field", fontsize=fontsize)
        ax.set_xlabel("Path length [m]")

        beamTracingDict = self.wavesCompute.getBeamTracing(timeIndex)
        beamElectronsLengthForEachWave = beamTracingDict["beamElectronsLengthForEachWave"]

        lengthData = beamTracingDict["length"]
        powerparallelData = beamTracingDict["powerparallel"]
        powerperpendicularData = beamTracingDict["powerperpendicular"]
        perplabel = "P$_\perp$/P$_{max}$ [-]"
        parlabel = "P$_\parallel$/P$_{max}$ [-]"
        displayLabelOnce = True
        for i in range(len(lengthData)):
            for j in range(len(lengthData[i])):
                dlength = beamElectronsLengthForEachWave[i][j]
                length = lengthData[i][j]
                powerparallel = powerparallelData[i][j]
                powerperpendicular = powerperpendicularData[i][j]

                ax.plot(
                    length[:dlength],
                    powerparallel[:dlength],
                    color="b",
                    linestyle=style,
                    label=parlabel,
                )
                ax.plot(
                    length[:dlength],
                    powerperpendicular[:dlength],
                    color="r",
                    linestyle=style,
                    label=perplabel,
                )
                if displayLabelOnce is True:
                    displayLabelOnce = False
                    perplabel = ""
                    parlabel = ""
        ax.legend()

    def plotECRHProfiles(
        self,
        ax,
        timeIndex,
        verbose=False,
    ):
        # ECRH PROFILE [MA/M2]
        ecLauncherInfo = self.wavesCompute.GetECLaunchersInfo(timeIndex)
        radialGrid = self.wavesCompute.getRadialGridInfo(timeIndex)
        activeLaunchers = {key: value for key, value in radialGrid.items() if value["isActive"] is True}
        _, firstRadialGridInfo = next(iter(activeLaunchers.items()))

        codeName = self.ids.code.name.upper()
        ax.set_title("ECRH Profiles")
        lenActiveLaunchers = len(activeLaunchers)
        if lenActiveLaunchers != 0:
            totalx1 = firstRadialGridInfo["rho_tor_norm"]
            totaly1 = ecLauncherInfo["total_power_density_profile"] * 1.0e-6
            totallabel1 = f"Total-{codeName}"

            ax.plot(totalx1, totaly1, label=totallabel1)
            if verbose:
                maxima = findMaxima(totaly1)
                logger.info(f"There are {len(maxima)-1} maxima")
                fwhm = []
                # fmt: off
                for i in range(len(maxima)):
                    if i == 0:
                        fwhm.append(findfwhm(totalx1,totaly1,maxima[0],0,(maxima[0] + maxima[1]) // 2,))
                    elif i == len(maxima) - 1:
                        fwhm.append(findfwhm(totalx1,totaly1,maxima[i],(maxima[i - 1] + maxima[i]) // 2,len(totaly1),))
                        logger.info(f"({totalx1[maxima[i]]}, {totaly1[maxima[i]]} --- fwhm: {fwhm[i]})")
                    else:
                        fwhm.append(findfwhm(totalx1,totaly1,maxima[i],(maxima[i - 1] + maxima[i]) // 2,(maxima[i] + maxima[i + 1]) // 2,))
                        logger.info(f"({totalx1[maxima[i]]}, {totaly1[maxima[i]]} --- fwhm: {fwhm[i]})")
                # fmt: on

            for iWave, _ in activeLaunchers.items():
                ax.plot(
                    firstRadialGridInfo["rho_tor_norm"],
                    ecLauncherInfo["single_power_density_profile"][iWave] * 1.0e-6,
                    linestyle="--",
                    label=ecLauncherInfo["single_ec_launcher_name"][iWave],
                )
            ax.set_ylabel("Absorbed power $\mathrm{[MW/m^{3}]}$")
            if firstRadialGridInfo["psiBased"] is False:
                ax.set_xlabel("Normalized toroidal flux coordinate")
            else:
                ax.set_xlabel("-(Poloidal flux coordinate) [Wb]")
            ax.legend()

    def plotECCDProfiles(
        self,
        ax,
        timeIndex,
        verbose=False,
    ):
        # ECCD PROFILE [MA/M2]
        ecLauncherInfo = self.wavesCompute.GetECLaunchersInfo(timeIndex)

        radialGrid = self.wavesCompute.getRadialGridInfo(timeIndex)
        activeLaunchers = {key: value for key, value in radialGrid.items() if value["isActive"] is True}
        _, firstRadialGridInfo = next(iter(activeLaunchers.items()))

        codeName = self.ids.code.name.upper()
        ax.set_title("ECCD Profiles")

        lenActiveLaunchers = len(activeLaunchers)
        if lenActiveLaunchers != 0:
            totalx2 = firstRadialGridInfo["rho_tor_norm"]
            totaly2 = ecLauncherInfo["total_current_density_profile"] * 1.0e-6
            totallabel = f"Total-{codeName}"
            ax.plot(totalx2, totaly2, label=totallabel)
            if verbose:
                minima = findMinima(totaly2)
                logger.info(f"There are {len(minima)} minima")
                fwhm = []
                # fmt: off
                for i in range(len(minima)):
                    if (i == 0):
                        fwhm.append(findfwhm(totalx2,totaly2,minima[0],0,(minima[0]+minima[1])//2))
                    elif (i == len(minima) - 1):
                        fwhm.append(findfwhm(totalx2,totaly2,minima[i],(minima[i-1]+minima[i])//2,len(totaly2)))
                    else:
                        fwhm.append(findfwhm(totalx2,totaly2,minima[i],(minima[i-1]+minima[i])//2,(minima[i]+minima[i+1])//2))
                    logger.info(f'({totalx2[minima[i]]}, {totaly2[minima[i]]} --- fwhm: {fwhm[i]})')
                # fmt: on
            # logger.debug(fwhm)
        for iWave, _ in activeLaunchers.items():
            ax.plot(
                firstRadialGridInfo["rho_tor_norm"],
                ecLauncherInfo["single_current_density_profile"][iWave] * 1.0e-6,
                linestyle="--",
                label=ecLauncherInfo["single_ec_launcher_name"][iWave],
            )
        ax.set_ylabel("$\mathrm{ECCD} [MA/m^{2}]}$")
        if firstRadialGridInfo["psiBased"] is False:
            ax.set_xlabel("Normalized toroidal flux coordinate")
        else:
            ax.set_xlabel("-(Poloidal flux coordinate) [Wb]")
        ax.legend()

    def plotECRHWaveform(
        self,
        ax,
        timeIndex,
    ):
        timeArray = self.ids.time
        ntime = len(self.ids.time)
        ecLauncherInfo = self.wavesCompute.GetECLaunchersInfo(timeIndex)

        radialGrid = self.wavesCompute.getRadialGridInfo(timeIndex)
        activeLaunchers = {key: value for key, value in radialGrid.items() if value["isActive"] is True}

        codeName = self.ids.code.name.upper()

        ax.set_title("ECRH Waveforms")

        if ntime == 1:
            logger.error("Only one time slice --> ECRH and ECCD waveforms not displayed")
            return -1
        else:
            ax.set_title("ECRH Waveforms")
            ax.set_ylabel("Power to the electrons $\mathrm{[MW]}$")
            ax.set_xlabel("Time (s)")
            # EC POWER WAVEFORM
            if len(activeLaunchers) > 0:
                ax.plot(
                    timeArray,
                    np.array(ecLauncherInfo["total_power_waveform"]) * 1.0e-6,
                    label=f"Total-{codeName}",
                )
            for iWave, _ in activeLaunchers.items():
                ax.plot(
                    timeArray,
                    np.array(ecLauncherInfo["single_power_waveform"][iWave]) * 1.0e-6,
                    linestyle="--",
                    label=ecLauncherInfo["single_ec_launcher_name"][iWave],
                )
            ax.legend()
            return 0

    def plotECCDWaveform(
        self,
        ax,
        timeIndex,
    ):
        timeArray = self.ids.time
        ntime = len(self.ids.time)
        ecLauncherInfo = self.wavesCompute.GetECLaunchersInfo(timeIndex)

        radialGrid = self.wavesCompute.getRadialGridInfo(timeIndex)
        activeLaunchers = {key: value for key, value in radialGrid.items() if value["isActive"] is True}

        codeName = self.ids.code.name.upper()

        ax.set_title("ECCD Waveforms")

        if ntime == 1:
            logger.error("Only one time slice --> ECCD waveforms not displayed")
            return -1
        else:
            ax.set_title("ECCD Waveforms")
            ax.set_ylabel("ECCD $\mathrm{[kA]}$")
            ax.set_xlabel("Time (s)")
            # EC POWER WAVEFORM
            if len(activeLaunchers) > 0:
                ax.plot(
                    timeArray,
                    np.array(ecLauncherInfo["total_current_waveform"]) * 1.0e-3,
                    label=f"Total-{codeName}",
                )
            for iWave, _ in activeLaunchers.items():
                ax.plot(
                    timeArray,
                    np.array(ecLauncherInfo["single_current_waveform"][iWave]) * 1.0e-6,
                    linestyle="--",
                    label=ecLauncherInfo["single_ec_launcher_name"][iWave],
                )
            ax.legend()
            return 0

    def displayECLaunchersInfo(self, timeIndex):
        ecLauncherInfo = self.wavesCompute.GetECLaunchersInfo(timeIndex)

        launchers = self.wavesCompute.getRadialGridInfo(timeIndex)

        for iWave, waveData in launchers.items():
            if waveData["isActive"] is True:
                logger.info(
                    f"{ecLauncherInfo['single_ec_launcher_name'][iWave]} is active with a power of {ecLauncherInfo['single_injected_power'][iWave]*1.e-6:.2f} MW --> Absorbed power = {ecLauncherInfo['single_absorbed_power'][iWave]*1.e-6:.2f} MW"
                )
                logger.info(f"--> ECCD =  {ecLauncherInfo['single_eccd'][iWave]*1.e-3:.2f} kA")
            else:
                logger.info(f"{ecLauncherInfo['single_ec_launcher_name'][iWave]} is off")

    @staticmethod
    def customizeLegend(legend):
        frame = legend.get_frame()
        frame.set_facecolor("0.95")
        for label in legend.get_texts():
            label.set_fontsize(6)
        for label in legend.get_lines():
            label.set_linewidth(1.5)  # the legend line width
        return

    # CD WAVEFORM
    def viewCDWaveform(self, ax, timeIndex, usepsi=False):
        timeArray = self.ids.time
        ecLauncherInfo = self.wavesCompute.GetECLaunchersInfo(timeIndex, usepsi)

        radialGrid = self.wavesCompute.getRadialGridInfo(timeIndex, usepsi)

        activeLaunchers = {key: value for key, value in radialGrid.items() if value["isActive"] is True}
        lenActiveLaunchers = len(activeLaunchers)
        ax.set_title("Current density waveform")
        if lenActiveLaunchers != 0:
            ax.plot(
                timeArray,
                np.array(ecLauncherInfo["total_current_waveform"]) * 1.0e-3,
                label=r"Total",
            )
        for iwave, _ in activeLaunchers.items():
            ax.plot(
                timeArray,
                np.array(ecLauncherInfo["single_current_waveform"][iwave]) * 1.0e-3,
                label=ecLauncherInfo["single_ec_launcher_name"][iwave],
            )
        ax.set_ylabel("Current Density $\mathrm{[kA]}$")
        ax.set_xlabel("Time (s)")
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        WavesView.customizeLegend(legend)

    # EC POWER WAVEFORM
    def viewECPowerWaveform(self, ax, timeIndex, usepsi=False):
        timeArray = self.ids.time
        ecLauncherInfo = self.wavesCompute.GetECLaunchersInfo(timeIndex, usepsi)

        radialGrid = self.wavesCompute.getRadialGridInfo(timeIndex, usepsi)

        activeLaunchers = {key: value for key, value in radialGrid.items() if value["isActive"] is True}
        lenActiveLaunchers = len(activeLaunchers)
        ax.set_title("EC Power Waveform")
        if lenActiveLaunchers != 0:
            ax.plot(
                timeArray,
                np.array(ecLauncherInfo["total_power_waveform"]) * 1.0e-6,
                label=r"Total",
            )
        for iwave, _ in activeLaunchers.items():
            ax.plot(
                timeArray,
                np.array(ecLauncherInfo["single_power_waveform"][iwave]) * 1.0e-6,
                label=ecLauncherInfo["single_ec_launcher_name"][iwave],
            )
        ax.set_ylabel("Power to the electrons $\mathrm{[MW]}$")
        ax.set_xlabel("Time (s)")
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        WavesView.customizeLegend(legend)

    # CD PROFILE [MA/M2]
    def viewCDProfile(self, ax, timeIndex, usepsi=False):
        timeArray = self.ids.time
        ecLauncherInfo = self.wavesCompute.GetECLaunchersInfo(timeIndex, usepsi)

        radialGrid = self.wavesCompute.getRadialGridInfo(timeIndex, usepsi)

        activeLaunchers = {key: value for key, value in radialGrid.items() if value["isActive"] is True}
        _, firstRadialGridInfo = next(iter(activeLaunchers.items()))
        lenActiveLaunchers = len(activeLaunchers)
        ax.set_title("Current density profile")
        if lenActiveLaunchers != 0:
            ax.plot(
                firstRadialGridInfo["rho_tor_norm"],
                ecLauncherInfo["total_current_density_profile"] * 1.0e-6,
                label=r"Total",
            )
        for iwave, _ in activeLaunchers.items():
            if iwave in ecLauncherInfo["single_current_density_profile"]:
                ax.plot(
                    firstRadialGridInfo["rho_tor_norm"],
                    ecLauncherInfo["single_current_density_profile"][iwave] * 1.0e-6,
                    label=ecLauncherInfo["single_ec_launcher_name"][iwave],
                )
        ax.set_ylabel("$\mathrm{CD} [MA/m^{2}]}$")
        if firstRadialGridInfo["psiBased"] is False and usepsi == False:
            ax.set_xlabel("Normalized toroidal flux coordinate")
        else:
            ax.set_xlabel("-(Poloidal flux coordinate) [Wb]")
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        WavesView.customizeLegend(legend)

    # PROFILE OF ABSORBED POWER DENSITY [MW/M3]
    def viewAbsorbedPowerDensityProfile(self, ax, timeIndex, usepsi=False):
        timeArray = self.ids.time
        ecLauncherInfo = self.wavesCompute.GetECLaunchersInfo(timeIndex, usepsi, True)

        radialGrid = self.wavesCompute.getRadialGridInfo(timeIndex, usepsi)

        activeLaunchers = {key: value for key, value in radialGrid.items() if value["isActive"] is True}
        _, firstRadialGridInfo = next(iter(activeLaunchers.items()))
        lenActiveLaunchers = len(activeLaunchers)
        ax.set_title("Absorbed power density profile")
        if lenActiveLaunchers != 0:
            ax.plot(
                firstRadialGridInfo["rho_tor_norm"],
                ecLauncherInfo["total_power_density_profile"] * 1.0e-6,
                label=r"Total",
            )
        for iwave, _ in activeLaunchers.items():
            if iwave in ecLauncherInfo["single_power_density_profile"]:
                ax.plot(
                    firstRadialGridInfo["rho_tor_norm"],
                    ecLauncherInfo["single_power_density_profile"][iwave] * 1.0e-6,
                    label=ecLauncherInfo["single_ec_launcher_name"][iwave],
                )
        ax.set_ylabel("Absorbed power $\mathrm{[MW/m^{3}]}$")
        if firstRadialGridInfo["psiBased"] is False and usepsi == False:
            ax.set_xlabel("Normalized toroidal flux coordinate")
        else:
            ax.set_xlabel("-(Poloidal flux coordinate) [Wb]")
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        WavesView.customizeLegend(legend)

    def plotBeamIndex(self, ax):
        """
        This function plots a bar graph of beam indices with a fixed height of 20.

        Args:
            ax: ax is a matplotlib axis object
        """
        # TODO add callback function which can be called whenever there is update requested on timeline
        beam_array = self.wavesCompute.getBeamArray()
        bars = ax.bar(beam_array, 20, color="g", width=0.5)
        ax.set_xlim(beam_array[0] - 1, beam_array[-1] + 1)
        ax.set_ylim(top=20)

    def plotPoloidalTracesUpdate(self, ax, beamTracingTimeIndex, beamIndex, verbose=False, update=True):
        # Read beam tracing from waves IDS
        beam_tracing = self.wavesCompute.getBeamTracing(beamTracingTimeIndex)

        nbeam = beam_tracing["nbeam"]
        nbeam_active = beam_tracing["activeBeamsCount"]
        nray = beam_tracing["maxTotalBeams"]
        is_active = beam_tracing["beamActivaStatusList"]
        len_ray = beam_tracing["len_ray"]
        z_ray = beam_tracing["z_ray"]
        r_ray = beam_tracing["r_ray"]

        if verbose == True:
            if nbeam_active > 1:
                logger.info(
                    "There are "
                    + str(nbeam_active)
                    + " active beam"
                    + int(nbeam_active != 1) * "s and each beam has "
                    + str(nray)
                    + " ray"
                    + int(nray != 1) * "s"
                )
            else:
                logger.info(
                    f"There is "
                    + str(nbeam_active)
                    + " active beam and each beam has "
                    + str(nray)
                    + " ray"
                    + int(nray != 1) * "s"
                )

        ax_polview_plot_traces = {}

        for ibeam in range(nbeam):
            # ax_polview_plot_traces[ibeam] = {}
            if is_active[ibeam] is True:

                for iray in range(nray):
                    # TODO: update mechanism needs to be centralized
                    if update is True:

                        (ax_polview_plot_traces[iray],) = ax.plot(
                            r_ray[ibeam, iray, : len_ray[ibeam, iray]],
                            z_ray[ibeam, iray, : len_ray[ibeam, iray]],
                            color="b",
                            linestyle="-",
                        )
                    else:
                        ax[iray].set_data(
                            r_ray[ibeam, iray, : len_ray[ibeam, iray]],
                            z_ray[ibeam, iray, : len_ray[ibeam, iray]],
                        )
        return ax_polview_plot_traces

    def plotTopviewTracesUpdate(self, ax, beamTracingTimeIndex, beamIndex, verbose=False, update=True):
        # Read beam tracing from waves IDS
        beam_tracing = self.wavesCompute.getBeamTracing(beamTracingTimeIndex)
        nbeam = beam_tracing["nbeam"]
        is_active = beam_tracing["beamActivaStatusList"]
        len_ray = beam_tracing["len_ray"]
        x_ray = beam_tracing["x_ray"]
        y_ray = beam_tracing["y_ray"]

        nray = beam_tracing["maxTotalBeams"]
        if verbose == True:
            nbeam_active = beam_tracing["nbeam_active"]
            if nbeam_active > 1:
                print(
                    f"There are {str(nbeam_active)} active beam"
                    + int(nbeam_active != 1) * "s and each beam has "
                    + str(nray)
                    + " ray"
                    + int(nray != 1) * "s"
                )
            else:
                print(
                    f"There is {str(nbeam_active)} active beam and each beam has {str(nray)} ray" + int(nray != 1) * "s"
                )

        ax_topview_plot_traces = {}
        for beamIndex in range(nbeam):
            # ax_topview_plot_traces[ibeam] = {}
            if is_active[beamIndex] == 1:
                color = "b"
                style = "-"

                for iray in range(nray):
                    if update == 1:
                        (ax_topview_plot_traces[iray],) = ax.plot(
                            x_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
                            y_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
                            color=color,
                            linestyle=style,
                        )
                    else:
                        ax[iray].set_data(
                            x_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
                            y_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
                        )
        if update == 1:
            return ax_topview_plot_traces
