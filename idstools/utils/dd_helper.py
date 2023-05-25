from os import getenv, path

from xml.etree import ElementTree as ET


class DDHelper(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DDHelper, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.ids_def = getenv("IMAS_PREFIX") + "/include/IDSDef.xml"
        self.root = None
        if path.isfile(self.ids_def):
            self.root = ET.parse(self.ids_def).getroot()
        else:
            raise FileNotFoundError(f"file not found:{self.ids_def}")

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
