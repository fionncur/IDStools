import copy
import logging
import os
import re
import typing

import yaml

from idstools.database import DBMaster

logger = logging.getLogger(f"module.{__name__}")


class MachineDescription:
    mdSummaryPath = r"/work/imas/shared/imasdb/ITER_MD/3/md_summary.yaml"

    def __init__(self, mdSummaryPath: str = "",connectionArgs= None) -> None:
        self.mdArgs = connectionArgs
        if self.mdArgs:
            if "database" in self.mdArgs.__dict__ and self.mdArgs.database == "ITER":
                self.mdArgs.database = "ITER_MD"

        self.mdSummaryYaml = {}
        if not mdSummaryPath:
            _mdSummaryPath = MachineDescription.mdSummaryPath

        else:
            _mdSummaryPath = mdSummaryPath

            if os.path.isdir(_mdSummaryPath):
                _mdSummaryPath = os.path.join(_mdSummaryPath, "md_summary.yaml")
        with open(_mdSummaryPath, "r") as stream:
            try:
                self.mdSummaryYaml = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def getLatestIdsData(self, idsName: str):
        mdIdsDict = self.getMDSummary(idsName)
        idsData = None
        config = None
        # Get wall of the tokamak
        for pulse, _config in mdIdsDict.items():
            if idsName == _config["config"]["ids"]:
                self.mdArgs.pulse, self.mdArgs.run = pulse.split("/")
                self.mdArgs.pulse, self.mdArgs.run = int(self.mdArgs.pulse), int(
                    self.mdArgs.run
                )
                self.mdArgs.uri = f"imas:mdsplus?user=public;shot={self.mdArgs.pulse};run={self.mdArgs.run};database={self.mdArgs.database};version={self.mdArgs.version}"
                mdConnection = DBMaster.getConnection(self.mdArgs)

                # print(mdConnection)
                if mdConnection is not None:
                    idsData = mdConnection.get(idsName)
                    mdConnection.close()
                    if idsData is None:
                        continue
                    else:
                        config = _config["config"]
                        break
        return {
            "idsData": idsData,
            "yamlConfig": config,
            "connectionArgs": copy.deepcopy(self.mdArgs),
        }

    def getMDDataByIdsList(self, mdIdsList=[]):
        """
        The `getMachineDatabaseData` method is responsible for retrieving machine database data for the specified pulse list. It iterates over each pulse in the `mdSummaryYaml` dictionary and checks if the pulse is present in the `pulseList`. If the pulse is not in the `pulseList`, it skips to the next pulse.
        """
        idsData = {}
        for idsName in mdIdsList:
            idsData[idsName] = self.getMDDataByIds(idsName)
        return idsData

    def getMDDataByIds(self, idsName: str):
        outputDict = self.getLatestIdsData(idsName)
        data = {}
        (
            data["idsData"],
            data["yamlConfig"],
            data["connectionArgs"],
        ) = (
            outputDict["idsData"],
            outputDict["yamlConfig"],
            outputDict["connectionArgs"],
        )
        return data
    
    def getMDSummary(
        self,
        idsNames: typing.Union[typing.List, str] = "",
        addObsoelete=False,
        checkValidity=False,
    ):
        """
        The `readMDSummary` method is responsible for reading the machine description summary and retrieving data for the specified IDS names.
        """
        # if provided just single string then convert to list with single string
        if type(idsNames) == str:
            idsNames = [idsNames]
        # lower case provided ids names
        idsNames = list(map(lambda x: x.lower(), idsNames))
        pulsesData: typing.Dict[str, typing.Dict] = {}
        for pulse, config in self.mdSummaryYaml.items():
            if idsNames:
                if config["ids"] not in idsNames:
                    continue

            if addObsoelete is False:
                if config["status"] == "obsolete":
                    continue

            pulsesData[pulse] = {}
            pulsesData[pulse]["data"] = None
            if checkValidity:
                self.mdArgs.pulse, self.mdArgs.run = pulse.split("/")
                self.mdArgs.pulse, self.mdArgs.run = int(self.mdArgs.pulse), int(
                    self.mdArgs.run
                )
                self.mdArgs.uri = f"imas:mdsplus?user=public;pulse={self.mdArgs.pulse};run={self.mdArgs.run};database={self.mdArgs.database};version={self.mdArgs.version}"
                mdConnection = DBMaster.getConnection(self.mdArgs)
                if mdConnection is not None:
                    idsData = mdConnection.get(config["ids"])
                    if idsData is not None:
                        pulsesData[pulse]["data"]
                    mdConnection.close()

            pulsesData[pulse]["config"] = config
        return pulsesData

    def getPandasDataFrame(self):
        """
        The function `getPandasDataFrame` converts a dictionary into a pandas DataFrame.

        Returns:
          a pandas DataFrame object.
        """
        import pandas as pd

        dataList = [{"id": key, **value} for key, value in self.mdSummaryYaml.items()]
        df = pd.DataFrame(dataList)
        return df

    def getStatus(self, pulse: int, run: int):
        """
        The function `getStatus` takes in two parameters, `pulse` and `run`, and returns the value of the key "status" from the `yaml` object dictionary using the `pulse` and `run` as keys.

        Args:
            pulse (int): The "pulse" parameter represents the number of pulses taken.
            run (int): The "run" parameter represents the number of runs in a particular pulse.

        Returns:
            The method `getStatus` returns the value of `"status"` if `yaml` object is not `None`, otherwise it returns `None`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if self.mdSummaryYaml:
            return self.mdSummaryYaml[pulserun]["status"]
        else:
            return None

    def getReasonForReplacement(self, pulse: int, run: int):
        """
        The function `getReasonForReplacement` takes in two parameters, `pulse` and `run`, and returns the value of the key "reason_for_replacement" from the `yaml` object dictionary using the `pulse` and `run` as keys.

        Args:
            pulse (int): The "pulse" parameter represents the number of pulses taken.
            run (int): The "run" parameter represents the number of runs in a particular pulse.

        Returns:
            The method `getReasonForReplacement` returns the value of `"reason_for_replacement"` if `yaml` object is not `None`, otherwise it returns `None`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if self.mdSummaryYaml:
            return self.mdSummaryYaml[pulserun]["reason_for_replacement"]
        else:
            return None

    def getReplacedBy(self, pulse: int, run: int):
        """
        The function `getReplacedBy` takes in two parameters, `pulse` and `run`, and returns the value of the key "replaced_by" from the `yaml` object dictionary using the `pulse` and `run` as keys.

        Args:
            pulse (int): The "pulse" parameter represents the number of pulses taken.
            run (int): The "run" parameter represents the number of runs in a particular pulse.

        Returns:
            The method `getReplacedBy` returns the value of `"replaced_by"` if `yaml` object is not `None`, otherwise it returns `None`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if self.mdSummaryYaml:
            return self.mdSummaryYaml[pulserun]["replaced_by"]
        else:
            return None

    def getReplaces(self, pulse: int, run: int):
        """
        The function `getReplaces` takes in two parameters, `pulse` and `run`, and returns the value of the key "replaces" from the `yaml` object dictionary using the `pulse` and `run` as keys.

        Args:
            pulse (int): The "pulse" parameter represents the number of pulses taken.
            run (int): The "run" parameter represents the number of runs in a particular pulse.

        Returns:
            The method `getReplaces` returns the value of `"replaces"` if `yaml` object is not `None`, otherwise it returns `None`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if self.mdSummaryYaml:
            return self.mdSummaryYaml[pulserun]["replaces"]
        else:
            return None

    def getChildren(self, pulse: int, run: int, dictToFill={}):
        """
        The function `getChildren` recursively retrieves information about replaced pulses and runs from a dictionary and stores it in a new dictionary.

        Args:
            pulse (int): The "pulse" parameter is an integer that represents a pulse number.
            run (int): The `run` parameter in the `getChildren` method represents the run number.
            dictToFill: The `dictToFill` parameter is a dictionary that is used to store the information about the children of a given pulse and run. It is initially an empty dictionary and is passed as an argument to the function to accumulate the information about the children.

        Returns:
            a dictionary `dictToFill` that contains information about the children of a given pulse and run. The dictionary has keys "pulse", "run", "status", and "reason_for_replacement", and the corresponding values are lists that store the information for each child.
        """
        replaced_by = self.getReplacedBy(pulse, run)
        if replaced_by is not None:
            string_list = re.findall(r"\d+", replaced_by)
            pulsec = string_list[0]
            runc = string_list[1]
            pulserunc = pulsec + "/" + runc
            if not "pulse" in dictToFill.keys():
                dictToFill["pulse"] = []
            if not "run" in dictToFill.keys():
                dictToFill["run"] = []
            if not "status" in dictToFill.keys():
                dictToFill["status"] = []
            if not "reason_for_replacement" in dictToFill.keys():
                dictToFill["reason_for_replacement"] = []
            dictToFill["pulse"].append(pulsec)
            dictToFill["run"].append(runc)
            dictToFill["status"].append(self.mdSummaryYaml[pulserunc]["status"])
            dictToFill["reason_for_replacement"].append(
                self.mdSummaryYaml[pulserunc]["reason_for_replacement"]
            )
            dictToFill = self.getChildren(int(pulsec), int(runc), dictToFill)
        return dictToFill

    def getParents(self, pulse: int, run: int, dictToFill={}):
        """
        The `getParents` function recursively retrieves the parent information for a given pulse and run, populating a dictionary with the parent pulse, parent run, status, and reason for replacement.

        Args:
            pulse (int): The `pulse` parameter is an integer that represents a pulse number.
            run (int): The `run` parameter is an integer that represents the run number.
            dictToFill: The `dictToFill` parameter is a dictionary that is used to store the information about the parents of a given pulse and run. It is initially an empty dictionary and is passed as an argument to the `getParents` function. The function fills this dictionary with the parent   information and returns it.

        Returns:
            a dictionary `dictToFill` that contains information about the parents of a given pulse and run.
        """
        replaces = self.getReplaces(pulse, run)
        if replaces is not None:
            string_list = re.findall(r"\d+", replaces)
            pulsep = string_list[0]
            runp = string_list[1]
            pulserunp = pulsep + "/" + runp
            if not "pulse" in dictToFill.keys():
                dictToFill["pulse"] = []
            if not "run" in dictToFill.keys():
                dictToFill["run"] = []
            if not "status" in dictToFill.keys():
                dictToFill["status"] = []
            if not "reason_for_replacement" in dictToFill.keys():
                dictToFill["reason_for_replacement"] = []

            dictToFill["pulse"].insert(0, pulsep)  # Order to be reversed for parents
            dictToFill["run"].insert(0, runp)
            dictToFill["status"].insert(0, self.mdSummaryYaml[pulserunp]["status"])
            dictToFill["reason_for_replacement"].insert(
                0, self.mdSummaryYaml[pulserunp]["reason_for_replacement"]
            )
            dictToFill = self.getParents(int(pulsep), int(runp), dictToFill)
        return dictToFill

    def getFamily(self, pulse: int, run: int):
        """
        The function "getFamily" returns a dictionary containing the parents and children of a given pulse and run.

        Args:
            pulse (int): The "pulse" parameter represents the pulse number
            run (int): The "run" parameter is an integer that represents the run number.

        Returns:
            a dictionary called `familyDict` which contains two keys: "parents" and "children". The values associated with these keys are the results of calling the `getParents` and `getChildren` methods with the given `pulse` and `run` parameters.
        """
        familyDict = {}
        familyDict["parents"] = self.getParents(pulse, run)
        familyDict["children"] = self.getChildren(pulse, run)
        return familyDict

    def checkIfExist(self, pulse: int, run: int):
        """
        The function checks if a given pulse and run combination exists in a yaml dictionary.

        Args:
            pulse (int): The "pulse" parameter is an integer representing the number.
            run (int): The parameter "run" is an integer representing the number.

        Returns:
            a boolean value. If the `pulserun` key is present in the `yaml` object dictionary, it will  return `True`. Otherwise, it will return `False`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if pulserun not in self.mdSummaryYaml.keys():
            return False
        return True
