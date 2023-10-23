viewsources
==========

*viewsources* script shows source information from available sources. It uses `core_sources ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/core_sources.html>`
It gives information about Mass of atom, Nuclear charge and Ion charge along with particles and energy flux of ions.

Syntax viewsources
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    $ viewsources -h
    usage: viewsources [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-m {CLOSEST,PREVIOUS,LINEAR}]
                      [-o OCCURRENCE] [-t TIME]
                      shot run

    View information about sources

    positional arguments:
      shot                  Shot number
      run                   Run number

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
      -t TIME, --time TIME  Time


Example viewsources
~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ viewsources 134174  117
        Time = 10.599 for public/ITER/3/134174/117
        total
                            electrons            particles(--)     energy  2.499896e+06
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40             6.564372e+21                       --
              3.0       1.0    -9e+40             6.564375e+21                       --
              9.0       4.0    -9e+40             0.000000e+00                       --
        auxiliary
                            electrons            particles(--)     energy  1.000030e+03
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        nbi
                            electrons            particles(--)     energy  0.000000e+00
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40             0.000000e+00                       --
              3.0       1.0    -9e+40             0.000000e+00                       --
              9.0       4.0    -9e+40             0.000000e+00                       --
        ec
                            electrons            particles(--)     energy  1.000030e+03
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        lh
                            electrons            particles(--)     energy  0.000000e+00
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        ic
                            electrons            particles(--)     energy  0.000000e+00
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        fusion
                            electrons            particles(--)     energy  5.340175e-01
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40            -1.012115e+12                       --
              3.0       1.0    -9e+40            -9.713402e+11                       --
              9.0       4.0    -9e+40             0.000000e+00                       --
        ohmic
                            electrons            particles(--)     energy  2.553747e+06
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        bootstrap_current
                            electrons            particles(--)               energy(--)
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        radiation
                            electrons            particles(--)     energy -2.312020e+04
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        synchrotron_radiation
                            electrons            particles(--)     energy -3.646184e+02
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        collisional_equipartition
                            electrons            particles(--)     energy -1.259825e+06
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        cold_neutrals
                            electrons            particles(--)     energy -3.173155e+04
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40             6.564372e+21                       --
              3.0       1.0    -9e+40             6.564375e+21                       --
              9.0       4.0    -9e+40             0.000000e+00                       --
        charge_exchange
                            electrons            particles(--)               energy(--)
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        pellet
                            electrons            particles(--)               energy(--)
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40             0.000000e+00                       --
              3.0       1.0    -9e+40             0.000000e+00                       --
              9.0       4.0    -9e+40             0.000000e+00                       --

    .. code-block:: bash

        $ viewsources 134174  117 -m PREVIOUS -t 50

        Time = 48.938 for public/ITER/3/134174/117
        total
                            electrons            particles(--)     energy  2.203519e+07
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40             4.710725e+21                       --
              3.0       1.0    -9e+40             4.710724e+21                       --
              9.0       4.0    -9e+40             0.000000e+00                       --
        auxiliary
                            electrons            particles(--)     energy  2.000062e+07
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        nbi
                            electrons            particles(--)     energy  0.000000e+00
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40             0.000000e+00                       --
              3.0       1.0    -9e+40             0.000000e+00                       --
              9.0       4.0    -9e+40             0.000000e+00                       --
        ec
                            electrons            particles(--)     energy  2.000062e+07
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        lh
                            electrons            particles(--)     energy  0.000000e+00
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        ic
                            electrons            particles(--)     energy  0.000000e+00
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        fusion
                            electrons            particles(--)     energy  2.845680e+03
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40            -6.465727e+15                       --
              3.0       1.0    -9e+40            -6.293794e+15                       --
              9.0       4.0    -9e+40             0.000000e+00                       --
        ohmic
                            electrons            particles(--)     energy  2.456604e+06
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        bootstrap_current
                            electrons            particles(--)               energy(--)
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        radiation
                            electrons            particles(--)     energy -3.902759e+05
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        synchrotron_radiation
                            electrons            particles(--)     energy -1.699482e+05
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        collisional_equipartition
                            electrons            particles(--)     energy -1.162582e+07
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        cold_neutrals
                            electrons            particles(--)     energy -3.460606e+04
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40             4.710731e+21                       --
              3.0       1.0    -9e+40             4.710730e+21                       --
              9.0       4.0    -9e+40             0.000000e+00                       --
        charge_exchange
                            electrons            particles(--)               energy(--)
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40                       --                       --
              3.0       1.0    -9e+40                       --                       --
              9.0       4.0    -9e+40                       --                       --
        pellet
                            electrons            particles(--)               energy(--)
                a       z_n     z_ion                particles                   energy
              2.0       1.0    -9e+40             0.000000e+00                       --
              3.0       1.0    -9e+40             0.000000e+00                       --
              9.0       4.0    -9e+40             0.000000e+00                       --