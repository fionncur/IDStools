import argparse
import copy
import logging
import os
import re
import typing

try:
    import imaspy as imas
except ImportError:
    import imas
from yaml import YAMLError, safe_load

from idstools.database import DBMaster
from idstools.utils.idshelper import (
    get_available_ids_and_occurrences,
    parse_uri,
)

logger = logging.getLogger(f"module.{__name__}")
MD_IDSES = "tf,wall,pf_passive,pf_active,magnetics"


class MachineDescription:

    def __init__(self, summary_yaml_file: str = "") -> None:
        self.md_summary_yaml = {}
        if not summary_yaml_file:
            publichome = os.getenv("IMAS_HOME", default="")

            _md_summary_path = os.path.join(publichome, r"shared/imasdb/ITER_MD/3/md_summary.yaml")

        else:
            _md_summary_path = summary_yaml_file

        with open(_md_summary_path, "r") as stream:
            try:
                self.md_summary_yaml = safe_load(stream)
            except YAMLError as exc:
                print(exc)

    def get_latest_ids_data(self, ids_name: str, backend="MDSPLUS", user="public", database="ITER_MD", version=3):
        md_ids_dict = self.get_md_summary(ids_name)
        ids_data = None
        config = None
        import argparse

        md_args = argparse.Namespace()
        md_args.backend = backend
        md_args.pulse = 0
        md_args.run = 0
        md_args.user = user
        md_args.database = database
        md_args.version = version
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
        ids_data = {}
        for ids_name in md_ids_list:
            ids_data[ids_name] = self.get_md_data_by_ids(ids_name)
        return ids_data

    def get_md_data_by_ids(self, ids_name: str):
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
        The function `get_pandas_data_frame` converts a dictionary into a pandas DataFrame.

        Returns:
          a pandas DataFrame object.
        """
        import pandas as pd

        data_list = [{"id": key, **value} for key, value in self.md_summary_yaml.items()]
        df = pd.DataFrame(data_list)
        return df

    def get_status(self, pulse: int, run: int):
        """
        The function `get_status` takes in two parameters, `pulse` and `run`, and returns the value of the
        key "status" from the `yaml` object dictionary using the `pulse` and `run` as keys.

        Args:
            pulse (int): The "pulse" parameter represents the number of pulses taken.
            run (int): The "run" parameter represents the number of runs in a particular pulse.

        Returns:
            The method `get_status` returns the value of `"status"` if `yaml` object is not `None`,
            otherwise it returns `None`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if self.md_summary_yaml:
            return self.md_summary_yaml[pulserun]["status"]
        else:
            return None

    def get_reason_for_replacement(self, pulse: int, run: int):
        """
        The function `get_reason_for_replacement` takes in two parameters, `pulse` and `run`, and returns
        the value of the key "reason_for_replacement" from the `yaml` object dictionary using the `pulse`
        and `run` as keys.

        Args:
            pulse (int): The "pulse" parameter represents the number of pulses taken.
            run (int): The "run" parameter represents the number of runs in a particular pulse.

        Returns:
            The method `get_reason_for_replacement` returns the value of `"reason_for_replacement"` if `yaml`
            object is not `None`, otherwise it returns `None`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if self.md_summary_yaml:
            return self.md_summary_yaml[pulserun]["reason_for_replacement"]
        else:
            return None

    def get_replaced_by(self, pulse: int, run: int):
        """
        The function `get_replaced_by` takes in two parameters, `pulse` and `run`, and returns the value of
        the key "replaced_by" from the `yaml` object dictionary using the `pulse` and `run` as keys.

        Args:
            pulse (int): The "pulse" parameter represents the number of pulses taken.
            run (int): The "run" parameter represents the number of runs in a particular pulse.

        Returns:
            The method `get_replaced_by` returns the value of `"replaced_by"` if `yaml` object is not `None`,
            otherwise it returns `None`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if self.md_summary_yaml:
            return self.md_summary_yaml[pulserun]["replaced_by"]
        else:
            return None

    def get_replaces(self, pulse: int, run: int):
        """
        The function `get_replaces` takes in two parameters, `pulse` and `run`, and returns the value of the key
        "replaces" from the `yaml` object dictionary using the `pulse` and `run` as keys.

        Args:
            pulse (int): The "pulse" parameter represents the number of pulses taken.
            run (int): The "run" parameter represents the number of runs in a particular pulse.

        Returns:
            The method `get_replaces` returns the value of `"replaces"` if `yaml` object is not `None`, otherwise
            it returns `None`.
        """
        pulserun = str(pulse) + r"/" + str(run)
        if self.md_summary_yaml:
            return self.md_summary_yaml[pulserun]["replaces"]
        else:
            return None

    def get_children(self, pulse: int, run: int, dict_to_fill={}):
        """
        The function `get_children` recursively retrieves information about replaced pulses and runs from a
        dictionary and stores it in a new dictionary.

        Args:
            pulse (int): The "pulse" parameter is an integer that represents a pulse number.
            run (int): The `run` parameter in the `get_children` method represents the run number.
            dict_to_fill: The `dict_to_fill` parameter is a dictionary that is used to store the information about
                the children of a given pulse and run. It is initially an empty dictionary and is passed as an
                argument to the function to accumulate the information about the children.

        Returns:
            a dictionary `dict_to_fill` that contains information about the children of a given pulse and run.
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
        The `get_parents` function recursively retrieves the parent information for a given pulse and run, populating
        a dictionary with the parent pulse, parent run, status, and reason for replacement.

        Args:
            pulse (int): The `pulse` parameter is an integer that represents a pulse number.
            run (int): The `run` parameter is an integer that represents the run number.
            dict_to_fill: The `dictToFill` parameter is a dictionary that is used to store the information about the
                parents of a given pulse and run. It is initially an empty dictionary and is passed as an argument to
                the `get_parents` function. The function fills this dictionary with the parent information
                and returns it.

        Returns:
            a dictionary `dict_to_fill` that contains information about the parents of a given pulse and run.
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
        The function "get_family" returns a dictionary containing the parents and children of a given pulse and run.

        Args:
            pulse (int): The "pulse" parameter represents the pulse number
            run (int): The "run" parameter is an integer that represents the run number.

        Returns:
            a dictionary called `famly_dict` which contains two keys: "parents" and "children". The values associated
            with these keys are the results of calling the `get_parents` and `get_children` methods with the given
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


def get_md_data(uri_list, dd_update=False, idses=MD_IDSES):
    ids_data = {}
    for mduri in uri_list:
        mdargs = argparse.Namespace()

        result = parse_uri(mduri)

        # specified things in uri
        _md_uri = result["uri_part"]
        _ids_occurrence = result["occurrence"]
        _ids_name = result["ids_name"]
        _ids_field = result["ids_path"]
        _ids_names = _ids_name
        mdargs.uri = _md_uri
        connection = DBMaster.get_connection(mdargs)
        if connection:
            all_idses_list = get_available_ids_and_occurrences(connection, None)
            if _ids_names == "":
                _ids_names = idses

            for _ids_name in _ids_names.split(","):
                _ids_name = _ids_name.strip()
                if _ids_name == "":
                    continue
                if _ids_name not in idses:
                    continue
                ids_found = False
                if _ids_occurrence is None:
                    _ids_occurrences = [value for term, value in all_idses_list if _ids_name in term]
                else:
                    _ids_occurrences = [_ids_occurrence]
                for occ in _ids_occurrences:
                    if dd_update:
                        _ids_data = imas.convert_ids(
                            connection.get(_ids_name, autoconvert=False, occurrence=occ), connection.factory.version
                        )
                    else:
                        _ids_data = connection.get(_ids_name, autoconvert=False, occurrence=occ)
                    data = {}
                    if _ids_data is not None:
                        ids_found = True
                        (
                            data["idsData"],
                            data["yamlConfig"],
                            data["connectionArgs"],
                            data["idsname"],
                            data["idsfield"],
                            data["idsocc"],
                        ) = (_ids_data, None, mdargs, _ids_name, _ids_field, occ)
                        ids_data[f"{_md_uri}#{_ids_name}:{occ}/{_ids_field}"] = data
                if not ids_found:
                    logger.info(f"Could not find {_ids_name} in the given data entry")
            connection.close()
    return ids_data
