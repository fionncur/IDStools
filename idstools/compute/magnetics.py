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
        """Initialization MagneticsCompute object.

        Args:
            ids : magnetics ids object
        """
        self.ids = ids

    def get_b_field_probe_values(self, probe_type="b_field_pol_probe"):
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
        if hasattr(self.ids, probe_type):
            for probe_index, probe in enumerate(self.ids[probe_type]):
                probe_info = {}
                probe_info["name"] = probe.name
                if hasattr(probe, "identifier") and probe.identifier:
                    probe_info["name"] = probe.identifier
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
                    logger.warning(f"Probe index {probe_index} : {probe_type} is empty")
                probes.append(probe_info)
        if len(probes) == 0:
            logger.warning(f"{probe_type} are empty")
            return None
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
            if hasattr(flux_loop, "identifier") and flux_loop.identifier:
                flux_loop_info["name"] = flux_loop.identifier
            flux_loop_info["r"] = [x.r.value for x in flux_loop.position]
            flux_loop_info["z"] = [x.z.value for x in flux_loop.position]
            flux_loop_info["phi"] = [x.phi.value for x in flux_loop.position]

            flux_loop_info["flux"] = {"data": flux_loop.flux.data, "time": flux_loop.flux.time}
            flux_loop_info["voltage"] = {"data": flux_loop.voltage.data, "time": flux_loop.voltage.time}
            flux_loop_info["area"] = flux_loop.area

            if not flux_loop_info:
                logger.warning(f"flux_loop index {iflux_loop} : flux_loop is empty")
            flux_loops.append(flux_loop_info)
        if len(flux_loops) == 0:
            logger.warning("flux_loops are empty")
            return None
        return flux_loops

    def get_rogowski_coil_values(self):
        """
        Retrieves the values of Rogowski coils from the IDS.

        This method iterates through the Rogowski coils available in the IDS and extracts
        relevant information such as name, position (r, z, phi), current data, and area.
        The extracted information is stored in a list of dictionaries, each representing
        a Rogowski coil.

        Returns:
            list: A list of dictionaries, each containing the following keys:
                - "name" (str): The name or identifier of the Rogowski coil.
                - "r" (list): A list of radial positions of the Rogowski coil.
                - "z" (list): A list of vertical positions of the Rogowski coil.
                - "phi" (list): A list of angular positions of the Rogowski coil.
                - "current" (dict): A dictionary containing:
                    - "data" (list): The current data of the Rogowski coil.
                    - "time" (list): The time points corresponding to the current data.
                - "area" (float): The area of the Rogowski coil.

        Raises:
            AttributeError: If the IDS object does not have the expected attributes.
        """

        rogowski_coils = []
        for index, rogowski_coil in enumerate(self.ids.rogowski_coil):
            rogowski_coil_info = {}
            rogowski_coil_info["name"] = rogowski_coil.name
            if hasattr(rogowski_coil, "identifier") and rogowski_coil.identifier:
                rogowski_coil_info["name"] = rogowski_coil.identifier
            rogowski_coil_info["r"] = [x.r.value for x in rogowski_coil.position]
            rogowski_coil_info["z"] = [x.z.value for x in rogowski_coil.position]
            rogowski_coil_info["phi"] = [x.phi.value for x in rogowski_coil.position]

            rogowski_coil_info["current"] = {"data": rogowski_coil.current.data, "time": rogowski_coil.current.time}
            rogowski_coil_info["area"] = rogowski_coil.area

            if not rogowski_coil_info:
                logger.warning(f"rogowski_coil index {index} : rogowski_coil is empty")
            rogowski_coils.append(rogowski_coil_info)
        if len(rogowski_coils) == 0:
            logger.warning("rogowski_coils are empty")
            return None
        return rogowski_coils

    def get_shunt_values(self):
        """
        Retrieves shunt information from the IDS object and returns it as a list of dictionaries.

        Each dictionary contains the following keys:
            - "name": The name or identifier of the shunt.
            - "r1": List of radial positions (r) of the first point of the shunt.
            - "z1": List of vertical positions (z) of the first point of the shunt.
            - "r2": List of radial positions (r) of the second point of the shunt.
            - "z2": List of vertical positions (z) of the second point of the shunt.
            - "voltage": A dictionary with keys "data" and "time" representing the voltage
            data and corresponding time points.
            - "resistance": The resistance value of the shunt.

        If a shunt dictionary is empty, a warning is logged with the index of the shunt.

        Returns:
            list: A list of dictionaries containing shunt information.
        """
        shunts = []
        for index, _shunt in enumerate(self.ids.shunt):
            shunt_info = {}
            shunt_info["name"] = _shunt.name
            if hasattr(_shunt, "identifier") and _shunt.identifier:
                shunt_info["name"] = _shunt.identifier
            shunt_info["r1"] = [x.r.value for x in _shunt.position.first_point]
            shunt_info["z1"] = [x.z.value for x in _shunt.position.first_point]
            shunt_info["r2"] = [x.r.value for x in _shunt.position.second_point]
            shunt_info["z2"] = [x.z.value for x in _shunt.position.second_point]
            shunt_info["voltage"] = {"data": _shunt.voltage.data, "time": _shunt.voltage.time}
            shunt_info["resistance"] = _shunt.resistance

            if not shunt_info:
                logger.warning(f"shunt index {index} : shunt is empty")
            shunts.append(shunt_info)
        if len(shunts) == 0:
            logger.warning("shunts are empty")
            return None
        return shunts

    def get_b_field_probes(self, probe_type="b_field_pol_probe"):
        """
        Retrieve probe information and organize it into a dictionary.

        This method calls `get_probes_values` to get a list of probe data, then
        extracts relevant information and stores it in a dictionary with the
        following keys:
            - "r": numpy array of radial positions of the probes.
            - "z": numpy array of vertical positions of the probes.
            - "poloidal_angle": numpy array of poloidal angles of the probes.
            - "toroidal_angle": numpy array of toroidal angles of the probes.
            - "area": numpy array of areas of the probes.
            - "names": list of names of the probes.

        Returns:
            dict: A dictionary containing probe information.
        """
        probes = self.get_b_field_probe_values(probe_type)
        if probes is None:
            return None
        probe_dict = {
            "r": np.array([p["r"] for p in probes]),
            "z": np.array([p["z"] for p in probes]),
            "poloidal_angle": np.array([p["poloidal_angle"] for p in probes]),
            "toroidal_angle": np.array([p["toroidal_angle"] for p in probes]),
            "area": np.array([p["area"] for p in probes]),
            "names": [p["name"] for p in probes],
            "lengths": [p["length"] for p in probes],
        }
        return probe_dict

    def get_flux_loops(self):
        """
        Retrieves flux loop data and organizes it into a dictionary.

        This method calls `get_fluxloop_values` to obtain a list of flux loop
        measurements, and then processes this list to create a dictionary
        containing the following keys:
            - "r": A numpy array of the radial positions of the flux loops.
            - "z": A numpy array of the vertical positions of the flux loops.
            - "area": A numpy array of the areas of the flux loops.
            - "names": A list of the names of the flux loops.

        Returns:
            dict: A dictionary containing the processed flux loop data.
        """
        flux_loops = self.get_fluxloop_values()
        if flux_loops is None:
            return None
        flux_loops_dict = {
            "r": np.array([p["r"] for p in flux_loops]),
            "z": np.array([p["z"] for p in flux_loops]),
            "area": np.array([p["area"] for p in flux_loops]),
            "names": [p["name"] for p in flux_loops],
        }
        return flux_loops_dict

    def get_rogowski_coils(self):
        """
        Retrieve Rogowski coil data and organize it into a dictionary.

        This method fetches the Rogowski coil values and structures them into a dictionary
        with keys 'r', 'z', 'phi', 'area', and 'names'. Each key corresponds to a numpy array
        or list containing the respective values for each Rogowski coil.

        Returns:
            dict: A dictionary containing the Rogowski coil data with the following keys:
                - 'r' (numpy.ndarray): Radial positions of the Rogowski coils.
                - 'z' (numpy.ndarray): Axial positions of the Rogowski coils.
                - 'phi' (numpy.ndarray): Azimuthal angles of the Rogowski coils.
                - 'area' (numpy.ndarray): Areas of the Rogowski coils.
                - 'names' (list): Names of the Rogowski coils.
        """
        rogowski_coil_data = self.get_rogowski_coil_values()
        if rogowski_coil_data is None:
            return None
        rogowski_coils_dict = {
            "r": np.array([p["r"] for p in rogowski_coil_data]),
            "z": np.array([p["z"] for p in rogowski_coil_data]),
            "phi": np.array([p["phi"] for p in rogowski_coil_data]),
            "area": np.array([p["area"] for p in rogowski_coil_data]),
            "names": [p["name"] for p in rogowski_coil_data],
        }
        return rogowski_coils_dict

    def get_shunts(self):
        """
        Retrieves shunt data and organizes it into a dictionary.

        This method calls `get_shunt_values` to obtain shunt data, then processes
        this data into a dictionary with the following keys:
            - "r1": numpy array of r1 values
            - "z1": numpy array of z1 values
            - "r2": numpy array of r2 values
            - "z2": numpy array of z2 values
            - "resitance": numpy array of resistance values
            - "names": list of shunt names

        Returns:
            dict: A dictionary containing shunt data arrays and names.
        """
        shunt_data = self.get_shunt_values()
        if shunt_data is None:
            return None
        shunt_dict = {
            "r1": np.array([p["r1"] for p in shunt_data]),
            "z1": np.array([p["z1"] for p in shunt_data]),
            "r2": np.array([p["r2"] for p in shunt_data]),
            "z2": np.array([p["z2"] for p in shunt_data]),
            "resitance": np.array([p["resitance"] for p in shunt_data]),
            "names": [p["name"] for p in shunt_data],
        }
        return shunt_dict
