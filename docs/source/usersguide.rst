User's Guide
============
Following are the different command line tools available in the *IDSTools*.

idscompo
----------

*idscompo* script gathers ion composition from core and edge profiles and print it on the screen

Syntax
~~~~~~
.. code-block:: bash

    python idscompo.py -h
    usage: idscompo.py [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-i] [--debug]

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

Example
~~~~~~~
.. code-block:: bash

    $ idscompo -s 131047 -r 4
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


idsexists
-----------

*idsexists* script shows lists of all scenarios where specified ids is exists. Just provide idsname as input arguement to the script and sit back.

Syntax
~~~~~~
.. code-block:: bash

    $ python idsexists.py -h
    Install tqdm to enable progress bar
    usage: idsexists.py [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] ids

    Checks if spciefied ids is exists in scenario database

    positional arguments:
    ids                   Name of the IDS to check if it is available in scenario

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


Example
~~~~~~~
.. code-block:: bash

    $ python idsexists.py edge_profiles
    (123148, 4)
    (123285, 1)
    (123166, 2)
    (112325, 3)
    (102425, 2)
    (123305, 1)
    (103034, 3)

equiplot
----------

*equiplot* script shows plasma equilibrium. Optionally it also shows pf coils position and toroidal flux.

Syntax
~~~~~~
.. code-block:: bash

    $ python scripts/equiplot.py -h
    usage: equiplot.py [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN
                    [-t TIME] [-o OCCURRENCE] [--rho] [--pfcoils] [--save] [-i]

    ---- Display the plasma equilibrium from the equilibrium IDS. It also shows pf coils position overlay if exists

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
    -t TIME, --time TIME  Time (default=middle)
    -o OCCURRENCE, --occurrence OCCURRENCE
                            Occurrence number (default=0)
    --rho                 Show pf coils overlay on the plot
    --pfcoils             Show pf coils overlay on the plot
    --save                Save figure at default location
    -i, --info            Adds all extra provenance info to the plot

Example
~~~~~~~
    .. code-block:: bash

        python equiplot.py -s 134174 -r 117 --rho --pfcoils --info

    .. image:: _static/images/EquilibriumView_viewMagneticPoloidalFlux.png
        :alt: image not found
        :align: center

    .. image:: _static/images/PFActiveView_viewActivePfCoils.png
        :alt: image not found
        :align: center


idsdiff
----------

*idsdiff* script shows ids level differences between two runs. It stores result in html document. For signals differences it is also shown as graph.

Syntax
~~~~~~
.. code-block:: bash

    $ python idsdiff.py -h
    usage: idsdiff.py [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION]
                    [--backendB BACKENDB] [--databaseB DATABASEB] [--userB USERB] [--skip-provenance]
                    [--generate-html] [--report-dir REPORT_DIR]
                    shotA runA shotB runB [ids [ids ...]]

    Compare a IDS from 2 datasets

    positional arguments:
    shotA                 shot number of first dataset
    runA                  run number of first dataset
    shotB                 shot number of second dataset
    runB                  run number of second dataset
    ids                   Name (or space separated list of names) of IDS to compare (leave empty to compare all IDSs)

    optional arguments:
    -h,         --help            show this help message and exit
    -u USER,    --user_or_path USER
                            user (default=public)
    --database DATABASE, -d DATABASE
                            database name (default=ITER)
    --backend BACKEND, -b BACKEND
                            backend format (default=MDSPLUS)
    --version VERSION, -v VERSION
                            data version (default=3)
    --backendB BACKENDB   Specifies the backend of second dataset (default: same as first dataset)
    --databaseB DATABASEB
                            Specifies the database name of second dataset (default: same as first dataset)
    --userB USERB         Specifies the owner (username) of second dataset (default: same as first dataset)
    --skip-provenance     Discards provenance data differences (optional)
    --generate-html       Generate static html page for showing difference including plots
    --report-dir REPORT_DIR
                            Specifies directory where report should be stored

Example
~~~~~~~
    .. code-block:: bash

        python scripts/idsdiff.py --generate-html 122525 1 122525 2 summary

    .. image:: _static/images/idsdiff_1.png
        :alt: image not found
        :align: center


    .. image:: _static/images/idsdiff_2.png
        :alt: image not found
        :align: center


ecstray
---------

*ecstray* script shows electron cyclotron stray radiation information by showing different plots. It shows cut off layer, resonance layer, top view equilibrium.


Syntax
~~~~~~
.. code-block:: bash

    $ python scripts/ecstray.py -h
    Install tqdm to enable progress bar
    usage: ecstray.py [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN

    ---- Shows electron cyclotron stray radiation information by showing different plots

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

Example
~~~~~~~
    .. code-block:: bash

        python scripts/ecstray.py -s 134174 -r 117

    .. image:: _static/images/ecstray.png
        :alt: image not found
        :align: center