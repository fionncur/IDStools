###################
 validate_db_entry
###################

Validation Tool for ITER Scenario DB

**************************
 Syntax validate_db_entry
**************************

.. code-block:: bash

    $ validate_db_entry -h
    usage: validate_db_entry [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [--shot SHOT] [--run RUN]
                            [--log {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--output OUTPUT] [--path PATH [PATH ...]]

    Validation Tool for ITER Scenario DB
    -----------------------------------------------------------
    Usage:
        0) Load IMAS
        $ module load IMAS

        1) Validate all pulses in IMAS database against default schemas with output file
        $ validate_db_entry -o output.log

        2) Check the validity of all pulses in IMAS database against schemas
        $ validate_db_entry -p /path/to/schema1.yaml /path/to/schema2.yaml

        3) Validate all pulses in local database to default schemas
        $ validate_db_entry -u username -d database

        4) Validate one pulse in IMAS database to schemas in the directory
        $ validate_db_entry -s 131024 -r 40 -p /path/to/schema/dir

        5) Validate all pulses having the shot number specified
        $ validate_db_entry -s 131024 -p /path/to/schema/dir

    optional arguments:
    -h, --help            show this help message and exit
    -u USER, --user_or_path USER
                            user (default=public)
    --database DATABASE, -d DATABASE
                            database name (default=ITER)
    --backend BACKEND, -b BACKEND
                            backend format (default=MDSPLUS)
    --version VERSION, -v VERSION
                            data version (default=3)
    --shot SHOT, -s SHOT  Shot number
    --run RUN, -r RUN     Run number
    --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                            Logging level, default=INFO
    --output OUTPUT, -o OUTPUT
                            file name of IDS validation, no file output unless given
    --path PATH [PATH ...], -p PATH [PATH ...]
                            list of schema file and/or directory paths from which schema files are recursively loaded


