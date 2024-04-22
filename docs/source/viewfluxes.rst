############
 viewfluxes
############

*viewfluxes* script shows flux information from available transport
models. It uses core_transport ids
It gives information about Mass of atom, Nuclear charge and Ion charge
along with particles and nergy flux of ions.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

*******************
 Syntax viewfluxes
*******************

   .. command-output:: viewfluxes -h


Example viewfluxes
~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: bash

        $ viewfluxes -p 134174 -r  117 -m CLOSEST
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

      $ viewfluxes -p 134174 -r 117 -m PREVIOUS -t 50

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
