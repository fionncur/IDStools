idslist
========

*idslist* is a utility that, as the name implies, shows list of all idses along with count of time slices. 
It also shows timestamps of slices. You can customize the output by choosing to display full array values or 
generate output in YAML format.


Syntax idslist
~~~~~~~~~~~~~~~

    .. code-block:: bash   
          
        $ idslist -h
        Install tqdm to enable progress bar
        usage: idslist [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-f] [-y]

        ---- List available IDSes in the pulse

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
        -s SHOT, --shot SHOT  Shot number
        -r RUN, --run RUN     Run number
        -f, --fullarray       Show full time array values
        -y, --yaml-format     List ids content for yaml files aimed at describing a scenario



Example idslist
~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ idslist -s 134174 -r 117
        Install tqdm to enable progress bar
        core_profiles  : 106   slices: [10.6 10.6 10.6 ... 75.  75.  75. ]
        core_sources   : 106   slices: [10.6 10.6 10.6 ... 75.  75.  75. ]
        core_transport : 106   slices: [10.6 10.6 10.6 ... 75.  75.  75. ]
        edge_profiles  : 650   slices: [10.1 10.2 10.3 ... 74.8 74.9 75. ]
        edge_sources   : 650   slices: [10.1 10.2 10.3 ... 74.8 74.9 75. ]
        edge_transport : 650   slices: [10.1 10.2 10.3 ... 74.8 74.9 75. ]
        equilibrium    : 106   slices: [  1.2    1.5    1.8  ... 146.44 147.94 149.44]
        summary        : 106   slices: [10.3 10.3 10.3 ... 75.  75.  75. ]

