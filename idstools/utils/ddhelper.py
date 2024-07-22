from os import path
from xml.etree import ElementTree as ET
import imas
import logging
import os

logger = logging.getLogger("module")


class d_d_helper(object):
    # root = None
    # version = None
    # cocos = None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(d_d_helper, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """Simple class which allows to query meta-data from the definition of IDSs as expressed in IDSDef.xml."""
        self.ids_def = d_d_helper.get_i_d_s_def_path()
        self.root = None
        if path.isfile(self.ids_def):
            self.root = e_t.parse(self.ids_def).getroot()
            self.version = self.root.findtext("./version", default="N/A")
            self.cocos = self.root.findtext("./cocos", default="N/A")
        else:
            logger.error("Error while trying to access IDSDef.xml, make sure you've loaded IMAS module")
            raise FileNotFoundError(f"file not found:{self.ids_def}")

    @classmethod
    def get_i_d_s_def_path(cls):
        # Find and parse XML definitions
        idsdef_path = ""
        if not idsdef_path:
            imas_fpath = os.path.dirname(imas.__file__)
            # Newer approach : IMAS/<VERSION>/lib/python3.8/site-packages/data_dictionary/idsinfo.py
            _idsdef_path = os.path.join(imas_fpath, r"../../../../include/IDSDef.xml")
            if os.path.isfile(_idsdef_path):
                idsdef_path = os.path.abspath(_idsdef_path)
            else:

                # Legacy approach : IMAS/<VERSION>/python/lib/data_dictionary/idsino.py
                _idsdef_path = os.path.join(imas_fpath, r"../../../include/IDSDef.xml")
                if os.path.isfile(_idsdef_path):
                    idsdef_path = os.path.abspath(_idsdef_path)

        # Search using IDSDEF_PATH env variable
        if not idsdef_path:
            if "IDSDEF_PATH" in os.environ:
                _idsdef_path = os.environ["IDSDEF_PATH"]
                if os.path.isfile(_idsdef_path):
                    idsdef_path = _idsdef_path

        # Search using IMAS_PREFIX env variable
        if not idsdef_path:
            if "IMAS_PREFIX" in os.environ:
                _idsdef_path = os.path.join(os.environ["IMAS_PREFIX"], r"include/IDSDef.xml")
                if os.path.isfile(_idsdef_path):
                    idsdef_path = _idsdef_path

        if not idsdef_path:
            print(
                "Error accessing IDSDef.xml.  Make sure its location is defined in your environment,"
                "e.g. by loading an IMAS module."
            )
        return idsdef_path

    def get_coordinate(self, idsname="", field_path=""):
        if self.root is None:
            return None
        if field_path == "":
            return None
        for ids in self.root.findall("IDS"):
            if ids.attrib["name"] != idsname.lower():
                continue
            for field in ids.iter("field"):
                if field.attrib["path"] != field_path:
                    continue
                if "timebasepath" in field.attrib.keys():
                    return field.attrib["timebasepath"]
                if "coordinate1" in field.attrib.keys():
                    return field.attrib["coordinate1"]

    def get_field(self, struct, field):
        """Recursive function which returns the node corresponding to a given field which is a descendant of struct."""
        elt = struct.find('./field[@name="' + field[0] + '"]')
        if elt is None:
            raise Exception("Element '" + field[0] + "' not found")
        if len(field) > 1:
            f = self.get_field(elt, field[1:])
        else:
            # specific generic node for which the useful doc is from the parent
            if field[0] != "value":
                f = elt
            else:
                f = struct
        return f

    def query(self, ids, path=None):
        """Returns attributes of the selected ids/path node as a dictionary."""
        ids = self.root.find(f"./IDS[@name='{ids}']")
        if ids is None:
            raise ValueError(f"Error getting the IDS, please check that '{ids}' corresponds to a valid IDS name")

        if path is not None:
            fields = path.split("/")

            try:
                f = self.get_field(ids, fields)
            except Exception as e:
                logger.debug(f"{e}")
                raise ValueError(f"Error while accessing {path}: {str(e)}")
        else:
            f = ids

        return f.attrib
