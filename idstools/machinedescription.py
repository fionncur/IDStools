import copy
import logging
import os
import re
import typing

from yaml import YAMLError, safe_load

from idstools.database import DBMaster

logger = logging.getLogger(f"module.{__name__}")


class MachineDescription:
    md_summary_path = r"/work/imas/shared/imasdb/ITER_MD/3/md_summary.yaml"

    def __init__(self, md_summary_path: str = "", connection_args=None) -> None:
        self.md_args = connection_args
        if self.md_args:
            if "database" in self.md_args.__dict__ and self.md_args.database == "ITER":
                self.md_args.database = "ITER_MD"

        self.md_summary_yaml = {}
        if not md_summary_path:
            _md_summary_path = MachineDescription.md_summary_path

        else:
            _md_summary_path = md_summary_path

            if os.path.isdir(_md_summary_path):
                _md_summary_path = os.path.join(_md_summary_path, "md_summary.yaml")
        with open(_md_summary_path, "r") as stream:
            try:
                self.md_summary_yaml = safe_load(stream)
            except YAMLError as exc:
                print(exc)

    def get_latest_ids_data(self, ids_name: str):
        md_ids_dict = self.get_md_summary(ids_name)
        ids_data = None
        config = None
        # Get wall of the tokamak
        import argparse

        md_args = argparse.Namespace()
        md_args.backend = "MDSPLUS"
        md_args.pulse = 0
        md_args.run = 0
        md_args.user = "public"
        md_args.database = "ITER_MD"
        md_args.version = 3
        md_args.uri = None
        for pulse, _config in md_ids_dict.items():
            if ids_name == _config["config"]["ids"]:
                md_args.pulse, md_args.run = pulse.split("/")
                md_args.pulse, md_args.run = int(md_args.pulse), int(md_args.run)
                md_args.uri = (
                    f"imas:{md_args.backend.lower()}?user={md_args.user};shot={md_args.pulse};"
                    f"run={md_args.run};database={md_args.database};version={md_args.version}"
                )
                md_connection = DBMaster.get_connection(md_args)

                # print(mdConnection)
                if md_connection is not None:
                    ids_data = md_connection.get(ids_name)
                    md_connection.close()
                    if ids_data is None:
                        continue
                    else:
                        config = _config["config"]
                        break
        return {
            "idsData": ids_data,
            "yamlConfig": config,
            "connectionArgs": copy.deepcopy(md_args),
        }

    def get_md_data_by_ids_list(self, md_ids_list=[]):
        """
        The `getMachineDatabaseData` method is responsible for retrieving machine database data for the specified
        pulse list. It iterates over each pulse in the `mdSummaryYaml` dictionary and checks if the pulse is present
        in the `pulseList`. If the pulse is not in the `pulseList`, it skips to the next pulse.
        """
        ids_data = {}
        for ids_name in md_ids_list:
            ids_data[ids_name] = self.get_m_d_data_by_ids(ids_name)
        return ids_data

    def get_m_d_data_by_ids(self, ids_name: str):
        output_dict = self.get_latest_ids_data(ids_name)
        data = {}
        (
            data["idsData"],
            data["yamlConfig"],
            data["connectionArgs"],
        ) = (
            output_dict["idsData"],
            output_dict["yamlConfig"],
            output_dict["connectionArgs"],
        )
        return data

    def get_md_summary(
        self,
        ids_names: typing.Union[typing.List, str] = "",
        add_obsoelete=False,
        check_validity=False,
    ):
        """
        The `readMDSummary` method is responsible for reading the machine description summary and retrieving
        data for the specified IDS names.
        """

        # if provided just single string then convert to list with single string
        if isinstance(ids_names, str):
            ids_names = [ids_names]
        # lower case provided ids names
        ids_names = list(map(lambda x: x.lower(), ids_names))
        pulses_data: typing.dict[str, typing.dict] = {}
        for pulse, config in self.md_summary_yaml.items():
            if ids_names:
                if config["ids"] not in ids_names:
                    continue

            if add_obsoelete is False:
                if config["status"] == "obsolete":
                    continue

            pulses_data[pulse] = {}
            pulses_data[pulse]["data"] = None
            if check_validity:
                self.md_args.pulse, self.md_args.run = pulse.split("/")
                self.md_args.pulse, self.md_args.run = int(self.md_args.pulse), int(self.md_args.run)
                self.md_args.uri = (
                    f"imas:mdsplus?user={self.md_args.user};pulse={self.md_args.pulse};"
                    f"run={self.md_args.run};database={self.md_args.database};version={self.md_args.version}"
                )
                md_connection = DBMaster.get_connection(self.md_args)
                if md_connection is not None:
                    ids_data = md_connection.get(config["ids"])
                    if ids_data is not None:
                        pulses_data[pulse]["data"]
                    md_connection.close()

            pulses_data[pulse]["config"] = config
        return pulses_data

    def get_pandas_data_frame(self):
        """
        The function `getPandasDataFrame` converts a dictionary into a pandas DataFrame.

        Returns:
          a pandas DataFrame object.
        """
        import pandas as pd

        data_list = [{"id": key, **value} for key, value in self.md_summary_yaml.items()]
        df = pd.DataFrame(data_list)
        return df

    def get_status(self, pulse: int, run: int):
        """
        The function `getStatus` takes in two parameters, `pulse` and `run`, and returns the value of the
        key "status" from the `yaml` object dictionary using the `pulse` and `run` as keys.

        Args:
            pulse (int): The "pulse" parameter represents the number of pulses taken.
            run (int): The "run" parameter represents the number of runs in a particular pulse.

        Returns:
            The method `getStatus` returns the value of `"status"` if `yaml` object is not `None`,
            otherwise it returns `None`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if self.md_summary_yaml:
            return self.md_summary_yaml[pulserun]["status"]
        else:
            return None

    def get_reason_for_replacement(self, pulse: int, run: int):
        """
        The function `getReasonForReplacement` takes in two parameters, `pulse` and `run`, and returns
        the value of the key "reason_for_replacement" from the `yaml` object dictionary using the `pulse`
        and `run` as keys.

        Args:
            pulse (int): The "pulse" parameter represents the number of pulses taken.
            run (int): The "run" parameter represents the number of runs in a particular pulse.

        Returns:
            The method `getReasonForReplacement` returns the value of `"reason_for_replacement"` if `yaml`
            object is not `None`, otherwise it returns `None`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if self.md_summary_yaml:
            return self.md_summary_yaml[pulserun]["reason_for_replacement"]
        else:
            return None

    def get_replaced_by(self, pulse: int, run: int):
        """
        The function `getReplacedBy` takes in two parameters, `pulse` and `run`, and returns the value of
        the key "replaced_by" from the `yaml` object dictionary using the `pulse` and `run` as keys.

        Args:
            pulse (int): The "pulse" parameter represents the number of pulses taken.
            run (int): The "run" parameter represents the number of runs in a particular pulse.

        Returns:
            The method `getReplacedBy` returns the value of `"replaced_by"` if `yaml` object is not `None`,
            otherwise it returns `None`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if self.md_summary_yaml:
            return self.md_summary_yaml[pulserun]["replaced_by"]
        else:
            return None

    def get_replaces(self, pulse: int, run: int):
        """
        The function `getReplaces` takes in two parameters, `pulse` and `run`, and returns the value of the key
        "replaces" from the `yaml` object dictionary using the `pulse` and `run` as keys.

        Args:
            pulse (int): The "pulse" parameter represents the number of pulses taken.
            run (int): The "run" parameter represents the number of runs in a particular pulse.

        Returns:
            The method `getReplaces` returns the value of `"replaces"` if `yaml` object is not `None`, otherwise
            it returns `None`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if self.md_summary_yaml:
            return self.md_summary_yaml[pulserun]["replaces"]
        else:
            return None

    def get_children(self, pulse: int, run: int, dict_to_fill={}):
        """
        The function `getChildren` recursively retrieves information about replaced pulses and runs from a
        dictionary and stores it in a new dictionary.

        Args:
            pulse (int): The "pulse" parameter is an integer that represents a pulse number.
            run (int): The `run` parameter in the `getChildren` method represents the run number.
            dictToFill: The `dictToFill` parameter is a dictionary that is used to store the information about
            the children of a given pulse and run. It is initially an empty dictionary and is passed as an
            argument to the function to accumulate the information about the children.

        Returns:
            a dictionary `dictToFill` that contains information about the children of a given pulse and run.
            The dictionary has keys "pulse", "run", "status", and "reason_for_replacement", and the corresponding
            values are lists that store the information for each child.
        """
        replaced_by = self.get_replaced_by(pulse, run)
        if replaced_by is not None:
            string_list = re.findall(r"\d+", replaced_by)
            pulsec = string_list[0]
            runc = string_list[1]
            pulserunc = pulsec + "/" + runc
            if "pulse" not in dict_to_fill.keys():
                dict_to_fill["pulse"] = []
            if "run" not in dict_to_fill.keys():
                dict_to_fill["run"] = []
            if "status" not in dict_to_fill.keys():
                dict_to_fill["status"] = []
            if "reason_for_replacement" not in dict_to_fill.keys():
                dict_to_fill["reason_for_replacement"] = []
            dict_to_fill["pulse"].append(pulsec)
            dict_to_fill["run"].append(runc)
            dict_to_fill["status"].append(self.md_summary_yaml[pulserunc]["status"])
            dict_to_fill["reason_for_replacement"].append(self.md_summary_yaml[pulserunc]["reason_for_replacement"])
            dict_to_fill = self.get_children(int(pulsec), int(runc), dict_to_fill)
        return dict_to_fill

    def get_parents(self, pulse: int, run: int, dict_to_fill={}):
        """
        The `getParents` function recursively retrieves the parent information for a given pulse and run, populating
        a dictionary with the parent pulse, parent run, status, and reason for replacement.

        Args:
            pulse (int): The `pulse` parameter is an integer that represents a pulse number.
            run (int): The `run` parameter is an integer that represents the run number.
            dictToFill: The `dictToFill` parameter is a dictionary that is used to store the information about the
            parents of a given pulse and run. It is initially an empty dictionary and is passed as an argument to
            the `getParents` function. The function fills this dictionary with the parent information and returns it.

        Returns:
            a dictionary `dictToFill` that contains information about the parents of a given pulse and run.
        """
        replaces = self.get_replaces(pulse, run)
        if replaces is not None:
            string_list = re.findall(r"\d+", replaces)
            pulsep = string_list[0]
            runp = string_list[1]
            pulserunp = pulsep + "/" + runp
            if "pulse" not in dict_to_fill.keys():
                dict_to_fill["pulse"] = []
            if "run" not in dict_to_fill.keys():
                dict_to_fill["run"] = []
            if "status" not in dict_to_fill.keys():
                dict_to_fill["status"] = []
            if "reason_for_replacement" not in dict_to_fill.keys():
                dict_to_fill["reason_for_replacement"] = []

            dict_to_fill["pulse"].insert(0, pulsep)  # Order to be reversed for parents
            dict_to_fill["run"].insert(0, runp)
            dict_to_fill["status"].insert(0, self.md_summary_yaml[pulserunp]["status"])
            dict_to_fill["reason_for_replacement"].insert(0, self.md_summary_yaml[pulserunp]["reason_for_replacement"])
            dict_to_fill = self.get_parents(int(pulsep), int(runp), dict_to_fill)
        return dict_to_fill

    def get_family(self, pulse: int, run: int):
        """
        The function "getFamily" returns a dictionary containing the parents and children of a given pulse and run.

        Args:
            pulse (int): The "pulse" parameter represents the pulse number
            run (int): The "run" parameter is an integer that represents the run number.

        Returns:
            a dictionary called `familyDict` which contains two keys: "parents" and "children". The values associated
            with these keys are the results of calling the `getParents` and `getChildren` methods with the given
            `pulse` and `run` parameters.
        """
        family_dict = {}
        family_dict["parents"] = self.get_parents(pulse, run)
        family_dict["children"] = self.get_children(pulse, run)
        return family_dict

    def check_if_exist(self, pulse: int, run: int):
        """
        The function checks if a given pulse and run combination exists in a yaml dictionary.

        Args:
            pulse (int): The "pulse" parameter is an integer representing the number.
            run (int): The parameter "run" is an integer representing the number.

        Returns:
            a boolean value. If the `pulserun` key is present in the `yaml` object dictionary, it will  return
            `True`. Otherwise, it will return `False`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if pulserun not in self.md_summary_yaml.keys():
            return False
        return True
