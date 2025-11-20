import logging
import os
import re
import time

import pandas as pd
import yaml

try:
    from yaml import CLoader as Loader

except ImportError:
    from yaml import Loader

from concurrent.futures import ThreadPoolExecutor

from pandas import json_normalize

from idstools.view.common import Terminal

logger = logging.getLogger("module")

yaml_mapping = {
    "reference_name": "ref_name",
    "responsible_name": "ro_name",
    "characteristics.shot": "pulse",
    "characteristics.run": "run",
    "characteristics.type": "type",
    "characteristics.workflow": "workflow",
    "characteristics.machine": "database",
    "scenario_key_parameters.confinement_regime": "confinement",
    "scenario_key_parameters.plasma_current": "ip",
    "scenario_key_parameters.magnetic_field": "b0",
    "scenario_key_parameters.main_species": "fuelling",
    "scenario_key_parameters.central_electron_density": "ne0",
    "scenario_key_parameters.sepmid_electron_density": "nesep",
    "scenario_key_parameters.central_zeff": "zeff",
    "scenario_key_parameters.sepmid_zeff": "zeff_sep",
    "scenario_key_parameters.density_peaking": "npeak",
    "hcd.p_hcd": "p_hcd",
    "hcd.p_ec": "p_ec",
    "hcd.p_ic": "p_ic",
    "hcd.p_nbi": "p_nbi",
    "hcd.p_lh": "p_lh",
    "hcd.p_sol": "p_sol",
    "free_description": "extra",
    "ids_list": "idslist",
    "tsteps": "tsteps",
    "location": "location",
    "plasma_composition.species": "species",
    "plasma_composition.n_over_e": "pc_n_over_ne",
    "plasma_composition.a": "pc_a",
    "plasma_composition.z": "pc_z",
    "plasma_composition.n_over_ntot": "pc_n_over_ntot",
    "plasma_composition.n_over_n_maj": "pc_n_over_n_maj",
    "lastmodified": "date",
}


# Class is a base class for scenario descriptions.
class ScenarioDescriptionSummary:
    def __init__(self, directory_list=[]) -> None:
        """
        The function initializes a directory list variable based on the provided input or a default value.

        Args:
            directory_list (list): A list of directory paths to search for scenario files.
        """
        self.directory_list = directory_list

    @staticmethod
    def get_yaml_data(yaml_file_path):
        """
        The function `get_yaml_data` reads a YAML file and returns its contents as a Python object.

        Args:
            yaml_file_path: The `yaml_file_path` parameter is a string that represents the file path of the YAML
                file that you want to load and retrieve data from.

        Returns:
            the data loaded from the YAML file.
        """
        with open(yaml_file_path, "r", encoding="utf-8") as file_handle:
            try:
                yaml_data = yaml.load(file_handle, Loader=Loader)
            except Exception as e:
                logger.warning(f"Could not read yaml file: {yaml_file_path} {e}")
                yaml_data = None
        return yaml_data

    @staticmethod
    def get_data_frame_from_yaml(yaml_file_path, add_obsolete=False):
        """
        The function `get_data_frame_from_yaml` takes a YAML file path, reads the data from the file, checks if
        the status is active (unless `addObsolete` is set to True), converts the data into a flat table, and
        returns it as a pandas DataFrame.

        Args:
            yaml_file_path: The path to the YAML file from which you want to create a DataFrame.
            add_obsolete: The add_obsolete parameter is a boolean flag that determines whether or not to include
                obsolete data in the resulting DataFrame.

        Returns:
            a pandas DataFrame object.
        """
        yaml_data = ScenarioDescriptionSummary.get_yaml_data(yaml_file_path)
        if yaml_data is None:
            return None
        if add_obsolete is False:
            if yaml_data["status"] != "active":
                return None
        flat_table = json_normalize(yaml_data)
        data_frame = pd.DataFrame(flat_table)
        return data_frame

    def get_dataframes_from_files(self, extension=".yaml", add_obsolete=False):
        """
        The function `get_dataframes_from_files` retrieves data from YAML files, creates dataframes, adds additional
        information, and returns a concatenated dataframe.

        Args:
            extension: The "extension" parameter is a string that specifies the file extension to search for.
            add_obsolete: The "add_obsolete" parameter is a boolean flag that determines whether or not to
                include obsolete data in the resulting dataframes.

        Returns:
            a pandas DataFrame object.
        """
        files = []
        for folder_path in self.directory_list:
            for root, _, filenames in os.walk(folder_path):
                for filename in filenames:
                    if filename.endswith(extension):
                        files.append(os.path.join(root, filename))

        if extension == ".yaml":
            data_frames = []
            append_df = data_frames.append

            def process_yaml_file(yaml_file):
                df = ScenarioDescriptionSummary.get_data_frame_from_yaml(yaml_file, add_obsolete=add_obsolete)
                yaml_file = os.path.abspath(yaml_file)
                if df is not None:
                    df["dd_version"] = ""
                    if "ITER/3/0" in yaml_file or "iterdb/3/0" in yaml_file:
                        df["dd_version"] = "3"
                    elif "ITER/4/" in yaml_file or "iterdb/4/" in yaml_file:
                        df["dd_version"] = "4"

                    df["location"] = yaml_file
                    local_time = time.ctime(os.path.getmtime(yaml_file))
                    df["lastmodified"] = pd.to_datetime(local_time)
                    self._extract_information(df)
                    return df
                return None

            with ThreadPoolExecutor() as executor:
                results = executor.map(process_yaml_file, files)

            for result in results:
                if result is not None:
                    append_df(result)
        df = pd.concat(data_frames, ignore_index=True)
        df = df.rename(columns=yaml_mapping)
        return df

    def _extract_information(self, df):
        """
        The function `_extract_information` extracts information from a DataFrame and adds new columns based
        on the extracted data.

        Args:
            df: The parameter `df` is a pandas DataFrame object.
        """
        if "idslist.summary.time_step_number" in df.columns:
            df["tsteps"] = df["idslist.summary.time_step_number"]

        idslist = set([x.split(".")[1] for x in df.columns if "idslist" in x])
        df["idslist"] = ",".join(idslist)
        species = n_over_ne = None
        if "plasma_composition.species" in df.columns:
            species = str(df["plasma_composition.species"][0])
        if "plasma_composition.n_over_ne" in df.columns:
            n_over_ne = str(df["plasma_composition.n_over_ne"][0])

        if species is not None and n_over_ne is not None:
            species = species.split()
            n_over_ne = n_over_ne.split()

            species_dict = {k: v for k, v in zip(species, n_over_ne)}
            sorted_dict = dict(sorted(species_dict.items(), key=lambda item: float(item[1]), reverse=True))
            df["composition"] = ",".join([f"{key}({value})" for key, value in sorted_dict.items()])
        else:
            df["composition"] = "None"


# The class ScenarioDescription
class ScenarioDescription:
    def __init__(self, pulse: int, run: int, yaml_path: str) -> None:
        """
        The above function initializes an object with a pulse, run, and yaml path, and attempts to load
        YAML data from a file.

        Args:
            pulse (int): The "pulse" parameter is an integer that represents a pulse number.
            run (int): The `run` parameter is an integer that represents the run number.
            yaml_path (str): The `yaml_path` parameter is a string that represents the path to the YAML file.
        """
        self.yaml_path = yaml_path
        self.yaml_data = None
        try:
            with open(self.yaml_path, "r") as f:
                self.yaml_data = yaml.safe_load(f)
        except Exception as e:
            logger.debug(f"{e}")
            logger.critical(f"{e}")

    def get_children(self, yaml_data, dict_to_fill={}):
        """
        The function `get_children` recursively retrieves data from a YAML file and populates a dictionary
        with specific keys and values.

        Args:
            yaml_data: The `yaml_data` parameter is a dictionary that contains data in YAML format.
            dict_to_fill: The `dict_to_fill` parameter is a dictionary that is used to store the values extracted
                from the `yaml data` . It is initially an empty dictionary and is passed as an argument to the
                `get_children` function.

        Returns:
            the dictionary with scenario children.
        """
        if yaml_data is None:
            return dict_to_fill
        replaced_by = None
        if "database_relations" in yaml_data.keys():
            if "replaced_by" in yaml_data["database_relations"].keys():
                replaced_by = yaml_data["database_relations"]["replaced_by"]
        if "pulse" not in dict_to_fill.keys():
            dict_to_fill["pulse"] = []
        if "run" not in dict_to_fill.keys():
            dict_to_fill["run"] = []
        if "status" not in dict_to_fill.keys():
            dict_to_fill["status"] = []
        if "comment" not in dict_to_fill.keys():
            dict_to_fill["comment"] = []
        if replaced_by is not None:
            string_list = re.findall(r"\d+", replaced_by)
            pulsec = string_list[0]
            runc = string_list[1]

            parent_dir = os.path.dirname(self.yaml_path)
            if os.path.basename(parent_dir) == "0":
                yaml_file_name = parent_dir + f'/ids_{pulsec}{str(runc).rjust(4, "0")}.yaml'
            else:
                grandparent_dir = os.path.dirname(os.path.dirname(parent_dir))
                yaml_file_name = grandparent_dir + f'/{pulsec}/{runc}/ids_{pulsec}{str(runc).rjust(4, "0")}.yaml'

            scenario_description = ScenarioDescription(pulsec, runc, yaml_file_name)

            if scenario_description.yaml_data is not None:
                dict_to_fill["pulse"].append(pulsec)
                dict_to_fill["run"].append(runc)
                dict_to_fill["status"].append(scenario_description.yaml_data["status"])
                dict_to_fill["comment"].append(scenario_description.yaml_data["database_relations"]["replaces"])
                dict_to_fill = self.get_children(scenario_description.yaml_data, dict_to_fill)
        return dict_to_fill

    def get_parents(self, yaml_data, dict_to_fill={}):
        """
        The function `get_parents` retrieves parent data from a YAML file and populates a dictionary with the
        parent information.

        Args:
            yaml_data: The `yaml_data` parameter is a dictionary that contains data in YAML format.
            dict_to_fill: The `dict_to_fill` parameter is a dictionary that is used to store the parents information.
                It is initially empty and is filled with parent data as the function recursively calls itself.

        Returns:
            the dictionary with scenario parents
        """
        if yaml_data is None:
            return dict_to_fill
        replaces = None
        if "database_relations" in yaml_data.keys():
            if "replaces" in yaml_data["database_relations"].keys():
                replaces = yaml_data["database_relations"]["replaces"]
        if "pulse" not in dict_to_fill.keys():
            dict_to_fill["pulse"] = []
        if "run" not in dict_to_fill.keys():
            dict_to_fill["run"] = []
        if "status" not in dict_to_fill.keys():
            dict_to_fill["status"] = []
        if "comment" not in dict_to_fill.keys():
            dict_to_fill["comment"] = []
        if replaces is not None:
            string_list = re.findall(r"\d+", replaces)
            pulsep = string_list[0]
            runp = string_list[1]
            parent_dir = os.path.dirname(self.yaml_path)

            if os.path.basename(parent_dir) == "0":
                yaml_file_name = parent_dir + f'/ids_{pulsep}{str(runp).rjust(4, "0")}.yaml'
            else:
                grandparent_dir = os.path.dirname(os.path.dirname(parent_dir))
                yaml_file_name = grandparent_dir + f'/{pulsep}/{runp}/ids_{pulsep}{str(runp).rjust(4, "0")}.yaml'

            scenario_description = ScenarioDescription(pulsep, runp, yaml_file_name)

            if scenario_description.yaml_data is not None:
                dict_to_fill["pulse"].insert(0, pulsep)  # Order to be reversed for parents
                dict_to_fill["run"].insert(0, runp)
                dict_to_fill["status"].insert(0, scenario_description.yaml_data["status"])
                dict_to_fill["comment"].insert(0, scenario_description.yaml_data["database_relations"]["replaces"])
                dict_to_fill = self.get_parents(scenario_description.yaml_data, dict_to_fill)
        return dict_to_fill

    def get_family(self):
        """
        The function "get_family" returns a dictionary containing the parents and children of a scenario based
        on the provided YAML data.

        Returns:
            a dictionary called `family_dict` which contains two keys: "parents" and "children". The values
            associated with these keys are the results of calling the `get_parents` and `get_children` methods,
            passing in `yaml data` as argument.
        """
        family_dict = {}
        family_dict["parents"] = self.get_parents(self.yaml_data, {})
        family_dict["children"] = self.get_children(self.yaml_data, {})
        return family_dict

    def print_yaml(self):
        """
        The function `print_yaml` prints the `yaml_data` attribute of the object on Terminal.
        """
        terminal = Terminal()
        terminal.print(self.yaml_data)


if __name__ == "__main__":
    default_folder_path = r"/work/imas/shared/imasdb/ITER/3/0"
    scenario_description_obj = ScenarioDescriptionSummary(folder_path=default_folder_path)
    df = scenario_description_obj.get_dataframes_from_files(extension=".yaml", add_obsolete=False)
