"""
This module provides view functions and classes for equilibrium ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

from idstools.compute.summary import SummaryCompute
from idstools.view.common import BasePlot

logger = logging.getLogger("module")


class SummaryView(BasePlot):
    def __init__(self, ids: object):
        """
        This is a constructor function that initializes an object with an input object and creates
        another object using the input object.

        Args:
            ids (object): The parameter `idsObj` is an object that is being passed to the constructor
                of the class. It is not clear from the code snippet what type of object it is, but it is being
                stored as an instance variable `self.idsObj`.
        """
        self.ids = ids
        self.compute_obj = SummaryCompute(ids)

    def view_hcd_waveforms(self, ax):
        """
        The function `view_hcd_waveforms` plots various power waveforms on a given axis.

        Args:
            ax: The `ax` parameter is an instance of the `Axes` class from the `matplotlib.pyplot` module. It
                represents the axes on which the waveforms will be plotted.
        """
        waveform = self.compute_obj.get_summary()
        plotstyle = "-" if len(waveform["time"]) > 1 else "o"
        if max(waveform["p_hcd"]) > 0:
            ax.plot(
                waveform["time"],
                waveform["p_hcd"] * 1.0e-6,
                plotstyle,
                label=r"$P_{HCD}$",
            )

        if max(waveform["p_ec"]) > 0:
            ax.plot(
                waveform["time"],
                waveform["p_ec"] * 1.0e-6,
                plotstyle,
                label=r"$P_{EC}$",
            )

        if max(waveform["p_ic"]) > 0:
            ax.plot(
                waveform["time"],
                waveform["p_ic"] * 1.0e-6,
                plotstyle,
                label=r"$P_{IC}$",
            )

        if max(waveform["p_nbi"]) > 0:
            ax.plot(
                waveform["time"],
                waveform["p_nbi"] * 1.0e-6,
                plotstyle,
                label=r"$P_{NBI}$",
            )

        if max(waveform["p_lh"]) > 0:
            ax.plot(
                waveform["time"],
                waveform["p_lh"] * 1.0e-6,
                plotstyle,
                label=r"$P_{LH}$",
            )

        # Fusion waveforms
        if max(waveform["p_fusion"]) > 0:
            ax.plot(
                waveform["time"],
                waveform["p_fusion"] * 1.0e-6,
                plotstyle,
                label=r"$P_{FUS}$",
            )

        if max(waveform["p_neutron"]) > 0:
            ax.plot(
                waveform["time"],
                waveform["p_neutron"] * 1.0e-6,
                plotstyle,
                label=r"$P_{NEUT}$",
            )

        if max(waveform["p_ohmic"]) > 0:
            ax.plot(
                waveform["time"],
                waveform["p_ohmic"] * 1.0e-6,
                plotstyle,
                label=r"$P_{OHM}$",
            )

        if max(waveform["p_steady"]) > 0:
            ax.plot(
                waveform["time"],
                waveform["p_steady"] * 1.0e-6,
                plotstyle,
                label=r"$P_{STEADY}$",
            )
        ax.set_xlim(self.ids.time[0], self.ids.time[-1])
        ax.set_ylabel(r"$P\/[\mathrm{MW}]$", fontdict={"color": "darkred"})
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    def view_ip_b0_waveforms(self, ax):
        """
        The function `view_ip_b0_waveforms` plots the absolute values of the Ip and B0 waveforms on a given axis.

        Args:
            ax: The parameter "ax" is an instance of the matplotlib Axes class. It represents the subplot where
                the Ip and B0 waveforms will be plotted.
        """
        waveform = self.compute_obj.get_summary()
        plotstyle = "-" if len(waveform["time"]) > 1 else "o"
        # Ip, B0 waveforms
        ax.plot(waveform["time"], abs(waveform["ip"]) * 1.0e-6, plotstyle, label=r"$|I_p|$")
        # ax.plot(waveform['time'],waveform['current_non_inductive']*1.e-6,label=r'$J_{NI}$')
        # ax.plot(waveform['time'],waveform['current_bootstrap']*1.e-6,label=r'$J_{BOOT}$')
        # ax.plot(waveform['time'],waveform['current_ohm']*1.e-6,label=r'$J_{OHM}$')
        ax.plot(waveform["time"], abs(waveform["b0"]), plotstyle, label=r"$|B_0|$")
        ax.set_ylabel(r"$I_p\/[\mathrm{MA}], B_0\/[\mathrm{T}]$", fontdict={"color": "darkred"})
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    def view_energy_content_waveforms(self, ax):
        """
        The function `view_energy_content_waveforms` plots energy content waveforms on a given axis.

        Args:
            ax: The parameter "ax" is an instance of the matplotlib Axes class. It represents the axes on which the
                waveforms will be plotted.
        """
        waveform = self.compute_obj.get_summary()
        plotstyle = "-" if len(waveform["time"]) > 1 else "o"
        ax.plot(
            waveform["time"],
            waveform["energy_total"] * 1.0e-6,
            plotstyle,
            label=r"$W_{TOT}$",
        )
        ax.plot(
            waveform["time"],
            waveform["energy_diamagnetic"] * 1.0e-6,
            plotstyle,
            label=r"$W_{DIA}$",
        )
        ax.plot(
            waveform["time"],
            waveform["energy_thermal"] * 1.0e-6,
            plotstyle,
            label=r"$W_{TH}$",
        )
        ax.plot(
            waveform["time"],
            waveform["energy_mhd"] * 1.0e-6,
            plotstyle,
            label=r"$W_{MHD}$",
        )

        ax.set_xlim(self.ids.time[0], self.ids.time[-1])
        ax.set_ylabel(r"$W\/[\mathrm{MJ}]$", fontdict={"color": "darkred"})
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    def view_vloop_waveforms(self, ax):
        """
        The function `view_vloop_waveforms` plots three waveforms (`V_LOOP`, `H_98`, and `TAU_ENERGY`)  against time
        on the given `ax` object.

        Args:
            ax: The parameter "ax" is an instance of the matplotlib Axes class. It represents the axes on which
                the waveforms will be plotted.
        """
        waveform = self.compute_obj.get_summary()
        plotstyle = "-" if len(waveform["time"]) > 1 else "o"
        ax.plot(waveform["time"], waveform["v_loop"], plotstyle, label=r"$V_{LOOP}$")
        ax.plot(waveform["time"], waveform["h_98"], plotstyle, label=r"$H_{98}$")
        ax.plot(waveform["time"], waveform["tau_energy"], plotstyle, label=r"$\tau_{E}$")
        ax.set_xlabel(r"$Time\/[\mathrm{s}]$", fontdict={"color": "darkred"})
        ax.set_ylabel(r"$V\/[\mathrm{V}],\/H,\/\tau\/[\mathrm{s}]$", fontdict={"color": "darkred"})
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    def show_info_on_plot(self, ax, info: str = "", location="right"):
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        if location == "top":
            ax.text(
                xmin,
                ymax + 0.5,
                info,
                horizontalalignment="left",
                rotation="horizontal",
                fontsize=6,
            )
        else:
            ax.text(
                xmax + 0.01 * abs(xmax),
                ymin + 0.01 * abs(ymax - ymin),
                info,
                horizontalalignment="left",
                verticalalignment="center",
                rotation="vertical",
                fontsize=6,
            )

    def view_time_line(self, ax, time):
        """
        The function `view_time_line` plots a vertical dashed line on a given matplotlib axis at a specified time.

        Args:
            ax: The parameter "ax" is a reference to the second y-axis of a matplotlib figure. It is used to plot
                the timeline on the same figure as the other data.
            time: The "time" parameter is the value at which you want to plot a vertical line on the timeline. It
                represents the specific point in time that you want to highlight on the timeline.
        """
        ymin, ymax = ax.get_ylim()
        ax.plot(
            [time, time],
            [ymin, ymax],
            color="gray",
            linestyle="--",
            label=r"$t_{slice}$",
        )
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        ax.set_ylim(ymin, ymax)

    def view_hmode(self, ax):
        """
        The function `view_hmode` checks if HMode is present and fills the area between `th_min` and `th_max` on the
        y-axis with a light yellow color if it is, otherwise it logs a warning message.

        Args:
            ax: The parameter `ax` is an instance of the `Axes` class from the `matplotlib` library. It represents
                the axes on which the plot is being drawn.
        """
        ymin, ymax = ax.get_ylim()

        h_mode_dict = self.compute_obj.get_h_mode_info()
        h_mode_present, th_min, th_max = (
            h_mode_dict["h_mode_present"],
            h_mode_dict["th_min"],
            h_mode_dict["th_max"],
        )
        if h_mode_present:
            ax.fill(
                [th_min, th_max, th_max, th_min],
                [ymin, ymin, ymax, ymax],
                "lightyellow",
                edgecolor="k",
                linewidth=0.08,
                label=r"$H_{mode}$",
            )
            ax.set_ylim(ymin, ymax)
        else:
            logger.warning("HMode is not present")
