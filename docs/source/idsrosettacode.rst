idsrosettacode
=======

*idsrosettacode*  retrieves the size of IDS objects from a database entry and shows IDS size in bytes and the time taken to read each object. 
It also shows total size of all IDS objects in the data entry. It shows total time taken to read all objects from the data entry. 
It is helpful for performance check of ids objects.


Syntax idsrosettacode
~~~~~~~~~~~~~~

    .. code-block:: bash     

        $ idsrosettacode -h
        usage: idsrosettacode [-h] [-i INPUTCSV] [-m MAPPING] [--varCol VARCOL] [--pathCol PATHCOL] [--traCol TRACOL] [--timeloc TIMELOC] [-b BACKEND] [-d DATABASE]
                              [--dbtype DBTYPE] [-r ROW] [-v] [--debug]

        This script applies mapping of a non-IDS database content (e.g. ITPA DBs) into IDS rules.

        optional arguments:
          -h, --help            show this help message and exit
          -i INPUTCSV, --inputCSV INPUTCSV
                                Path to csv file containing the external database content (default=HDB5.2.3.csv, the H-mode DB will be downloaded from
                                https://osf.io/zhwa3/ automatically if not present)
          -m MAPPING, --mapping MAPPING
                                Path to csv-formatted mapping file (default=/home/ITER/sawantp1/git/idstools/idstools/mappings/h-mode-db-mapping.csv)
          --varCol VARCOL       Name of the column of the mapping file listing all DB variables (default=DB_VARIABLE)
          --pathCol PATHCOL     Name of the column of the mapping file listing the paths to store all DB variables into IDS fields (default=IDS_PATH)
          --traCol TRACOL       Name of the column of the mapping file listing the transformations to be done on DB variables (default = summary) (default=TRANSFORMATION)
          --timeloc TIMELOC     Name of the IDS from which the time will be extracted to populate time-empty IDSs (default=summary
          -b BACKEND, --backend BACKEND
                                backend format (default=ASCII)
          -d DATABASE, --database DATABASE
                                target IMAS database name (default=test)
          --dbtype DBTYPE       Type of database (default = H-MODE) (default=H-MODE)
          -r ROW, --row ROW     Stores data for the given row/entry of the input database (processes all rows otherwise)
          -v, --verbose         Run in verbose mode
          --debug               Run in debug mode


Example idsrosettacode
~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ idsrosettacode 






