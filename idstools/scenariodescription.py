import glob
import logging
import os
import re
import time

import pandas as pd
from yaml import load as yamlload
try:
    from yaml import CLoader as yamlLoader
except ImportError:
    from yaml import Loader as yamlLoader
from pandas import json_normalize

from idstools.view.common import Terminal

logger = logging.getLogger("module")

yamlMapping = {
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
    "location": "location",
}


# Class is a base class for scenario descriptions.
class ScenarioDescriptionBase:
    def __init__(self, folderPath=os.getcwd()) -> None:
        """
        The function initializes a folder path variable based on the provided input or a default value.

        Args:
            folderPath (str): The `folderPath` parameter is a string that represents the path to a folder.
        """
        if os.path.exists(folderPath):
            self.folderPath = folderPath

    @staticmethod
    def getYamlData(yamlFilePath):
        """
        The function `getYamlData` reads a YAML file and returns its contents as a Python object.

        Args:
            yamlFilePath: The `yamlFilePath` parameter is a string that represents the file path of the YAML file that you want to load and retrieve data from.

        Returns:
            the data loaded from the YAML file.
        """
        with open(yamlFilePath, "r") as fileHandle:
            try:
                yamlData = yamlload(fileHandle, Loader=yamlCLoader)
            except Exception as e:
                yamlData = None
        return yamlData

    @staticmethod
    def getDataFrameFromYaml(yamlFilePath, addObsolete=False):
        """
        The function `getDataFrameFromYaml` takes a YAML file path, reads the data from the file, checks if the status is active (unless `addObsolete` is set to True), converts the data into a flat table, and returns it as a pandas DataFrame.

        Args:
            yamlFilePath: The path to the YAML file from which you want to create a DataFrame.
            addObsolete: The addObsolete parameter is a boolean flag that determines whether or not to include obsolete data in the resulting DataFrame.

        Returns:
            a pandas DataFrame object.
        """
        yamlData = ScenarioDescriptionBase.getYamlData(yamlFilePath)
        if addObsolete is False:
            if yamlData["status"] != "active":
                return None
        if yamlData is None:
            return None
        flatTable = json_normalize(yamlData)
        dataFrame = pd.DataFrame(flatTable)
        return dataFrame

    def getDataframesFromFiles(self, extension=".yaml", addObsolete=False):
        """
        The function `getDataframesFromFiles` retrieves data from YAML files, creates dataframes, adds additional information, and returns a concatenated dataframe.

        Args:
            extension: The "extension" parameter is a string that specifies the file extension to search for.
            addObsolete: The "addObsolete" parameter is a boolean flag that determines whether or not to
        include obsolete data in the resulting dataframes.

        Returns:
            a pandas DataFrame object.
        """
        files = glob.glob(f"{self.folderPath}/**/*{extension}", recursive=True)
        if extension == ".yaml":
            dataFrames = []
            for yamlFile in files:
                df = ScenarioDescriptionBase.getDataFrameFromYaml(
                    yamlFile, addObsolete=addObsolete
                )
                if df is not None:
                    df["location"] = yamlFile
                    localTime = time.ctime(os.path.getmtime(yamlFile))
                    df["lastmodified"] = pd.to_datetime(localTime)
                    self._extractInformation(df)
                    dataFrames.append(df)

        df = pd.concat(dataFrames, ignore_index=True)
        df = df.rename(columns=yamlMapping)
        return df

    def _extractInformation(self, df):
        """
        The function `_extractInformation` extracts information from a DataFrame and adds new columns based on the extracted data.

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

            speciesDict = {k: v for k, v in zip(species, n_over_ne)}
            sorted_dict = dict(
                sorted(
                    speciesDict.items(), key=lambda item: float(item[1]), reverse=True
                )
            )
            df["composition"] = ",".join(
                [f"{key}({value})" for key, value in sorted_dict.items()]
            )
        else:
            df["composition"] = "None"


# The class ScenarioDescription is a subclass of ScenarioDescriptionBase.
class ScenarioDescription(ScenarioDescriptionBase):
    def __init__(self, pulse: int, run: int, folderPath: str = "") -> None:
        """
        The above function initializes an object with a pulse, run, and folder path, and attempts to load YAML data from a file based on the pulse and run numbers.

        Args:
            pulse (int): The "pulse" parameter is an integer that represents a pulse number. It is used to construct the filename for the YAML file that will be loaded.
            run (int): The `run` parameter is an integer that represents the run number.
            folderPath (str): The `folderPath` parameter is a string that represents the path to a folder where the YAML file is located.
        """
        super().__init__(folderPath)
        yamlFileName = self.folderPath + f'/ids_{pulse}{str(run).rjust(4,"0")}.yaml'
        self.yamlData = None
        try:
            with open(yamlFileName, "r") as f:
                self.yamlData = yamlload(f, Loader=yamlCLoader)
        except Exception as exc:
            logger.critical(f"Warning: {exc}")

    def getChildren(self, yamlData, dictToFill={}):
        """
        The function `getChildren` recursively retrieves data from a YAML file and populates a dictionary with specific keys and values.

        Args:
            yamlData: The `yamlData` parameter is a dictionary that contains data in YAML format.
            dictToFill: The `dictToFill` parameter is a dictionary that is used to store the values extracted from the `yaml data` . It is initially an empty dictionary and is passed as an argument to the `getChildren` function.

        Returns:
            the dictionary with scenario children.
        """
        replaced_by = None
        if "database_relations" in yamlData.keys():
            if "replaced_by" in yamlData["database_relations"].keys():
                replaced_by = yamlData["database_relations"]["replaced_by"]
        if not "pulse" in dictToFill.keys():
            dictToFill["pulse"] = []
        if not "run" in dictToFill.keys():
            dictToFill["run"] = []
        if not "status" in dictToFill.keys():
            dictToFill["status"] = []
        if not "comment" in dictToFill.keys():
            dictToFill["comment"] = []
        if replaced_by is not None:
            string_list = re.findall(r"\d+", replaced_by)
            pulsec = string_list[0]
            runc = string_list[1]
            scenarioDescription = ScenarioDescription(pulsec, runc, self.folderPath)

            if scenarioDescription.yamlData is not None:
                dictToFill["pulse"].append(pulsec)
                dictToFill["run"].append(runc)
                dictToFill["status"].append(scenarioDescription.yamlData["status"])
                dictToFill["comment"].append(
                    scenarioDescription.yamlData["database_relations"]["replaces"]
                )
                dictToFill = self.getChildren(scenarioDescription.yamlData, dictToFill)
        return dictToFill

    def getParents(self, yamlData, dictToFill={}):
        """
        The function `getParents` retrieves parent data from a YAML file and populates a dictionary with the parent information.

        Args:
            yamlData: The `yamlData` parameter is a dictionary that contains data in YAML format.
            dictToFill: The `dictToFill` parameter is a dictionary that is used to store the parents information. It is initially empty and is filled with parent data as the function recursively calls itself.

        Returns:
            the dictionary with scenario parents
        """
        replaces = None
        if "database_relations" in yamlData.keys():
            if "replaces" in yamlData["database_relations"].keys():
                replaces = yamlData["database_relations"]["replaces"]
        if not "pulse" in dictToFill.keys():
            dictToFill["pulse"] = []
        if not "run" in dictToFill.keys():
            dictToFill["run"] = []
        if not "status" in dictToFill.keys():
            dictToFill["status"] = []
        if not "comment" in dictToFill.keys():
            dictToFill["comment"] = []
        if replaces is not None:
            string_list = re.findall(r"\d+", replaces)
            pulsep = string_list[0]
            runp = string_list[1]
            scenarioDescription = ScenarioDescription(pulsep, runp, self.folderPath)

            if scenarioDescription.yamlData is not None:
                dictToFill["pulse"].insert(
                    0, pulsep
                )  # Order to be reversed for parents
                dictToFill["run"].insert(0, runp)
                dictToFill["status"].insert(0, scenarioDescription.yamlData["status"])
                dictToFill["comment"].insert(
                    0, scenarioDescription.yamlData["database_relations"]["replaces"]
                )
                dictToFill = self.getParents(scenarioDescription.yamlData, dictToFill)
        return dictToFill

    def getFamily(self):
        """
        The function "getFamily" returns a dictionary containing the parents and children of a scenario based on the provided YAML data.

        Returns:
            a dictionary called `familyDict` which contains two keys: "parents" and "children". The values associated with these keys are the results of calling the `getParents` and `getChildren` methods, passing in `yaml data` as argument.
        """
        familyDict = {}
        familyDict["parents"] = self.getParents(self.yamlData, {})
        familyDict["children"] = self.getChildren(self.yamlData, {})
        return familyDict

    def printYaml(self):
        """
        The function `printYaml` prints the `yamlData` attribute of the object on terminal.
        """
        terminal = Terminal()
        terminal.print(self.yamlData)


if __name__ == "__main__":
    defaultFolderPath = r"/work/imas/shared/imasdb/ITER/3/0"
    scenarioDescriptionObj = ScenarioDescriptionBase(folderPath=defaultFolderPath)
    df = scenarioDescriptionObj.getDataframesFromFiles(
        extension=".yaml", addObsolete=False
    )
