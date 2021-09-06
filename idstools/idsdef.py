#!/usr/bin/env python
import xml.etree.ElementTree as ET
import os

class IDSDef:
    """Simple class which allows to query meta-data from the definition of IDSs as expressed in IDSDef.xml.
    """
    
    root = None
    version = None
    
    def __init__(self):
        # parse the XML def
        try:
            imaspref = os.environ['IMAS_PREFIX']
            tree = ET.parse(imaspref+'/include/IDSDef.xml')
            self.root = tree.getroot()
            self.version = self.root.find('./version').text
        except:
            print("Error while trying to access IDSDef.xml, make sure you've loaded IMAS module",file=sys.stderr)

            
    def getField(self,struct,field):
        """Recursive function which returns the node corresponding to a given field which is a descendant of struct.
        """
        elt = struct.find('./field[@name="'+field[0]+'"]')
        if elt==None:
            raise Exception("Element '"+field[0]+"' not found")
        if len(field)>1:
            f = self.getField(elt,field[1:])
        else:
            # specific generic node for which the useful doc is from the parent
            if field[0]!='value':
                f = elt
            else:
                f = struct
        return f

    
    def query(self,ids, path=None):
        """Returns attributes of the selected ids/path node as a dictionary.
        """
        ids = self.root.find(f"./IDS[@name='{ids}']")
        if ids==None:
            raise ValueError(f"Error getting the IDS, please check that '{ids}' corresponds to a valid IDS name")

        if path!=None:
            fields = path.split('/')

            try:
                f = self.getField(ids,fields)
            except Exception as exc:
                raise ValueError("Error while accessing {path}: {str(exc)}")
        else:
            f = ids

        return f.attrib
        

    def version():
        """Returns the current Data-Dictionary version.
        """
        

if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='Query the IDS XML Definition for documentation')
    parser.add_argument('ids',type=str,help='IDS name')
    parser.add_argument('path',type=str,nargs='?',default=None,help='Path for field of interest within the IDS')
    opt = parser.add_mutually_exclusive_group()
    opt.add_argument('-a','--all',action='store_true',help='Print all attributes')
    opt.add_argument('-s','--select',type=str,default='documentation',
                        help='Select attribute to be printed \t(default=%(default)s)')
    parser.add_argument('-v','--version',action='store_true',help='Print Data Dictionary version')
    args = parser.parse_args()

    try:
        dd = IDSDef()
        f = dd.query(args.ids, args.path)
    except ValueError as ve:
        print(f"{ve}",file=sys.stderr)

    if args.version:
        print(f"This is Data Dictionary version = {dd.version}")
        
    if args.all:
        for a in f.keys():
            print(a+': '+f[a])
    else:
        print(f[args.select])


    
