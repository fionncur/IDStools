##############
 viewrotation
##############

*viewrotation* Display the plasma kinetic profiles from the
core_profiles IDSs.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

*********************
 Syntax viewrotation
*********************

   .. code-block:: bash

      $ viewrotation -h
      usage: viewrotation [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-t TIME] [--save] [-i]

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
      --save                Save figure at default location
      -i, --info            Adds all extra provenance info to the plot

*********
 Example
*********

   .. code-block:: bash

      $ viewrotation -s 134174 -r 117
      Time  = 75.00 s in range [10.60,75.00] s
      Index = 105
      Averaged resolution = 0.6133411929278538 s
      core_profiles.profiles_1d[0].ion[0].velocity.diamagnetic could not be read
      core_profiles.profiles_1d[0].ion[1].velocity.diamagnetic could not be read
      core_profiles.profiles_1d[0].ion[2].velocity.diamagnetic could not be read

   .. image:: _static/images/viewrotation.png
      :alt: image not found
      :align: center
