import logging
import os
import re

import yaml

from idstools.view.common import Terminal

logger = logging.getLogger("module")


# Class is a base class for scenario descriptions.
class ScenarioDescriptionBase:
    def __init__(self, folderPath: str = "") -> None:
        """
        The function initializes a folder path variable based on the provided input or a default value.

        Args:
            folderPath (str): The `folderPath` parameter is a string that represents the path to a folder.
        """
        defaultFolderPath = os.environ["IMAS_HOME"] + "/shared/imasdb/ITER/3/0"
        lowlevelVersion = int(os.environ["UAL_VERSION"][0])
        if lowlevelVersion < 4:
            defaultFolderPath = os.environ["IMAS_HOME"] + "/shared/iterdb/3/0"

        if os.path.exists(folderPath):
            self.folderPath = folderPath
        else:
            self.folderPath = defaultFolderPath


# The class ScenarioDescription is a subclass of ScenarioDescriptionBase.
class ScenarioDescription(ScenarioDescriptionBase):
    def __init__(self, shot: int, run: int, folderPath: str = "") -> None:
        """
        The above function initializes an object with a shot, run, and folder path, and attempts to load YAML data from a file based on the shot and run numbers.

        Args:
            shot (int): The "shot" parameter is an integer that represents a shot number. It is used to construct the filename for the YAML file that will be loaded.
            run (int): The `run` parameter is an integer that represents the run number.
            folderPath (str): The `folderPath` parameter is a string that represents the path to a folder where the YAML file is located.
        """
        super().__init__(folderPath)
        yamlFileName = self.folderPath + f'/ids_{shot}{str(run).rjust(4,"0")}.yaml'

        self.yamlData = None
        try:
            with open(yamlFileName, "r") as f:
                self.yamlData = yaml.load(f, Loader=yaml.CLoader)
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
        replaced_by = yamlData["database_relations"]["replaced_by"]
        if not "shot" in dictToFill.keys():
            dictToFill["shot"] = []
        if not "run" in dictToFill.keys():
            dictToFill["run"] = []
        if not "status" in dictToFill.keys():
            dictToFill["status"] = []
        if not "comment" in dictToFill.keys():
            dictToFill["comment"] = []
        if replaced_by is not None:
            string_list = re.findall(r"\d+", replaced_by)
            shotc = string_list[0]
            runc = string_list[1]
            scenarioDescription = ScenarioDescription(shotc, runc, self.folderPath)

            if scenarioDescription.yamlData is not None:
                dictToFill["shot"].append(shotc)
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
        replaces = yamlData["database_relations"]["replaces"]
        if not "shot" in dictToFill.keys():
            dictToFill["shot"] = []
        if not "run" in dictToFill.keys():
            dictToFill["run"] = []
        if not "status" in dictToFill.keys():
            dictToFill["status"] = []
        if not "comment" in dictToFill.keys():
            dictToFill["comment"] = []
        if replaces is not None:
            string_list = re.findall(r"\d+", replaces)
            shotp = string_list[0]
            runp = string_list[1]
            scenarioDescription = ScenarioDescription(shotp, runp, self.folderPath)

            if scenarioDescription.yamlData is not None:
                dictToFill["shot"].insert(0, shotp)  # Order to be reversed for parents
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
