import logging
from os import getenv, path
from xml.etree import ElementTree as ET

logger = logging.getLogger("module")


class DDHelper(object):
    # root = None
    # version = None
    # cocos = None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DDHelper, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """Simple class which allows to query meta-data from the definition of IDSs as expressed in IDSDef.xml."""
        self.ids_def = getenv("IMAS_PREFIX") + "/include/IDSDef.xml"
        self.root = None
        if path.isfile(self.ids_def):
            self.root = ET.parse(self.ids_def).getroot()
            self.version = self.root.findtext("./version", default="N/A")
            self.cocos = self.root.findtext("./cocos", default="N/A")
        else:
            logger.error(
                "Error while trying to access IDSDef.xml, make sure you've loaded IMAS module"
            )
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

    def getField(self, struct, field):
        """Recursive function which returns the node corresponding to a given field which is a descendant of struct."""
        elt = struct.find('./field[@name="' + field[0] + '"]')
        if elt == None:
            raise Exception("Element '" + field[0] + "' not found")
        if len(field) > 1:
            f = self.getField(elt, field[1:])
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
        if ids == None:
            raise ValueError(
                f"Error getting the IDS, please check that '{ids}' corresponds to a valid IDS name"
            )

        if path != None:
            fields = path.split("/")

            try:
                f = self.getField(ids, fields)
            except Exception as exc:
                raise ValueError("Error while accessing {path}: {str(exc)}")
        else:
            f = ids

        return f.attrib

    # def __init__(self):
    #     # parse the XML def
    #     try:
    #         imaspref = os.environ["IMAS_PREFIX"]
    #         tree = ET.parse(imaspref + "/include/IDSDef.xml")
    #         self.root = tree.getroot()
    #         self.version = self.root.findtext("./version", default="N/A")
    #         self.cocos = self.root.findtext("./cocos", default="N/A")
    #     except:
    #         print(
    #             "Error while trying to access IDSDef.xml, make sure you've loaded IMAS module",
    #             file=sys.stderr,
    #         )
