import itertools
import logging

import matplotlib.pyplot as plt

from idstools.compute.distribution_sources import DistributionSourcesCompute
from idstools.view.common import BasePlot

logger = logging.getLogger(f"module.{__name__}")


class DistributionSourcesView(BasePlot):
    def __init__(self, ids):
        self.distribution_sources_compute = DistributionSourcesCompute(ids)
        self.ids = ids

    def view_neutrons(self, ax: plt.axes, time_slice=0):
        rho_tor_norm = self.distribution_sources_compute.get_rho_tor_norm(time_slice)
        nrho = len(rho_tor_norm)
        if rho_tor_norm is not None and nrho == 0:
            logger.critical("distribution_sources.source[0].profiles_1d[0].grid.rho_tor_norm) is empty")
            return

        sources = self.distribution_sources_compute.get_source_info(time_slice)
        if len(sources) > 32:
            sources = dict(itertools.islice(sources.items(), 32))
        for key, source in sources.items():
            ax.plot(rho_tor_norm, source["particles"], label=source["label"])
            logger.info(
                f' {source["label"]}; P = ' + "%.2f" % (source["powerInKW"]) + " kW",
            )

        # Set Plot properties
        font_args = {
            "fontfamily": "serif",
            "color": "darkred",
            "fontweight": "normal",
            "fontsize": 12,
        }
        ax.tick_params(
            which="both",
            labelsize=12,
        )
        ax.set_xlim(rho_tor_norm[0], rho_tor_norm[nrho - 1])
        ax.set_xlabel(r"$\rho/\rho_0$", font_args, labelpad=1)
        ax.set_ylabel(r"Neutron rate ($s^{-1}.m{^{-3}}$)", font_args, labelpad=0)

        # set legend
        # legx_pos = 1.35
        # legy_pos = 1.05
        legend = ax.legend(loc="upper right")
        frame = legend.get_frame()
        frame.set_facecolor("0.95")
        for label in legend.get_texts():
            label.set_fontsize(7)
        for label in legend.get_lines():
            label.set_linewidth(1.5)

    def view_time(self, ax: plt.axes, time: float):
        ax_time = ax.twiny()
        ymin, ymax = ax.get_ylim()
        ax_time.plot(
            [time, time],
            [ymin, ymax],
            color="gray",
            linestyle="--",
            linewidth=1,
            label=r"$t_{slice}$",
        )
        ax_time.set_ylim(ymin, ymax)

    def view_pulse_info(self, ax: plt.axes, title: str, hostdir: str, shot: int, run: int, t: float):
        self.database_info(ax, title, hostdir, shot, run, t)
