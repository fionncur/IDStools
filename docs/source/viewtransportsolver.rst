viewtransportsolver
===================

*viewtransportsolver* Displays the Core plasma transport of particles, energy, momentum and poloidal flux. 


Syntax viewtransportsolver
~~~~~~~~~~~~~~~~~~

    .. code-block:: bash   

        $ viewtransportsolver -h
        usage: viewtransportsolver [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-m {CLOSEST,PREVIOUS,LINEAR}] [-o OCCURRENCE] -s SHOT -r RUN [-t TIME]

        Check match between transport fluxes and a simple calculation

        optional arguments:
        -h, --help            show this help message and exit
        -u USER, --user_or_path USER
                                user            (default=public)
        --database DATABASE, -d DATABASE
                                database name   (default=ITER)
        --backend BACKEND, -b BACKEND
                                backend format  (default=MDSPLUS)
        --version VERSION, -v VERSION
                                data version    (default=3)
        -m {CLOSEST,PREVIOUS,LINEAR}, --slicingmethod {CLOSEST,PREVIOUS,LINEAR}
                                Slicing method  (default=CLOSEST)
        -o OCCURRENCE, --occurrence OCCURRENCE
                                occurrence
        -s SHOT, --shot SHOT  Shot number
        -r RUN, --run RUN     Run number
        -t TIME, --time TIME  Time


Example 
~~~~~~~

    .. code-block:: bash

        $ viewtransportsolver -s 134000 -r 40
