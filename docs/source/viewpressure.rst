##############
 viewpressure
##############

*viewpressure* Display the plasma kinetic profiles from the
core_profiles IDSs, It shows ion and electrons pressure properties from
core_profiles.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

*********************
 Syntax viewpressure
*********************

   .. code-block:: bash

      $ viewpressure -h
      usage: viewpressure [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-t TIME] [--save] [-i]

      Display the plasma kinetic profiles from the core_profiles IDSs

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
      -s SHOT, --shot SHOT  Shot number
      -r RUN, --run RUN     Run number
      -t TIME, --time TIME  Time
      --save                Save figure at default location
      -i, --info            Adds all extra provenance info to the plot

*********
 Example
*********

   .. code-block:: bash

      $ viewpressure -s 134174 -r 117
      Time  = 71.44 s in range [10.60,75.00] s
      Index = 53
      Averaged resolution = 0.6133411929278538 s
      Empty profiles_1d[0].pressure_fast_parallel
      Empty profiles_1d[0].pressure_fast_perpendicular
      Empty profiles_1d[0].electrons.pressure
      Empty profiles_1d[0].electrons.pressure_fast_parallel
      Empty profiles_1d[0].electrons.pressure_fast_perpendicular
      Total volume:83036.75126289157
      Empty profiles_1d[0].ion.pressure_fast_parallel
      Empty profiles_1d[0].ion.pressure_fast_perpendicular
      Empty profiles_1d[0].electrons.pressure
      Empty profiles_1d[0].electrons.pressure_fast_parallel
      Empty profiles_1d[0].electrons.pressure_fast_perpendicular

   .. image:: _static/images/plot_pressure.png
      :alt: image not found
      :align: center
