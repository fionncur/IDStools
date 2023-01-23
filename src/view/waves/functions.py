from ...view.common.functions import BasePlot
from ...compute.waves.functions import WavesCompute


class WavesView:
    def __init__(self, ids_object):
        self.waves_object = WavesCompute(ids_object)
        self.ids_object = ids_object

    def plot_beam_index(self, ax):
        beam_array = self.waves_object.get_beam_array()
        ax.bar(beam_array, 20, color="g", width=0.5)

        ax.set_xlim(beam_array[0] - 1, beam_array[-1] + 1)
        ax.set_ylim(top=20)

    # time_index_wv, beam_index

    def plot_poloidal_traces(
        self, ax, time_index_wv, beam_index, verbose=False, init=1
    ):

        # Read beam tracing from waves IDS
        beam_tracing = self.waves_object.read_beam_tracing(time_index_wv)
        nbeam = beam_tracing["nbeam"]
        nbeam_active = beam_tracing["nbeam_active"]
        nray = beam_tracing["nray"]
        is_active = beam_tracing["is_active"]
        len_ray = beam_tracing["len_ray"]
        z_ray = beam_tracing["z_ray"]
        r_ray = beam_tracing["r_ray"]

        if verbose == True:
            if nbeam_active > 1:
                print(
                    "There are "
                    + str(nbeam_active)
                    + " active beam"
                    + int(nbeam_active != 1) * "s and each beam has "
                    + str(nray)
                    + " ray"
                    + int(nray != 1) * "s"
                )
            else:
                print(
                    "There is "
                    + str(nbeam_active)
                    + " active beam and each beam has "
                    + str(nray)
                    + " ray"
                    + int(nray != 1) * "s"
                )

        ax_polview_plot_traces = {}
        # for ibeam in range(nbeam):
        # ax_polview_plot_traces[ibeam] = {}
        if is_active[beam_index] == 1:
            iray = -1
            for irray in range(nray):
                iray = iray + 1
                if init == 1:
                    (ax_polview_plot_traces[iray],) = ax.plot(
                        r_ray[beam_index, iray, : len_ray[beam_index, iray]],
                        z_ray[beam_index, iray, : len_ray[beam_index, iray]],
                        color="b",
                        linestyle="-",
                    )
                else:
                    ax[iray].set_data(
                        r_ray[beam_index, iray, : len_ray[beam_index, iray]],
                        z_ray[beam_index, iray, : len_ray[beam_index, iray]],
                    )
        if init == 1:
            return ax_polview_plot_traces

    def plot_topview_traces(self, ax, time_index_wv, beam_index, verbose=False, init=1):

        # Read beam tracing from waves IDS
        beam_tracing = self.waves_object.read_beam_tracing(time_index_wv)
        nbeam = beam_tracing["nbeam"]
        nbeam_active = beam_tracing["nbeam_active"]
        nray = beam_tracing["nray"]
        is_active = beam_tracing["is_active"]
        len_ray = beam_tracing["len_ray"]
        x_ray = beam_tracing["x_ray"]
        y_ray = beam_tracing["y_ray"]

        if verbose == True:
            if nbeam_active > 1:
                print(
                    "There are "
                    + str(nbeam_active)
                    + " active beam"
                    + int(nbeam_active != 1) * "s and each beam has "
                    + str(nray)
                    + " ray"
                    + int(nray != 1) * "s"
                )
            else:
                print(
                    "There is "
                    + str(nbeam_active)
                    + " active beam and each beam has "
                    + str(nray)
                    + " ray"
                    + int(nray != 1) * "s"
                )

        color = "b"
        style = "-"

        ax_topview_plot_traces = {}
        # for ibeam in range(nbeam):
        # ax_topview_plot_traces[ibeam] = {}
        if is_active[beam_index] == 1:
            iray = -1
            for irray in range(nray):
                iray = iray + 1
                if init == 1:
                    (ax_topview_plot_traces[iray],) = ax.plot(
                        x_ray[beam_index, iray, : len_ray[beam_index, iray]],
                        y_ray[beam_index, iray, : len_ray[beam_index, iray]],
                        color=color,
                        linestyle=style,
                    )
                else:
                    ax[iray].set_data(
                        x_ray[beam_index, iray, : len_ray[beam_index, iray]],
                        y_ray[beam_index, iray, : len_ray[beam_index, iray]],
                    )
        if init == 1:
            return ax_topview_plot_traces
