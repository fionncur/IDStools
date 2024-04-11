viewfluxes
==========

*viewfluxes* script shows flux information from available transport models. It uses `core_transport ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/core_transport.html>`
It gives information about Mass of atom, Nuclear charge and Ion charge along with particles and nergy flux of ions.

Syntax viewfluxes
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    $ viewfluxes -h
    usage: viewfluxes [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-uri URI] [-s PULSE] [-r RUN] [-m {CLOSEST,PREVIOUS,LINEAR}]
                      [-o OCCURRENCE] [-t TIME]

    View information about fluxes

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
      -uri URI, --uri URI   uri             (default=None)
      -s PULSE, --shot PULSE, --pulse PULSE
                            Pulse number
      -r RUN, --run RUN     Run number
      -m {CLOSEST,PREVIOUS,LINEAR}, --slicingmethod {CLOSEST,PREVIOUS,LINEAR}
                            Slicing method  (default=CLOSEST)
      -o OCCURRENCE, --occurrence OCCURRENCE
                            occurrence
      -t TIME, --time TIME  Time



Example viewfluxes
~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ viewfluxes -s 134174 -r  117 -m CLOSEST
        $ viewfluxes --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3"

        Showing details for sdcc-login01.iter.org:/work/imas/shared/imasdb/ITER/3 (pulse 134174,117 time:10.60))

        combined (-9e+40)
                            electrons            particles(--)               energy(--)
              a       z_n     z_ion                particles                   energy
            2.0       1.0    -9e+40                       --                       --
            3.0       1.0    -9e+40                       --                       --
            9.0       4.0    -9e+40                       --                       --

        transport_solver (-9e+40)
                            electrons            particles(--)               energy(--)
              a       z_n     z_ion                particles                   energy
            2.0       1.0    -9e+40                       --                       --
            3.0       1.0    -9e+40                       --                       --
            9.0       4.0    -9e+40                       --                       --

        neoclassical (-9e+40)
                            electrons            particles(--)               energy(--)
              a       z_n     z_ion                particles                   energy
            2.0       1.0    -9e+40                       --                       --
            3.0       1.0    -9e+40                       --                       --
            9.0       4.0    -9e+40                       --                       --

        anomalous (-9e+40)
                            electrons            particles(--)               energy(--)
              a       z_n     z_ion                particles                   energy
            2.0       1.0    -9e+40                       --                       --
            3.0       1.0    -9e+40                       --                       --
            9.0       4.0    -9e+40                       --                       --



    .. code-block:: bash

        $ viewfluxes 134174  117 -m PREVIOUS -t 50

        Showing details for sdcc-login01.iter.org:/work/imas/shared/imasdb/ITER/3 (pulse 134174,117 time:48.938))

        combined (-9e+40)
                            electrons            particles(--)               energy(--)
              a       z_n     z_ion                particles                   energy
            2.0       1.0    -9e+40                       --                       --
            3.0       1.0    -9e+40                       --                       --
            9.0       4.0    -9e+40                       --                       --

        transport_solver (-9e+40)
                            electrons            particles(--)               energy(--)
              a       z_n     z_ion                particles                   energy
            2.0       1.0    -9e+40                       --                       --
            3.0       1.0    -9e+40                       --                       --
            9.0       4.0    -9e+40                       --                       --

        neoclassical (-9e+40)
                            electrons            particles(--)               energy(--)
              a       z_n     z_ion                particles                   energy
            2.0       1.0    -9e+40                       --                       --
            3.0       1.0    -9e+40                       --                       --
            9.0       4.0    -9e+40                       --                       --

        anomalous (-9e+40)
                            electrons            particles(--)               energy(--)
              a       z_n     z_ion                particles                   energy
            2.0       1.0    -9e+40                       --                       --
            3.0       1.0    -9e+40                       --                       --
            9.0       4.0    -9e+40                       --                       --



