import itertools
import logging

import matplotlib.pyplot as plt

from ..compute.distribution_sources import DistributionSourcesCompute
from idstools.view.common import BasePlot

logger = logging.getLogger(f"module.{__name__}")


class DistributionSourcesView(BasePlot):
    def __init__(self, ids):
        self.distributionSourcesCompute = DistributionSourcesCompute(ids)
        self.ids = ids

    def viewNeutrons(self, ax: plt.axes):
        rhoTorNorm = self.distributionSourcesCompute.getRhoTorNorm()
        nrho = len(rhoTorNorm)
        if rhoTorNorm is not None and nrho == 0:
            logger.critical(
                "distribution_sources.source[0].profiles_1d[0].grid.rho_tor_norm) is empty"
            )
            return

        sources = self.distributionSourcesCompute.getSourceInfo()
        if len(sources) > 32:
            sources = dict(itertools.islice(sources.items(), 32))
        for key, source in sources.items():
            ax.plot(rhoTorNorm, source["particles"], label=source["label"])
            logger.info(
                f' {source["label"]}; P = ' + "%.2f" % (source["powerInKW"]) + " kW",
            )

        # Set Plot properties
        fontArgs = {
            "fontfamily": "serif",
            "color": "darkred",
            "fontweight": "normal",
            "fontsize": 12,
        }
        ax.tick_params(
            which="both",
            labelsize=12,
        )
        ax.set_xlim(rhoTorNorm[0], rhoTorNorm[nrho - 1])
        ax.set_xlabel(r"$\rho/\rho_0$", fontArgs, labelpad=1)
        ax.set_ylabel(r"Neutron rate ($s^{-1}.m{^{-3}}$)", fontArgs, labelpad=0)
        ax.grid(b=True)

        # set legend
        legx_pos = 1.35
        legy_pos = 1.05
        legend = ax.legend(bbox_to_anchor=(legx_pos - 0.35, legy_pos - 0.05))
        frame = legend.get_frame()
        frame.set_facecolor("0.95")
        for label in legend.get_texts():
            label.set_fontsize(7)
        for label in legend.get_lines():
            label.set_linewidth(1.5)

    def viewTime(self, ax: plt.axes, time: float):
        axTime = ax.twiny()
        ymin, ymax = ax.get_ylim()
        axTime.plot(
            [time, time],
            [ymin, ymax],
            color="gray",
            linestyle="--",
            linewidth=1,
            label=r"$t_{slice}$",
        )
        axTime.set_ylim(ymin, ymax)

    def viewPulseInfo(
        self, ax: plt.axes, title: str, hostdir: str, shot: int, run: int, t: float
    ):
        self.database_info(ax, title, hostdir, shot, run, t)
