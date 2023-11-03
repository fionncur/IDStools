dbscraper
=========

The *dbscraper* script scrapes data from a particular IDS path for a specified series of pulses and displays the pulse along with the value.


dbscraper Syntax
~~~~~~~~~~~~~~~~
    .. code-block:: bash

        $ dbscraper -h

        Install tqdm to enable progress bar
        usage: dbscraper [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [--saveas SAVEAS]
                            [--status STATUS] [--list-count LIST_COUNT] [--verbose]
                            idspath

        Extracts given quantities from all data entries of a given database

        positional arguments:
        idspath               IDS path (starting with IDS name) to the desired data to be collected, e.g equilibrium/time

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
        --saveas SAVEAS       File in which to store the results of this query, in csv format
        --status STATUS       Will list only data entries with specified status (if such metadata is available)
        --list-count LIST_COUNT
                                number of entries user needs to display
        --verbose             Verbose mode

dbscraper Example
~~~~~~~~~~~~~~~~~
    .. code-block:: bash

        $ dbscraper "equilibrium/time_slice(0)/global_quantities/volume" --list-count 10 

        |    |   PULSE |   RUN |   VALUE |
        |---:|--------:|------:|--------:|
        |  0 |  121014 |    11 | 810.044 |
        |  1 |  101004 |    70 | 809.715 |
        |  2 |  123148 |     4 | nan     |
        |  3 |  110501 |     1 | 315.004 |
        |  4 |  123285 |     1 |  -9e+40 |
        |  5 |  123166 |     2 | nan     |
        |  6 |  123138 |     2 |  -9e+40 |
        |  7 |  121005 |    20 | 832.297 |
        |  8 |  134110 |    23 | 786.301 |
        |  9 |  112325 |     3 |  -9e+40 |


