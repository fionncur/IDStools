import argparse
import os,sys
from imas import imasdef

# default parent parser for all idstools scripts
imas_parser = argparse.ArgumentParser(add_help=False)
imas_parser.add_argument("-u", "--user", 
                         type=str, default=os.environ["USER"],
                         help="user \t\t(default=%(default)s)")
db_group = imas_parser.add_mutually_exclusive_group()
db_group.add_argument("--database", "-d", 
                   type=str, default="iter",
                   help="database name \t(default=%(default)s)")
db_group.add_argument("--tokamak", "-t", 
                   type=str, dest="database", default=os.getenv("TOKAMAKNAME"),
                   help="tokamak name \t[deprecated: use -d instead]")
imas_parser.add_argument("--backend", "-b", 
                         type=str, default="MDSPLUS", 
                         help="backend format \t(default=%(default)s)")
imas_parser.add_argument("--version", "-v", 
                         type=str, default='3', 
                         help="data version \t(default=%(default)s)")


def get_backend_id(name):
    return getattr(imasdef,name+"_BACKEND")



