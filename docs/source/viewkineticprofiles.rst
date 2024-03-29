#####################
 viewkineticprofiles
#####################

*viewkineticprofiles* shows plasma kinetic profiles from the
core_profiles IDSs
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`

****************************
 Syntax viewkineticprofiles
****************************

.. code-block:: bash

   $ viewkineticprofiles -h
   usage: viewkineticprofiles [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-t TIME] [-e] [--verbose] [--save]

   ---- Display the plasma kinetic profiles from the core_profiles IDSs

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
   -e, --edge            Add edge profiles if available
   --verbose             Verbose output
   --save                Save figure at default location

*****************************
 Example viewkineticprofiles
*****************************

   .. code-block:: bash

      $ viewkineticprofiles -s 134174 -r 117
      Time  = 71.44 s in range [10.60,75.00] s
      Index = 53
      Averaged resolution = 0.6133411929278538 s
      Time  = 71.44 s in range [1.20,149.44] s
      Index = 53
      Averaged resolution = 1.4117675982100488 s
      Ti_flag : 1, Ti_e_flag : 0
      ------------
      species:      D       T       Be
      a:            2.0     3.0     9.0
      z:            1.0     1.0     4.0
      n_over_ntot:  0.504   0.495   0.001
      n_over_ne:    0.502   0.494   0.001
      n_over_n_maj: 1.000   0.984   0.002

   .. image:: _static/images/viewkineticprofiles.png
      :alt: image not found
      :align: center
