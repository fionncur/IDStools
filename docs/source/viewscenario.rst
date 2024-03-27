##############
 viewscenario
##############

*viewscenario* Display the plasma kinetic profiles and equilibrium from
the core_profiles and equilibrium IDSs.

*********************
 Syntax viewscenario
*********************

   .. code:: bash

      $ viewscenario -h
      usage: viewscenario [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-t TIME | -n] [-i] [--save]

      ---- Display the plasma kinetic profiles and equilibrium from the core_profiles and equilibrium IDSs

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
      -t TIME, --time TIME  Time for profiles
      -n, --noProfiles      Do not plot profiles or equilibrium
      -i, --info            Add title with additional provenance information
      --save                Save figure at default location

*********
 Example
*********

   .. code:: bash

      $ viewpressure -s 134174 -r 117
      Time  = 71.44 s in range [10.60,75.00] s
      Index = 53
      Averaged resolution = 0.6133411929278538 s
      summary.global_quantities.energy_mhd.value could not be read
      HMode is not present
      HMode is not present
      HMode is not present
      HMode is not present

   .. image:: _static/images/viewscenario.png
      :alt: image not found
      :align: center
