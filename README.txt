----------------------------------------------------------------------------------------------------------------
 scenario_summary
------------------

usage: scenario_summary [-h] [-f FOLDER] [-s SELECTION] [-c CHOICE]

---- Script to list available scenarios in a specific folder ----

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        folder where to search for scenarios (recursive)
  -s SELECTION, --selection SELECTION
                        list of fields to filter: e.g. He4,2.65
                        ----> Select only scenarios filling these criteria
  -c CHOICE, --choice CHOICE
                        list of variables to display, e.g.: shot,run,ip,b0
                        ... available among following variables:
                                shot     = shot number
                                run      = run number
                                type     = data type (experimental,predictive,interpretative)
                                workflow = suite of codes used to compte these data
                                machine  = tokamak name
                                ip       = plasma current
                                b0       = central magnetic field
                                species  = plasma main species
                                ne0      = central electron density
                                zeff     = central Zeff
                                p_hcd    = total H&CD power
                                p_ec     = EC power
                                p_ic     = IC power
                                p_nbi    = NBI power
                                p_lh     = LH power
                                idslist  = List of IDSs available in the datafile
                                location = Location of the full description file

----------------------------------------------------------------------------------------------------------------
create_db_entry  (needs ids_content, described below)
----------------

usage: create_db_entry [-h] -u USER -t TOKAMAKNAME -s SHOT -r RUN

---- Auto-generated yaml scenario file (!!! STILL TO BE COMPLETED BY HAND !!!)

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  username of the DB where the datafile is located
  -t TOKAMAKNAME, --tokamakname TOKAMAKNAME
                        tokamak name of the DB where the datafile is located
  -s SHOT, --shot SHOT  shot number
  -r RUN, --run RUN     run number

EXAMPLE:
create_db_entry -u schneim -t test -s 33 -r 1
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
