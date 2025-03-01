"""
This module provides compute functions and classes for magnetics ids data

`refer data dictionary <https://imas-data-dictionary.readthedocs.io/en/latest/generated/ids/magnetics.html>`_.

"""

import logging

import numpy as np

from idstools.utils.utility_functions import get_slice_from_array

logger = logging.getLogger("module")


class MagneticsCompute:
    """This class provides compute functions for magnetics ids"""

    def __init__(self, ids: object):
        """Initialization MagneticsCompute object.

        Args:
            ids : magnetics ids object
        """
        self.ids = ids

    def get_b_field_probe_values(self, probe_type="b_field_pol_probe", select=":"):
        """
        Retrieve B-field probe values from the IDS object.

        Parameters:
        -----------
        probe_type : str, optional
            The type of probe to retrieve values for. Default is "b_field_pol_probe".
        select : str, optional
            A selection string to filter the probes. Default is ":".

        Returns:
        --------
        list of dict or None
            A list of dictionaries containing probe information, or None if no probes are found.

        Each dictionary in the list contains the following keys:
        - "name": str, the name or identifier of the probe.
        - "type": str, the type of the probe.
        - "r": float, the radial position of the probe.
        - "z": float, the vertical position of the probe.
        - "phi": float, the toroidal angle of the probe.
        - "poloidal_angle": float, the poloidal angle of the probe.
        - "toroidal_angle": float, the toroidal angle of the probe.
        - "area": float, the area of the probe.
        - "length": float, the length of the probe.
        - "turns": int, the number of turns of the probe.

        Notes:
        ------
        - If the specified probe type is not found in the IDS object, a warning is logged.
        - If no probes are found after filtering, a warning is logged and None is returned.
        """
        probes = []
        if hasattr(self.ids, probe_type):
            all_probes = list(self.ids[probe_type])
            if select is not None:
                all_probes = get_slice_from_array(all_probes, select)
            for probe_index, probe in enumerate(all_probes):
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

    def get_fluxloop_values(self, select=":"):
        """
        Retrieve flux loop values from the IDS (Integrated Data Structure).

        Parameters:
        select (str): A string to select a subset of the flux loop arrays. Default is ":" which selects all.

        Returns:
        list: A list of dictionaries containing flux loop information. Each dictionary includes:
            - "name" (str): The name or identifier of the flux loop.
            - "r" (list): List of radial positions.
            - "z" (list): List of vertical positions.
            - "phi" (list): List of toroidal positions.
            - "flux" (dict): Dictionary with "data" (flux data) and "time" (time data).
            - "voltage" (dict): Dictionary with "data" (voltage data) and "time" (time data).
            - "area" (float): The area of the flux loop.

        If no flux loops are found or if the flux loop information is empty, a warning is logged and None is returned.
        """
        flux_loop_arrays = list(self.ids.flux_loop)
        if select is not None:
            flux_loop_arrays = get_slice_from_array(flux_loop_arrays, select)

        flux_loops = []
        for iflux_loop, flux_loop in enumerate(flux_loop_arrays):
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

    def get_rogowski_coil_values(self, select=":"):
        """
        Retrieve values from Rogowski coils.

        This method extracts information from Rogowski coils stored in the IDS (Integrated Data Structure).
        It allows for optional selection of specific coils using a slice notation.

        Args:
            select (str, optional): A slice notation string to select specific Rogowski coils. Defaults to ":".

        Returns:
            list[dict] or None: A list of dictionaries containing Rogowski coil information. Each dictionary contains:
                - "name" (str): The name or identifier of the Rogowski coil.
                - "r" (list[float]): Radial positions of the coil.
                - "z" (list[float]): Axial positions of the coil.
                - "phi" (list[float]): Toroidal positions of the coil.
                - "current" (dict): A dictionary with "data" (list[float]) and "time" (list[float]) of the coil current.
                - "area" (float): The area of the Rogowski coil.
            Returns None if no Rogowski coils are found or if the selection is empty.

        Raises:
            AttributeError: If the IDS object does not have the expected attributes.
        """
        rogowski_coil_arrays = list(self.ids.rogowski_coil)
        if select is not None:
            rogowski_coil_arrays = get_slice_from_array(rogowski_coil_arrays, select)

        rogowski_coils = []
        for index, rogowski_coil in enumerate(rogowski_coil_arrays):
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

    def get_shunt_values(self, select=":"):
        """
        Retrieve shunt values from the IDS object and return them as a list of dictionaries.

        Parameters:
        select (str): A string representing the selection slice. Default is ":".

        Returns:
        list: A list of dictionaries containing shunt information. Each dictionary contains:
            - "name" (str): The name or identifier of the shunt.
            - "r1" (list): A list of radial positions for the first point.
            - "z1" (list): A list of vertical positions for the first point.
            - "r2" (list): A list of radial positions for the second point.
            - "z2" (list): A list of vertical positions for the second point.
            - "voltage" (dict): A dictionary containing voltage data and time.
            - "resistance" (float): The resistance of the shunt.

        If no shunts are found or if the shunts list is empty, a warning is logged and None is returned.
        """
        shunts_array = list(self.ids.shunt)
        if select is not None:
            shunts_array = get_slice_from_array(shunts_array, select)

        shunts = []
        for index, _shunt in enumerate(shunts_array):
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

    def get_b_field_probes(self, probe_type="b_field_pol_probe", select=":"):
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
        probes = self.get_b_field_probe_values(probe_type, select=select)
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

    def get_flux_loops(self, select=":"):
        """
        Retrieve flux loop data and organize it into a dictionary.

        Parameters:
        select (str): A selection string to filter the flux loop values. Default is ":".

        Returns:
        dict: A dictionary containing the flux loop data with keys:
            - "r": numpy array of radial positions.
            - "z": numpy array of vertical positions.
            - "area": numpy array of areas.
            - "names": list of names.
        None: If no flux loop data is found.
        """
        flux_loops = self.get_fluxloop_values(select=select)
        if flux_loops is None:
            return None
        flux_loops_dict = {
            "r": [p["r"] for p in flux_loops],
            "z": [p["z"] for p in flux_loops],
            "area": [p["area"] for p in flux_loops],
            "names": [p["name"] for p in flux_loops],
        }
        return flux_loops_dict

    def get_rogowski_coils(self, select=":"):
        """
        Retrieve Rogowski coil data and organize it into a dictionary.

        Parameters:
        select (str): A selection string to filter the Rogowski coil data. Default is ":".

        Returns:
        dict or None: A dictionary containing Rogowski coil data with keys:
            - "r": numpy array of radial positions
            - "z": numpy array of vertical positions
            - "phi": numpy array of angular positions
            - "area": numpy array of coil areas
            - "names": list of coil names
            Returns None if no data is available.
        """
        rogowski_coil_data = self.get_rogowski_coil_values(select=select)
        if rogowski_coil_data is None:
            return None
        rogowski_coils_dict = {
            "r": [p["r"] for p in rogowski_coil_data],
            "z": [p["z"] for p in rogowski_coil_data],
            "phi": [p["phi"] for p in rogowski_coil_data],
            "area": [p["area"] for p in rogowski_coil_data],
            "names": [p["name"] for p in rogowski_coil_data],
        }
        return rogowski_coils_dict

    def get_shunts(self, select=":"):
        """
        Retrieve shunt data and organize it into a dictionary.

        Parameters:
        select (str): A selection string to filter the shunt data. Default is ":".

        Returns:
        dict: A dictionary containing shunt data with the following keys:
            - "r1": numpy array of r1 values
            - "z1": numpy array of z1 values
            - "r2": numpy array of r2 values
            - "z2": numpy array of z2 values
            - "resitance": numpy array of resistance values
            - "names": list of shunt names

        If no shunt data is found, returns None.
        """
        shunt_data = self.get_shunt_values(select=select)
        if shunt_data is None:
            return None
        shunt_dict = {
            "r1": [p["r1"] for p in shunt_data],
            "z1": [p["z1"] for p in shunt_data],
            "r2": [p["r2"] for p in shunt_data],
            "z2": [p["z2"] for p in shunt_data],
            "resitance": [p["resitance"] for p in shunt_data],
            "names": [p["name"] for p in shunt_data],
        }
        return shunt_dict
