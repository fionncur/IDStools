"""
This module provides view functions and classes for spectrometer_visible ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

import matplotlib.pyplot as plt

from idstools.compute.spectrometer_visible import SpectrometerVisibleCompute

logger = logging.getLogger("module")

LABEL_RADIANCE = "Spectral Radiance (ph s^-1 m^-2 sr^-1 nm^-1)"
LABEL_INTENSITY = "Intensity (counts)"


class SpectrometerVisibleView:
    """This class provides view functions for spectrometer_visible ids"""

    def __init__(self, ids_obj: object):
        """Initialization SpectrometerVisibleView object.

        Args:
            ids_obj : spectrometer_visible ids object
        """
        self.ids_obj = ids_obj
        self.compute_obj = SpectrometerVisibleCompute(ids_obj)

    def view_radiance(self, ax: plt.axes, spectro_index, logscale=False):
        """
        The function `view_radiance` plots radiance data from multiple spectrometers on separate axes.

        Args:
            ax (List[plt.axes]): The parameter `ax` is a list of `plt.axes` objects. These objects represent the
                axes on which the radiance data will be plotted. The function `viewRadiance` takes these axes as input
                and plots the radiance data on each of them.
            spectro_index: The `spectro_index` parameter represents the index of the spectrometer for which the
                intensity spectra will be plotted. It is used to select the appropriate channels from the spectrometers.

        Returns:
            the value of the variable "filename".
        """
        filename = ""
        spectros = self.compute_obj.get_channels()
        channels = spectros[int(spectro_index)]

        for _, channelinfo in channels.items():
            ax.plot(
                channelinfo["wavelengths"],
                channelinfo["radiance_spectral"],
                label=f"CH#{channelinfo['identifier']:0>2g} R {channelinfo['radius']:0>0.2f} m",
            )
            filename = "_".join(
                [
                    channelinfo["diagnostic"].replace(".", "_"),
                    f"{channelinfo['min_wavelength']:0.2f}",
                    f"{channelinfo['max_wavelength']:0.2f}",
                ]
            )
        if logscale is False:
            ax.set_ylim(bottom=0.0)

        ax.set_title(f"{channelinfo['diagnostic']}, Spectrum {spectro_index}")
        if logscale:
            ax.set_yscale("log")
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

    def view_intensity(self, ax: plt.axes, spectro_index, logscale=False):
        """
        The `view_intensity` function plots intensity of spectrom from multiple spectrometers.

        Args:
            ax (List[plt.axes]): The parameter `ax` is a list of `plt.axes` objects. These objects represent the
                axes on which the intensity spectra will be plotted. The function `view_intensity` takes these axes
                as input and plots the intensity spectra on them.
            spectro_index: The `spectroIndex` parameter represents the index of the spectrometer for which the
                intensity spectra will be plotted. It is used to select the appropriate channels from the spectrometers.

        Returns:
            a string variable named "filename".
        """
        filename = ""
        spectros = self.compute_obj.get_channels()
        channels = spectros[int(spectro_index)]
        for _, channelinfo in channels.items():
            ax.plot(
                channelinfo["wavelengths"],
                channelinfo["intensity_spectrum"] * channelinfo["exposure_time"],
                label=f"CH#{channelinfo['identifier']:0>2g} R {channelinfo['radius']:0>0.2f} m",
            )
            filename = "_".join(
                [
                    channelinfo["diagnostic"].replace(".", "_"),
                    f"{channelinfo['min_wavelength']:0.2f}",
                    f"{channelinfo['max_wavelength']:0.2f}",
                ]
            )
        if logscale is False:
            ax.set_ylim(bottom=0.0)

        if logscale:
            ax.set_yscale("log")
        ax.set_title(f"{channelinfo['diagnostic']}, Spectrum {spectro_index}")

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
