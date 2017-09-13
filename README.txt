----------------------------------------------------------------------------------------------------------------
 scenario_summary
------------------

usage: scenario_summary [-h] [-f FOLDER] [-c CHOICE]

---- Script to list available scenarios in a specific folder ----

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        folder where to search for scenarios (recursive)
  -c CHOICE, --choice CHOICE
                        list of variables to display, e.g.: "'shot','run','plasma_current','magnetic_field'"
                        ...available among following variables:
                                'shot', 'run', 'type', 'workflow', 'machine',
                                'plasma_current', 'magnetic_field', 'main_species',
                                'line_averaged_density', 'idslist'

EXAMPLE:
scenario_summary -c "'shot','run','workflow'"

----------------------------------------------------------------------------------------------------------------
create_yaml  (needs ids_content, described below)
------------

usage: create_yaml [-h] -u USER -t TOKAMAKNAME -s SHOT -r RUN

---- Auto-generated yaml scenario file (!!! STILL TO BE COMPLETED BY HAND !!!)

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  username of the DB where the datafile is located
  -t TOKAMAKNAME, --tokamakname TOKAMAKNAME
                        tokamak name of the DB where the datafile is located
  -s SHOT, --shot SHOT  shot number
  -r RUN, --run RUN     run number

EXAMPLE:
create_yaml -u schneim -t test -s 33 -r 1
----> ids_330001.yaml created.

----------------------------------------------------------------------------------------------------------------
 ids_content
--------------

usage: ids_content [-h] -u USER -t TOKAMAKNAME -s SHOT -r RUN

---- List ids content for yaml files aimed at describing a scenario ----

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  username of the DB where the datafile is located
  -t TOKAMAKNAME, --tokamakname TOKAMAKNAME
                        tokamak name of the DB where the datafile is located
  -s SHOT, --shot SHOT  shot number
  -r RUN, --run RUN     run number

EXAMPLE:
ids_content  -u schneim -t test -s 33 -r 1
