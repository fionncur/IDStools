import logging
import re

logger = logging.getLogger("module")


LABEL_RADIANCE = "Spectral Radiance (ph s^-1 m^-2 sr^-1 nm^-1)"
LABEL_INTENSITY = "Intensity (counts)"
CHANNEL_NAME_PATTERN = r"^(\d{2}\.\w{2}) CH#(\d{2}) Spectrum (\d{1})$"


class SpectrometerVisibleCompute:
    def __init__(self, ids_object):
        self.ids_object = ids_object

    def get_valid_spectrometers(self):
        """
        The function `get_valid_spectrometers` returns a list of valid spectrometers by extracting
        the names from the `channel` objects.

        Returns:
            a list of valid spectrometers.
        """
        spectrometers = []
        for channel in self.ids_object.channel:
            if len(channel.name.split("Spectrum ")) > 1:
                spectrometers.append(channel.name.split("Spectrum ")[1])
            else:
                spectrometers.append(1)
        return list(set(spectrometers))

    def get_channels(self, channel_name_pattern=CHANNEL_NAME_PATTERN):
        """
        The `get_channels` function retrieves information about channels based on a given channel name pattern.

        Args:
            channel_name_pattern: The `channel_name_pattern` parameter is a regular expression pattern used to
                match the names of channels. It is used to filter out channels whose names do not match th
                specified pattern.

        Returns:
            a dictionary called "channels".
        """
        channels = {}
        for channel in self.ids_object.channel:
            channel_info = {}
            match = re.compile(channel_name_pattern).fullmatch(channel.name.value)

            if match is None:
                logger.warning(
                    f"Channel's name {channel.name.value} does not math pattern {channel_name_pattern.pattern}"
                )
                continue

            diagnostic = match[1]

            identifier = int(match[2])
            spectrum_n = int(match[3])
            gs = channel.grating_spectrometer
            if not gs.wavelengths.size:
                logger.warning(f"{channel.name} grating_spectrometer.wavelengths is empty.")
                continue

            wavelengths = gs.wavelengths * 1e9
            delta = (wavelengths[1] - wavelengths[0]) / 2.0
            min_wavelength = wavelengths[0] - delta
            max_wavelength = wavelengths[-1] + delta

            if not gs.radiance_spectral.data.size:
                logging.warning(f"{channel.name} grating_spectrometer.radiance_spectral.data is empty.")
                radiance_spectral = None
            else:
                radiance_spectral = gs.radiance_spectral.data[:, 0] * 1e-9

            if not gs.intensity_spectrum.data.size:
                logging.warning(f"{channel.name} grating_spectrometer.intensity_spectrum.data is empty.")
                intensity_spectrum = None
            else:
                intensity_spectrum = gs.intensity_spectrum.data[:, 0]

            if not gs.exposure_time.value:
                logging.warning(f"{channel.name} grating_spectrometer.exposure_time is empty.")
                exposure_time = None
            else:
                exposure_time = gs.exposure_time.value

            radius = channel.line_of_sight.second_point.r.value

            channel_info["channel_name"] = channel.name.value
            channel_info["diagnostic"] = diagnostic
            channel_info["identifier"] = identifier
            channel_info["spectrum_n"] = spectrum_n

            channel_info["wavelengths"] = wavelengths
            channel_info["delta"] = delta
            channel_info["min_wavelength"] = min_wavelength
            channel_info["max_wavelength"] = max_wavelength
            channel_info["radiance_spectral"] = radiance_spectral

            channel_info["intensity_spectrum"] = intensity_spectrum
            channel_info["exposure_time"] = exposure_time
            channel_info["radius"] = radius

            if spectrum_n not in channels.keys():
                channels[spectrum_n] = {}
            channels[spectrum_n][identifier] = channel_info

        return channels
