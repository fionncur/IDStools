""" 
This module provides view functions and classes for spectrometer_visible ids data

`more about pf_active ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/spectrometer_visible.html>`_

"""
import logging
from typing import List

import matplotlib.pyplot as plt

from idstools.compute.spectrometer_visible import SpectrometerVisibleCompute

logger = logging.getLogger("module")

LABEL_RADIANCE = "Spectral Radiance (ph s^-1 m^-2 sr^-1 nm^-1)"
LABEL_INTENSITY = "Intensity (counts)"


class SpectrometerVisibleView:
    """This class provides view functions for spectrometer_visible ids"""

    def __init__(self, idsObj: object):
        """Initialization SpectrometerVisibleView object.

        Args:
            idsObj : spectrometer_visible ids object
        """
        self.idsObj = idsObj
        self.computeObj = SpectrometerVisibleCompute(idsObj)

    def viewRadiance(self, ax: List[plt.axes]):
        """
        The function `viewRadiance` plots radiance data from multiple spectrometers on separate axes.

        Args:
            ax (List[plt.axes]): The parameter `ax` is a list of `plt.axes` objects. These objects represent the axes on which the radiance data will be plotted. The function `viewRadiance` takes these axes as input and plots the radiance data on each of them.

        Returns:
            the value of the variable "filename".
        """
        filename = ""
        spectros = self.computeObj.getChannels()
        spectrosCounter = len(spectros) - 1
        if len(ax) < spectrosCounter:
            logger.warning(
                "There are {spectrosCounter} valid spectrometers available, Please provide axes to plot rest of the spectrometers data"
            )
        for sIndex, channels in spectros.items():
            if spectrosCounter < len(ax):
                singleax = ax[spectrosCounter]
                spectrosCounter = spectrosCounter - 1
            for _, channelinfo in channels.items():
                singleax.plot(
                    channelinfo["wavelengths"],
                    channelinfo["radiance_spectral"],
                    linewidth=1.0,
                    label=f"CH#{channelinfo['identifier']:0>2g} R {channelinfo['radius']:0>0.2f} m",
                )
            singleax.set_ylim(bottom=0.0)

            singleax.set_title(
                "\n".join((channelinfo["diagnostic"], f"Spectrum {sIndex}"))
            )
            singleax.set_xlabel("Wavelength (nm)")
            singleax.set_ylabel(LABEL_RADIANCE)
            singleax.grid(True)

            singleax.legend(
                bbox_to_anchor=(1.0, 0.5),
                loc="center left",
                borderaxespad=0.0,
                frameon=False,
                fontsize="x-small",
            )

        return filename

    def viewIntensity(self, ax: List[plt.axes]):
        """
        The `viewIntensity` function plots intensity of spectrom from multiple spectrometers.

        Args:
            ax (List[plt.axes]): The parameter `ax` is a list of `plt.axes` objects. These objects represent the axes on which the intensity spectra will be plotted. The function `viewIntensity` takes these axes as input and plots the intensity spectra on them.

        Returns:
            a string variable named "filename".
        """
        filename = ""
        spectros = self.computeObj.getChannels()
        spectrosCounter = len(spectros) - 1
        if len(ax) < spectrosCounter:
            logger.warning(
                "There are {spectrosCounter} valid spectrometers available, Please provide axes to plot rest of the spectrometers data"
            )
        for sIndex, channels in spectros.items():
            if spectrosCounter < len(ax):
                singleax = ax[spectrosCounter]
                spectrosCounter = spectrosCounter - 1
            for _, channelinfo in channels.items():
                singleax.plot(
                    channelinfo["wavelengths"],
                    channelinfo["intensity_spectrum"] * channelinfo["exposure_time"],
                    linewidth=1.0,
                    label=f"CH#{channelinfo['identifier']:0>2g} R {channelinfo['radius']:0>0.2f} m",
                )
                filename = "_".join(
                    [
                        channelinfo["diagnostic"].replace(".", "_"),
                        f"{channelinfo['min_wavelength']:0.2f}",
                        f"{channelinfo['max_wavelength']:0.2f}",
                    ]
                )
            singleax.set_ylim(bottom=0.0)

            singleax.set_title(
                "\n".join((channelinfo["diagnostic"], f"Spectrum {sIndex}"))
            )
            singleax.set_xlabel("Wavelength (nm)")
            singleax.set_ylabel(LABEL_RADIANCE)
            singleax.grid(True)

            singleax.legend(
                bbox_to_anchor=(1.0, 0.5),
                loc="center left",
                borderaxespad=0.0,
                frameon=False,
                fontsize="x-small",
            )

        return filename
