from idstools.view.common import BasePlot
from idstools.compute.waves import WavesCompute

import numpy as np
import logging

logger = logging.getLogger(f"module.{__name__}")


class WavesView:
    def __init__(self, ids):
        self.wavesCompute = WavesCompute(ids)
        self.ids = ids

    def plotPolViewTraces(
        self, ax, timeIndex, color="b", style="-", label="", fontsize=9, labelpad=-1
    ):
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

    def plotTopViewTraces(
        self, ax, timeIndex, color="b", style="-", label="", fontsize=9, labelpad=-1
    ):
        ax.set_title("Top View (X,Y)", fontsize=fontsize)
        ax.set_xlabel("X [m]", fontsize=fontsize, labelpad=labelpad)
        ax.set_ylabel("Y [m]", fontsize=fontsize, labelpad=labelpad)

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

    def plotElectronPower(
        self, ax, timeIndex, color="b", style="-", label="", fontsize=9, labelpad=-1
    ):
        ax.set_title("Power along the beams", fontsize=fontsize)
        ax.set_xlabel("Path length [m]", fontsize=fontsize, labelpad=labelpad)
        ax.set_ylabel("P$_{electrons}$ [MW]", fontsize=fontsize, labelpad=labelpad)

        beamTracingDict = self.wavesCompute.getBeamTracing(timeIndex)
        beamElectronsLengthForEachWave = beamTracingDict[
            "beamElectronsLengthForEachWave"
        ]

        lengthData = beamTracingDict["length"]
        electronspowerData = beamTracingDict["electronspower"]
        displayLabelOnce = True
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
        ax.legend(loc="upper left", shadow=True, fancybox=True)

    def plotPowerFlowNormal(
        self, ax, timeIndex, color="b", style="-", label="", fontsize=9, labelpad=-1
    ):
        ax.set_ylabel(
            "P$_\parallel$/P$_{max}$ [-]", fontsize=fontsize, labelpad=labelpad
        )
        ax.set_xlabel("Path length [m]", fontsize=fontsize, labelpad=labelpad)
        ax.set_ylabel("P$_\perp$/P$_{max}$ [-]", fontsize=fontsize, labelpad=labelpad)

        beamTracingDict = self.wavesCompute.getBeamTracing(timeIndex)
        beamElectronsLengthForEachWave = beamTracingDict[
            "beamElectronsLengthForEachWave"
        ]

        lengthData = beamTracingDict["length"]
        powerparallelData = beamTracingDict["powerparallel"]
        powerperpendicularData = beamTracingDict["powerperpendicular"]
        for i in range(len(lengthData)):
            for j in range(len(lengthData[i])):
                dlength = beamElectronsLengthForEachWave[i][j]
                length = lengthData[i][j]
                powerparallel = powerparallelData[i][j]
                powerperpendicular = powerperpendicularData[i][j]

                ax.plot(
                    length[:dlength],
                    powerparallel[:dlength],
                    color=color,
                    linestyle=style,
                )
                ax.plot(
                    length[:dlength],
                    powerperpendicular[:dlength],
                    color=color,
                    linestyle=style,
                )
        ax.legend(loc="upper left", shadow=True, fancybox=True)


# -----------------------------------------------------------------------------------------------------------------------

#       def plotBeamIndex(self, ax):
#         """
#         This function plots a bar graph of beam indices with a fixed height of 20.

#         Args:
#             ax: ax is a matplotlib axis object
#         """
#         # TODO add callback function which can be called whenever there is update requested on timeline
#         beam_array = self.wavesCompute.getBeamArray()
#         ax.bar(beam_array, 20, color="g", width=0.5)

#         ax.set_xlim(beam_array[0] - 1, beam_array[-1] + 1)
#         ax.set_ylim(top=20)

#     # time_index_wv, beam_index

#     def plotPoloidalTraces(
#         self, ax, beamTracingTimeIndex, beamIndex, verbose=False, update=1
#     ):
#         # Read beam tracing from waves IDS
#         beam_tracing = self.wavesCompute.getBeamTracing(beamTracingTimeIndex)
#         nbeam = beam_tracing["nbeam"]
#         nbeam_active = beam_tracing["nbeam_active"]
#         nray = beam_tracing["nray"]
#         is_active = beam_tracing["is_active"]
#         len_ray = beam_tracing["len_ray"]
#         z_ray = beam_tracing["z_ray"]
#         r_ray = beam_tracing["r_ray"]

#         if verbose == True:
#             if nbeam_active > 1:
#                 logger.info(
#                     "There are "
#                     + str(nbeam_active)
#                     + " active beam"
#                     + int(nbeam_active != 1) * "s and each beam has "
#                     + str(nray)
#                     + " ray"
#                     + int(nray != 1) * "s"
#                 )
#             else:
#                 logger.info(
#                     f"There is "
#                     + str(nbeam_active)
#                     + " active beam and each beam has "
#                     + str(nray)
#                     + " ray"
#                     + int(nray != 1) * "s"
#                 )

#         ax_polview_plot_traces = {}
#         # for ibeam in range(nbeam):
#         # ax_polview_plot_traces[ibeam] = {}
#         if is_active[beamIndex] == 1:
#             for iray in range(nray):
#                 # TODO: update mechanism needs to be centralized
#                 if update == True:
#                     (ax_polview_plot_traces[iray],) = ax.plot(
#                         r_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
#                         z_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
#                         color="b",
#                         linestyle="-",
#                     )
#                 else:
#                     ax[iray].set_data(
#                         r_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
#                         z_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
#                     )
#         if update == True:
#             return ax_polview_plot_traces

#     def plotTopviewTraces(
#         self, ax, beamTracingTimeIndex, beamIndex, verbose=False, update=True
#     ):
#         # Read beam tracing from waves IDS
#         beam_tracing = self.wavesCompute.getBeamTracing(beamTracingTimeIndex)
#         nbeam = beam_tracing["nbeam"]
#         is_active = beam_tracing["is_active"]
#         len_ray = beam_tracing["len_ray"]
#         x_ray = beam_tracing["x_ray"]
#         y_ray = beam_tracing["y_ray"]

#         nray = beam_tracing["nray"]
#         if verbose == True:
#             nbeam_active = beam_tracing["nbeam_active"]
#             if nbeam_active > 1:
#                 print(
#                     f"There are {str(nbeam_active)} active beam"
#                     + int(nbeam_active != 1) * "s and each beam has "
#                     + str(nray)
#                     + " ray"
#                     + int(nray != 1) * "s"
#                 )
#             else:
#                 print(
#                     f"There is {str(nbeam_active)} active beam and each beam has {str(nray)} ray"
#                     + int(nray != 1) * "s"
#                 )

#         ax_topview_plot_traces = {}
#         # for ibeam in range(nbeam):
#         # ax_topview_plot_traces[ibeam] = {}
#         if is_active[beamIndex] == 1:
#             color = "b"
#             style = "-"

#             for iray in range(nray):
#                 if update == 1:
#                     (ax_topview_plot_traces[iray],) = ax.plot(
#                         x_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
#                         y_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
#                         color=color,
#                         linestyle=style,
#                     )
#                 else:
#                     ax[iray].set_data(
#                         x_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
#                         y_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
#                     )
#         if update == 1:
#             return ax_topview_plot_traces
