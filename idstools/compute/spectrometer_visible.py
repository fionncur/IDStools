import numpy as np
from typing import Union

class SpectrometerVisibleCompute:
    def __init__(self, ids_object):
        self.ids_object = ids_object

    def get_vessel(
        self, iunit: int = 0, add_endpoint: bool = False
    ) -> Union[dict, None]:
        # Deduce the number of spectra from the channel name (not safe but no other method yet)
list_of_spectra = []
for channel in ids.channel:
    if len(channel.name.split("Spectrum ")) > 1:
        spectrum_index = channel.name.split("Spectrum ")[1]
    else:
        spectrum_index = 1
    if spectrum_index not in list_of_spectra:
        list_of_spectra.append(spectrum_index)
n_spectra = len(list_of_spectra)

for n in range(n_spectra):
    wavelengths: np.ndarray = None
    diagnostic: str = None
    min_wavelength: float = None
    max_wavelength: float = None

    figure_radiance, axes_radiance = plt.subplots(tight_layout=True)
    figure_intensity, axes_intensity = plt.subplots(tight_layout=True)

    for channel in ids.channel:
        match = CHANNEL_NAME_PATTERN.fullmatch(channel.name)

        if match is None:
            logger.error(
                f"Channel's name {channel.name} does not math pattern "
                f"{CHANNEL_NAME_PATTERN.pattern}"
            )
            raise ValueError()

        if diagnostic is None:
            diagnostic = match[1]

        identifier = int(match[2])
        spectrum_n = int(match[3])

        if spectrum_n != n + 1:
            continue

        gs = channel.grating_spectrometer
        if not gs.wavelengths.size:
            logger.warning(f"{channel.name} grating_spectrometer.wavelengths is empty.")
            continue

        if wavelengths is None:
            wavelengths = gs.wavelengths * 1e9
            delta = (wavelengths[1] - wavelengths[0]) / 2.0
            min_wavelength = wavelengths[0] - delta
            max_wavelength = wavelengths[-1] + delta

        if not gs.radiance_spectral.data.size:
            logging.warning(
                f"{channel.name} grating_spectrometer.radiance_spectral.data is empty."
            )
            continue
        radiance_spectral = gs.radiance_spectral.data[:, 0] * 1e-9

        if not gs.intensity_spectrum.data.size:
            logging.warning(
                f"{channel.name} grating_spectrometer.intensity_spectrum.data is empty."
            )
            continue
        intensity_spectrum = gs.intensity_spectrum.data[:, 0]

        if not gs.exposure_time:
            logging.warning(
                f"{channel.name} grating_spectrometer.exposure_time is empty."
            )
            continue
        exposure_time = gs.exposure_time

        radius = channel.line_of_sight.second_point.r