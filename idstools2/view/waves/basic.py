from ...view.common.basic import BasePlot
from ...compute.waves.basic import WavesCompute


import logging

logger = logging.getLogger(f"module.{__name__}")


class WavesView:
    def __init__(self, ids):
        self.wavesCompute = WavesCompute(ids)
        self.ids = ids

    def plotBeamIndex(self, ax):
        """
        This function plots a bar graph of beam indices with a fixed height of 20.

        Args:
            ax: ax is a matplotlib axis object
        """
        #TODO add callback function which can be called whenever there is update requested on timeline
        beam_array = self.wavesCompute.getBeamArray()
        ax.bar(beam_array, 20, color="g", width=0.5)

        ax.set_xlim(beam_array[0] - 1, beam_array[-1] + 1)
        ax.set_ylim(top=20)

    # time_index_wv, beam_index

    def plotPoloidalTraces(
        self, ax, beamTracingTimeIndex, beamIndex, verbose=False, update=1
    ):
        # Read beam tracing from waves IDS
        beam_tracing = self.wavesCompute.getBeamTracing(beamTracingTimeIndex)
        nbeam = beam_tracing["nbeam"]
        nbeam_active = beam_tracing["nbeam_active"]
        nray = beam_tracing["nray"]
        is_active = beam_tracing["is_active"]
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
        # for ibeam in range(nbeam):
        # ax_polview_plot_traces[ibeam] = {}
        if is_active[beamIndex] == 1:
            for iray in range(nray):
                # TODO: update mechanism needs to be centralied
                if update == True:
                    (ax_polview_plot_traces[iray],) = ax.plot(
                        r_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
                        z_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
                        color="b",
                        linestyle="-",
                    )
                else:
                    ax[iray].set_data(
                        r_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
                        z_ray[beamIndex, iray, : len_ray[beamIndex, iray]],
                    )
        if update == True:
            return ax_polview_plot_traces

    def plotTopviewTraces(
        self, ax, beamTracingTimeIndex, beamIndex, verbose=False, update=True
    ):
        # Read beam tracing from waves IDS
        beam_tracing = self.wavesCompute.getBeamTracing(beamTracingTimeIndex)
        nbeam = beam_tracing["nbeam"]
        is_active = beam_tracing["is_active"]
        len_ray = beam_tracing["len_ray"]
        x_ray = beam_tracing["x_ray"]
        y_ray = beam_tracing["y_ray"]

        nray = beam_tracing["nray"]
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
                    f"There is {str(nbeam_active)} active beam and each beam has {str(nray)} ray"
                    + int(nray != 1) * "s"
                )

        ax_topview_plot_traces = {}
        # for ibeam in range(nbeam):
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
