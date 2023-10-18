viewidscompo
================

*viewidscompo* script gathers ion composition from core and edge profiles and print it on the screen

Syntax viewidscompo
~~~~~~~~~~~~~~~
.. code-block:: bash

    python viewidscompo.py -h
    usage: viewidscompo.py [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-i] [--debug]

    ---- Display the plasma composition from the core_profiles IDS

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
    -i, --info            Show information
    --debug               Show debugging

Example viewidscompo
~~~~~~~~~~~~~~~~
.. code-block:: bash

    $ viewidscompo -s 131047 -r 4
    !   No edge_profiles IDS in the data-entry.
    core +  edge  -
    ------------
    core_profiles
    ------------
    species:      H         D         T         He3       He4       Be        Ne
    a:            1.0       2.0       3.0       3.0       4.0       9.0       20.0
    z:            1.0       1.0       1.0       2.0       2.0       4.0       10.0
    n_over_ntot:  5.29e-06  0.460     0.493     7.01e-07  0.011     0.024     0.012
    n_over_ne:    4.45e-06  0.387     0.414     5.89e-07  9.58e-03  0.020     0.010
    n_over_n_maj: 1.07e-05  0.933     1.000     1.42e-06  0.023     0.048     0.024




