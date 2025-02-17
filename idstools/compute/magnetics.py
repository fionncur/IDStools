"""
This module provides compute functions and classes for magnetics ids data

`refer data dictionary <https://imas-data-dictionary.readthedocs.io/en/latest/generated/ids/magnetics.html>`_.

"""

import logging

import numpy as np

logger = logging.getLogger("module")


class MagneticsCompute:
    """This class provides compute functions for magnetics ids"""

    def __init__(self, ids: object):
        """Initialization PfActiveCompute object.

        Args:
            ids : magnetics ids object
        """
        self.ids = ids

    def get_probes_values(self):
        """
        Retrieve values of magnetic probes from the IDS object.

        This method iterates over the `b_field_pol_probe` attribute of the IDS object,
        extracting relevant information for each probe and storing it in a dictionary.
        The dictionaries are then collected into a list which is returned.

        Returns:
            list: A list of dictionaries, each containing information about a magnetic probe.
                  Each dictionary contains the following keys:
                  - "name": The name of the probe.
                  - "type": The type of the probe.
                  - "r": The radial position of the probe.
                  - "z": The vertical position of the probe.
                  - "phi": The toroidal angle of the probe.
                  - "poloidal_angle": The poloidal angle of the probe.
                  - "toroidal_angle": The toroidal angle of the probe.
                  - "area": The area of the probe.
                  - "length": The length of the probe.
                  - "turns": The number of turns of the probe.

        Logs:
            If a probe's information is empty, a warning is logged with the probe index.
        """
        probes = []
        for probe_index, probe in enumerate(self.ids.b_field_pol_probe):
            probe_info = {}
            probe_info["name"] = probe.name
            probe_info["type"] = probe.type
            probe_info["r"] = probe.position.r
            probe_info["z"] = probe.position.z
            probe_info["phi"] = probe.position.phi
            probe_info["poloidal_angle"] = probe.poloidal_angle
            probe_info["toroidal_angle"] = probe.toroidal_angle
            probe_info["area"] = probe.area
            probe_info["length"] = probe.length
            probe_info["turns"] = probe.turns
            if not probe_info:
                logger.warning(f"Probe index {probe_index} : b_field_pol_probe is empty")
            probes.append(probe_info)
        return probes

    def get_fluxloop_values(self):
        """
        Retrieve flux loop values from the IDS (Integrated Data Structure).

        This method iterates over the flux loops in the IDS and extracts relevant information
        such as name, position (r, z, phi), flux data, voltage data, and area. The extracted
        information is stored in a list of dictionaries, where each dictionary corresponds to
        a flux loop.

        Returns:
            list: A list of dictionaries, each containing the following keys:
                - "name" (str): The name of the flux loop.
                - "r" (list): A list of radial positions.
                - "z" (list): A list of vertical positions.
                - "phi" (list): A list of toroidal angles.
                - "flux" (dict): A dictionary with keys "data" (flux data) and "time" (time points).
                - "voltage" (dict): A dictionary with keys "data" (voltage data) and "time" (time points).
                - "area" (float): The area of the flux loop.

        Logs:
            A warning is logged if a flux loop is found to be empty.

        Example:
            flux_loops = get_fluxloop_values()
        """
        flux_loops = []
        for iflux_loop, flux_loop in enumerate(self.ids.flux_loop):
            flux_loop_info = {}
            flux_loop_info["name"] = flux_loop.name
            flux_loop_info["r"] = [x.r.value for x in flux_loop.position]
            flux_loop_info["z"] = [x.z.value for x in flux_loop.position]
            flux_loop_info["phi"] = [x.phi.value for x in flux_loop.position]

            flux_loop_info["flux"] = {"data": flux_loop.flux.data, "time": flux_loop.flux.time}
            flux_loop_info["voltage"] = {"data": flux_loop.voltage.data, "time": flux_loop.voltage.time}
            flux_loop_info["area"] = flux_loop.area

            if not flux_loop_info:
                logger.warning(f"flux_loop index {iflux_loop} : flux_loop is empty")
            flux_loops.append(flux_loop_info)
        return flux_loops

    def get_probes(self):
        """
        Retrieve probe information and organize it into a dictionary.

        This method calls `get_probes_values` to get a list of probe data, then
        extracts relevant information and stores it in a dictionary with the
        following keys:
            - "R": numpy array of radial positions of the probes.
            - "Z": numpy array of vertical positions of the probes.
            - "Poloidal_Angle": numpy array of poloidal angles of the probes.
            - "toroidal_angle": numpy array of toroidal angles of the probes.
            - "Area": numpy array of areas of the probes.
            - "Names": list of names of the probes.

        Returns:
            dict: A dictionary containing probe information.
        """
        probes = self.get_probes_values()
        probe_dict = {
            "R": np.array([p["r"] for p in probes]),
            "Z": np.array([p["z"] for p in probes]),
            "Poloidal_Angle": np.array([p["poloidal_angle"] for p in probes]),
            "toroidal_angle": np.array([p["toroidal_angle"] for p in probes]),
            "Area": np.array([p["area"] for p in probes]),
            "Names": [p["name"] for p in probes],
        }
        return probe_dict

    def get_flux_loops(self):
        """
        Retrieves flux loop data and organizes it into a dictionary.

        This method calls `get_fluxloop_values` to obtain a list of flux loop
        measurements, and then processes this list to create a dictionary
        containing the following keys:
            - "R": A numpy array of the radial positions of the flux loops.
            - "Z": A numpy array of the vertical positions of the flux loops.
            - "Area": A numpy array of the areas of the flux loops.
            - "Names": A list of the names of the flux loops.

        Returns:
            dict: A dictionary containing the processed flux loop data.
        """
        flux_loops = self.get_fluxloop_values()
        flux_loops_dict = {
            "R": np.array([p["r"] for p in flux_loops]),
            "Z": np.array([p["z"] for p in flux_loops]),
            "Area": np.array([p["area"] for p in flux_loops]),
            "Names": [p["name"] for p in flux_loops],
        }

        return flux_loops_dict
