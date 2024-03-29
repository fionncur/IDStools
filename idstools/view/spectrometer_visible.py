""" 
This module provides view functions and classes for spectrometer_visible ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

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

    def viewRadiance(self, ax: plt.axes, spectroIndex):
        """
        The function `viewRadiance` plots radiance data from multiple spectrometers on separate axes.

        Args:
            ax (List[plt.axes]): The parameter `ax` is a list of `plt.axes` objects. These objects represent the axes on which the radiance data will be plotted. The function `viewRadiance` takes these axes as input and plots the radiance data on each of them.
            spectroIndex: The `spectroIndex` parameter represents the index of the spectrometer for which the intensity spectra will be plotted. It is used to select the appropriate channels from the spectrometers.
            title: The `title` parameter is a string that represents the title of the plot.

        Returns:
            the value of the variable "filename".
        """
        filename = ""
        spectros = self.computeObj.getChannels()
        channels = spectros[int(spectroIndex)]

        for _, channelinfo in channels.items():
            ax.plot(
                channelinfo["wavelengths"],
                channelinfo["radiance_spectral"],
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
        ax.set_ylim(bottom=0.0)

        ax.set_title(f"{channelinfo['diagnostic']}, Spectrum {spectroIndex}")

        ax.set_xlabel("Wavelength (nm)")
        ax.set_ylabel(LABEL_RADIANCE)
        ax.grid(True)

        ax.legend(
            bbox_to_anchor=(1.0, 0.5),
            loc="center left",
            borderaxespad=0.0,
            frameon=False,
            fontsize="x-small",
        )

        return filename

    def viewIntensity(self, ax: plt.axes, spectroIndex):
        """
        The `viewIntensity` function plots intensity of spectrom from multiple spectrometers.

        Args:
            ax (List[plt.axes]): The parameter `ax` is a list of `plt.axes` objects. These objects represent the axes on which the intensity spectra will be plotted. The function `viewIntensity` takes these axes as input and plots the intensity spectra on them.
            spectroIndex: The `spectroIndex` parameter represents the index of the spectrometer for which the intensity spectra will be plotted. It is used to select the appropriate channels from the spectrometers.
            title: The `title` parameter is a string that represents the title of the plot.

        Returns:
            a string variable named "filename".
        """
        filename = ""
        spectros = self.computeObj.getChannels()
        channels = spectros[int(spectroIndex)]
        for _, channelinfo in channels.items():
            ax.plot(
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
        ax.set_ylim(bottom=0.0)

        ax.set_title(f"{channelinfo['diagnostic']}, Spectrum {spectroIndex}")

        ax.set_xlabel("Wavelength (nm)")
        ax.set_ylabel(LABEL_RADIANCE)

        ax.legend(
            bbox_to_anchor=(1.0, 0.5),
            loc="center left",
            borderaxespad=0.0,
            frameon=False,
            fontsize="x-small",
        )

        return filename
