import logging
import os
import re
import typing

import imas
import yaml

from idstools.database import Connection
from idstools.utils.clihelper import getBackendID

logger = logging.getLogger(f"module.{__name__}")


class MachineDescription:
    mdSummaryPath = r"/work/imas/shared/imasdb/ITER_MD/3/md_summary.yaml"

    def __init__(
        self, mdSummaryPath: str = "", connection: typing.Optional[Connection] = None
    ) -> None:
        self.connection = connection
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

    def getMDDataByPulseList(self, pulseList):
        """
        The `getMachineDatabaseData` method is responsible for retrieving machine database data for the specified pulse list. It iterates over each pulse in the `mdSummaryYaml` dictionary and checks if the pulse is present in the `pulseList`. If the pulse is not in the `pulseList`, it skips to the next pulse.
        """
        pulsesData: typing.Dict[str, typing.Dict] = {}
        for pulse, config in self.mdSummaryYaml.items():
            self.connection.shot, self.connection.run = pulse.split("/")
            if pulse not in pulseList:
                continue

            pulsesData[pulse] = {}

            pulsesData[pulse]["data"] = self._getIdsData(config["ids"])
            pulsesData[pulse]["config"] = config
        return pulsesData

    def _getIdsData(self, idsname):
        """
        The `getIdsData` method is responsible for retrieving data from the specified IDS name using the provided connection information. It creates an instance of `imas.DBEntry` with the backend ID, database name, shot number, run number, user, and version provided in the `Connection` object. It then opens the connection to the IDS database using the `open()` method. If the connection is successful, it retrieves the data for the specified IDS name using the `get()` method of the `conn` object. If the connection fails, it logs an error message and returns `None` as the data.
        """
        conn = imas.DBEntry(
            getBackendID(self.connection.backend),
            self.connection.database,
            int(self.connection.shot),
            int(self.connection.run),
            self.connection.user,
            self.connection.version,
        )
        err, n = conn.open()
        if err != 0:
            logger.error(
                "Shot {0}, run {1} for user={2} and database={3} does not exists".format(
                    self.connection.shot,
                    self.connection.run,
                    self.connection.user,
                    self.connection.database,
                )
            )
            data = None
        else:
            data = conn.get(idsname)
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
                pulsesData[pulse]["data"] = None
                if self.connection is not None:
                    self.connection.shot, self.connection.run = pulse.split("/")

                    pulsesData[pulse]["data"] = self._getIdsData(config["ids"])

            pulsesData[pulse]["config"] = config
        return pulsesData

    def getStatus(self, shot: int, run: int):
        """
        The function `getStatus` takes in two parameters, `shot` and `run`, and returns the value of the key "status" from the `yaml` object dictionary using the `shot` and `run` as keys.

        Args:
            shot (int): The "shot" parameter represents the number of shots taken.
            run (int): The "run" parameter represents the number of runs in a particular shot.

        Returns:
            The method `getStatus` returns the value of `"status"` if `yaml` object is not `None`, otherwise it returns `None`.
        """
        shotrun = str(shot) + r"/" + str(run)
        if self.mdSummaryYaml:
            return self.mdSummaryYaml[shotrun]["status"]
        else:
            return None

    def getReasonForReplacement(self, shot: int, run: int):
        """
        The function `getReasonForReplacement` takes in two parameters, `shot` and `run`, and returns the value of the key "reason_for_replacement" from the `yaml` object dictionary using the `shot` and `run` as keys.

        Args:
            shot (int): The "shot" parameter represents the number of shots taken.
            run (int): The "run" parameter represents the number of runs in a particular shot.

        Returns:
            The method `getReasonForReplacement` returns the value of `"reason_for_replacement"` if `yaml` object is not `None`, otherwise it returns `None`.
        """
        shotrun = str(shot) + r"/" + str(run)
        if self.mdSummaryYaml:
            return self.mdSummaryYaml[shotrun]["reason_for_replacement"]
        else:
            return None

    def getReplacedBy(self, shot: int, run: int):
        """
        The function `getReplacedBy` takes in two parameters, `shot` and `run`, and returns the value of the key "replaced_by" from the `yaml` object dictionary using the `shot` and `run` as keys.

        Args:
            shot (int): The "shot" parameter represents the number of shots taken.
            run (int): The "run" parameter represents the number of runs in a particular shot.

        Returns:
            The method `getReplacedBy` returns the value of `"replaced_by"` if `yaml` object is not `None`, otherwise it returns `None`.
        """
        shotrun = str(shot) + r"/" + str(run)
        if self.mdSummaryYaml:
            return self.mdSummaryYaml[shotrun]["replaced_by"]
        else:
            return None

    def getReplaces(self, shot: int, run: int):
        """
        The function `getReplaces` takes in two parameters, `shot` and `run`, and returns the value of the key "replaces" from the `yaml` object dictionary using the `shot` and `run` as keys.

        Args:
            shot (int): The "shot" parameter represents the number of shots taken.
            run (int): The "run" parameter represents the number of runs in a particular shot.

        Returns:
            The method `getReplaces` returns the value of `"replaces"` if `yaml` object is not `None`, otherwise it returns `None`.
        """
        shotrun = str(shot) + r"/" + str(run)
        if self.mdSummaryYaml:
            return self.mdSummaryYaml[shotrun]["replaces"]
        else:
            return None

    def getChildren(self, shot: int, run: int, dictToFill={}):
        """
        The function `getChildren` recursively retrieves information about replaced shots and runs from a dictionary and stores it in a new dictionary.

        Args:
            shot (int): The "shot" parameter is an integer that represents a shot number.
            run (int): The `run` parameter in the `getChildren` method represents the run number.
            dictToFill: The `dictToFill` parameter is a dictionary that is used to store the information about the children of a given shot and run. It is initially an empty dictionary and is passed as an argument to the function to accumulate the information about the children.

        Returns:
            a dictionary `dictToFill` that contains information about the children of a given shot and run. The dictionary has keys "shot", "run", "status", and "reason_for_replacement", and the corresponding values are lists that store the information for each child.
        """
        replaced_by = self.getReplacedBy(shot, run)
        if replaced_by is not None:
            string_list = re.findall(r"\d+", replaced_by)
            shotc = string_list[0]
            runc = string_list[1]
            shotrunc = shotc + "/" + runc
            if not "shot" in dictToFill.keys():
                dictToFill["shot"] = []
            if not "run" in dictToFill.keys():
                dictToFill["run"] = []
            if not "status" in dictToFill.keys():
                dictToFill["status"] = []
            if not "reason_for_replacement" in dictToFill.keys():
                dictToFill["reason_for_replacement"] = []
            dictToFill["shot"].append(shotc)
            dictToFill["run"].append(runc)
            dictToFill["status"].append(self.mdSummaryYaml[shotrunc]["status"])
            dictToFill["reason_for_replacement"].append(
                self.mdSummaryYaml[shotrunc]["reason_for_replacement"]
            )
            dictToFill = self.getChildren(int(shotc), int(runc), dictToFill)
        return dictToFill

    def getParents(self, shot: int, run: int, dictToFill={}):
        """
        The `getParents` function recursively retrieves the parent information for a given shot and run, populating a dictionary with the parent shot, parent run, status, and reason for replacement.

        Args:
            shot (int): The `shot` parameter is an integer that represents a shot number.
            run (int): The `run` parameter is an integer that represents the run number.
            dictToFill: The `dictToFill` parameter is a dictionary that is used to store the information about the parents of a given shot and run. It is initially an empty dictionary and is passed as an argument to the `getParents` function. The function fills this dictionary with the parent   information and returns it.

        Returns:
            a dictionary `dictToFill` that contains information about the parents of a given shot and run.
        """
        replaces = self.getReplaces(shot, run)
        if replaces is not None:
            string_list = re.findall(r"\d+", replaces)
            shotp = string_list[0]
            runp = string_list[1]
            shotrunp = shotp + "/" + runp
            if not "shot" in dictToFill.keys():
                dictToFill["shot"] = []
            if not "run" in dictToFill.keys():
                dictToFill["run"] = []
            if not "status" in dictToFill.keys():
                dictToFill["status"] = []
            if not "reason_for_replacement" in dictToFill.keys():
                dictToFill["reason_for_replacement"] = []

            dictToFill["shot"].insert(0, shotp)  # Order to be reversed for parents
            dictToFill["run"].insert(0, runp)
            dictToFill["status"].insert(0, self.mdSummaryYaml[shotrunp]["status"])
            dictToFill["reason_for_replacement"].insert(
                0, self.mdSummaryYaml[shotrunp]["reason_for_replacement"]
            )
            dictToFill = self.getParents(int(shotp), int(runp), dictToFill)
        return dictToFill

    def getFamily(self, shot: int, run: int):
        """
        The function "getFamily" returns a dictionary containing the parents and children of a given shot and run.

        Args:
            shot (int): The "shot" parameter represents the shot number
            run (int): The "run" parameter is an integer that represents the run number.

        Returns:
            a dictionary called `familyDict` which contains two keys: "parents" and "children". The values associated with these keys are the results of calling the `getParents` and `getChildren` methods with the given `shot` and `run` parameters.
        """
        familyDict = {}
        familyDict["parents"] = self.getParents(shot, run)
        familyDict["children"] = self.getChildren(shot, run)
        return familyDict

    def checkIfExist(self, shot: int, run: int):
        """
        The function checks if a given shot and run combination exists in a yaml dictionary.

        Args:
            shot (int): The "shot" parameter is an integer representing the number.
            run (int): The parameter "run" is an integer representing the number.

        Returns:
            a boolean value. If the `shotrun` key is present in the `yaml` object dictionary, it will  return `True`. Otherwise, it will return `False`.
        """
        shotrun = str(shot) + r"/" + str(run)
        if shotrun not in self.mdSummaryYaml.keys():
            return False
        return True
