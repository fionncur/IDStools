#!/usr/bin/env python
from os import getenv, path
from sys import exit
import re
import yaml
import argparse


IMAS_DIR = "IMAS_PREFIX"
FILE_IDSDef = getenv(IMAS_DIR) + "/include/IDSDef.xml"
TARGET_DATA_TYPE = "FLT_2D"
report_buf = {}


# ----------------------------------------------------------------------
import imas


class IMASData:
    """

    """

    def __init__(self, user_or_path, database, version, shot, run):
        self.user_or_path = user_or_path
        self.database = database
        self.version = version
        self.shot = shot
        self.run = run
        self.ids = {}

    def entry(self):
        return imas.ids(self.shot, self.run, 0, 0)

    def open(self):
        db = self.entry()
        db.open_env(self.user_or_path, self.database, self.version)
        if db.expIdx == -1:
            raise ValueError(
                "can not open user_or_path={}, database={}, shot={}, run={}".format(
                    self.user_or_path, self.database, self.shot, self.run
                )
            )
        else:
            return db

    def create(self):
        db = self.entry()
        db.create_env(self.user_or_path, self.database, self.version)
        if db.expIdx == -1:
            raise ValueError(
                "can not create user_or_path={}, database={}, shot={}, run={}".format(
                    self.user_or_path, self.database, self.shot, self.run
                )
            )
        else:
            return db

    def close(self, imas_entry):
        imas_entry.close()

    def get(self, occurrence):
        return self.ids.get(occurrence)


# ----------------------------------------------------------------------


def path2py(p, rm_last_bracket=False, header=False, idx=None):
    """
    Substitute IDS Path to Python Expression
    """
    ids_header = "ids."
    idx_header = "idx."

    result = re.search("^(\d)\.\.\.(\d)$", p)
    if result is not None:  # constant coordinate definition (e.g. 1...3)
        return "range(" + str(result.group(2)) + ")"

    else:  # other coordinate definition
        if rm_last_bracket == True:
            p = p[: p.rfind("(")]
        p = re.sub("\((\w+)\)", r"(" + idx_header + "\\1)", p)
        p = p.replace("/", ".")
        p = p.replace("(", "[")
        p = p.replace(")", "]")

        if idx is not None:
            keys = idx.data.keys()
            for k in keys:
                s = idx_header + k
                p = p.replace(s, str(eval(s)))

        if header:
            return ids_header + p
        else:
            return p


# ----------------------------------------------------------------------


class IdxDict(dict):
    """
    Class for DD Sub-Indices (e.g. itime, i1, ..., etc.)
    """

    def __init__(self, p):
        idict = []

        for m in re.finditer("\((\w+)\)", p):  # find subscripts and set as attribute
            it = m.group()[1:-1]
            idict.append("'" + it + "': None")  # initial value = None

        d = eval("{" + ",".join(idict) + "}")
        super(IdxDict, self).__setattr__("data", d)

    def __setattr__(self, k, v):
        self.data[k] = v

    def __getattr__(self, k):
        try:
            return self.data[k]
        except KeyError:
            raise AttributeError


# ----------------------------------------------------------------------


def test_FLT_2D(field, path_doc, ids, idx):
    """
    Validate Size & Shape of 2D Array wrt DD
    """
    global report_buf
    report = {}
    data_size = 0

    p = path2py(path_doc, header=True)
    c1 = path2py(field.get("coordinate1"), header=True)
    c2 = path2py(field.get("coordinate2"), header=True)

    try:
        data = eval(p)
        data_size = data.size
    except:
        print("Error on data {}, skipped".format(p))
        return

    if data_size > 0:  #   skip in case of data_size .le. 0

        # Replace time node with ids.time if homogeneous_time == 1
        homogeneous_time = ids.ids_properties.homogeneous_time
        if re.search("time$", c1) and (homogeneous_time == 1):
            c1 = "ids.time"
        if re.search("time$", c2) and (homogeneous_time == 1):
            c2 = "ids.time"

        l_dim1, l_dim2 = data.shape
        report["data_size"] = data_size
        report["data_shape"] = "({0},{1})".format(l_dim1, l_dim2)

        l_crd1 = l_crd2 = 0

        # Coordinate1
        report["coordinate1"] = path2py(field.get("coordinate1"), idx=idx)
        try:
            crd1 = eval(c1)
            l_crd1 = len(crd1)
        except:
            l_crd1 = -1

        report["coordinate1_len"] = l_crd1
        if (l_dim1 == l_crd1) and (l_crd1 > 0):
            report["coordinate1_result"] = True
        elif (report["coordinate1"] == "1...N") and (l_dim1>0):
            report["coordinate1_result"] = True
        else:
            report["coordinate1_result"] = False

        # Coordinate2
        report["coordinate2"] = path2py(field.get("coordinate2"), idx=idx)
        try:
            crd2 = eval(c2)
            l_crd2 = len(crd2)
        except:
            l_crd2 = -1

        report["coordinate2_len"] = l_crd2
        if (l_dim2 == l_crd2) and (l_crd2 > 0):
            report["coordinate2_result"] = True
        elif (report["coordinate2"] == "1...N") and (l_dim2>0):
            report["coordinate2_result"] = True
        else:
            report["coordinate2_result"] = False

        # Result
        report["remark"] = report["coordinate1_result"] and report["coordinate2_result"]
        report_buf.update({path2py(path_doc, idx=idx): report})


# ----------------------------------------------------------------------


def path_iterator(field, nodes, ids, idx=None, level=0):
    """
    Iterate Recursively over Sub-Indices of IDS Path (e.g. itime, i1, ..., etc.)
    """
    p = "/".join(nodes[: level + 1])
    if level < len(nodes) - 1:
        result = re.search("(\w+)(\(\w+\))$", p)

        # for dynamic array (e.g. path(itime)/to(i1)/array(i2))
        if result is not None:
            try:
                wk = eval(path2py(p, rm_last_bracket=True, header=True))
                for i in range(len(wk)):
                    idxname = result.group(2)[1:-1]
                    # increment the index in global scope
                    exec(idxname + "=" + str(i), idx.data)
                    path_iterator(field, nodes, ids, idx=idx, level=level + 1)
                    if not args.check_all:
                        break
            except:
                print("error for checking {}".format(p))
                pass

        # for node (e.g. path(itime)/to(i1)/node)
        else:
            path_iterator(field, nodes, ids, idx=idx, level=level + 1)

    else:
        test_FLT_2D(field, p, ids, idx)


# ----------------------------------------------------------------------


def ids_iterator(dd, db):
    """
    Iterate over the occurence of IDS and the number of 2D Array wrt DD
    """
    global report_buf
    idsname = dd.get("name")
    ids = eval("db." + idsname)
    maxoc = int(dd.get("maxoccur"))
    buf = {}

    for oc in range(maxoc):
        report_buf = {}
        idsprop = ids.partialGet("ids_properties", oc)
        homogeneous_time = idsprop.homogeneous_time
        dictw = {
            "homogeneous_time": homogeneous_time,
            "data_dictionary": idsprop.version_put.data_dictionary,
            "access_layer": idsprop.version_put.access_layer,
            "access_layer_language": idsprop.version_put.access_layer_language,
            "remark": None,
        }

        if homogeneous_time in [0, 1, 2]:
            if args.check_all:
                ids.get(oc)
            else:
                ids.getSlice(0, 1, oc)

            for field in dd.iter("field"):
                if field.get("data_type") == TARGET_DATA_TYPE:
                    path_doc = field.get("path_doc")
                    nodes = path_doc.split("/")
                    if not args.prop:
                        path_iterator(field, nodes, ids, idx=IdxDict(path_doc))

            dictw[TARGET_DATA_TYPE] = report_buf
            if bool(report_buf):
                dictw["remark"] = all(
                    {report_buf[x]["remark"] for x in report_buf.keys()}
                )
            buf.update({"occurence(" + str(oc) + ")": dictw})

    out = {idsname: {"maxoccur": maxoc, "result": buf}}
    return out


# ----------------------------------------------------------------------


def main():
    """
    IDS Data Validation Tool for Two Dimensional Array with respect to DD (IDSDef.xml)
    """
    from xml.etree import ElementTree as ET

    # Open the database
    try:
        db = IMASData(
            args.user_or_path,
            args.database,
            getenv("IMAS_VERSION")[0],
            args.shot,
            args.run,
        ).open()
    except:
        exit(
            "can not open user_or_path={}, database={}, shot={}, run={}".format(
                args.user_or_path, args.database, args.shot, args.run
            )
        )

    # Load IMAS-DD file
    if path.isfile(FILE_IDSDef):
        root = ET.parse(FILE_IDSDef).getroot()
    else:
        exit("file not found:{}".format(FILE_IDSDef))

    for dd in root:
        if dd.tag == "IDS":
            if (args.idslist is None) or (dd.get("name") in args.idslist):
                out = ids_iterator(dd, db)
                print(
                    yaml.dump(out, indent=4, default_flow_style=False, sort_keys=False)
                )

    db.close()


# ----------------------------------------------------------------------


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="IDS Data Validation Tool"
    )
    parser.add_argument(
        "-u",
        "--user_or_path",
        dest="user_or_path",
        help="User or path name of the DB where the data-entry is located",
        required=False,
        default="public",
    )
    parser.add_argument(
        "-d",
        "--database",
        dest="database",
        help="Database name of the DB where the data-entry is located",
        required=False,
        default="iter",
    )
    parser.add_argument(
        "-s", "--shot", dest="shot", help="Shot number", required=True, type=int
    )
    parser.add_argument(
        "-r", "--run", dest="run", help="Run number", required=True, type=int
    )
    parser.add_argument(
        "-i",
        "--idslist",
        dest="idslist",
        help="List of IDS names",
        required=False,
        nargs="*",
    )
    parser.add_argument(
        "-p",
        "--properties",
        action="store_true",
        dest="prop",
        help="Report only ids_properties",
        required=False,
    )
    parser.add_argument(
        "-a",
        "--check_all",
        action="store_true",
        dest="check_all",
        help="Check the whole elements in IDSs, otherwise check one slice as default",
        required=False,
    )
    args = parser.parse_args()
    main()
