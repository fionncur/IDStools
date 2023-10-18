viewneutron
===========

*viewneutron*  plots particles vs normalised toroidal flux coordinate. It retrieves from `distribution_sources` IDS.
https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/distribution_sources.html


Syntax viewneutron
~~~~~~~~~~~~~~~

    .. code-block:: bash   

        $ viewneutron -h
        usage: viewneutron [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-t TIME] [--save] [-i]

        ---- Display the neutron profiles from the distribution_sources IDSs

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
        -t TIME, --time TIME  Time
        --save                Save figure at default location
        -i, --info            Adds all extra provenance info to the plot


Example 
~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ viewneutron -s 121014 -r 11 -t 450 --info
        Time  = 482.00 s
        Distribution_sources contains 9 sources
        D + D -> He3 + n(2.45 MeV); Total; P = 136.60 kW
        D + D -> He3 + n(2.45 MeV); Thermal - Thermal; P = 1.57 kW
        D + D -> He3 + n(2.45 MeV); Beam - Thermal; P = 135.03 kW
        D + D -> He3 + n(2.45 MeV); Total; P = -90000000000000011196554993145437224960.00 kW
        D + T -> He4 + n(14.1 MeV); Total; P = 29.37 kW
        D + T -> He4 + n(14.1 MeV); Thermal - Thermal; P = 0.12 kW
        D + T -> He4 + n(14.1 MeV); Beam - Thermal; P = 0.57 kW
        D + T(1 MeV) -> He4 + n(14.1 MeV); Total; P = 29.37 kW
        D + T(1 MeV) -> He4 + n(14.1 MeV); Total; P = -90000000000000011196554993145437224960.00 kW


    .. image:: _static/images/plot_neutron.png
        :alt: image not found
        :align: center

