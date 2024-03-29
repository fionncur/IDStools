#################
 viewequilibrium
#################

*viewequilibrium* script shows plasma equilibrium. Optionally it also
shows pf coils position and toroidal flux.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

************************
 Syntax viewequilibrium
************************

.. code-block:: bash

   $ viewequilibrium -h
   usage: viewequilibrium [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN
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
   --rho                 Show rho overlay on the plot
   --pfcoils             Show pf coils overlay on the plot
   --save                Save figure at default location
   -i, --info            Adds all extra provenance info to the plot

*************************
 Example viewequilibrium
*************************

   .. code-block:: bash

      $ viewequilibrium -s 134174 -r 117 --rho --pfcoils --info

   .. image:: _static/images/EquilibriumView_viewMagneticPoloidalFlux.png
      :alt: image not found
      :align: center

   .. image:: _static/images/PFActiveView_viewActivePfCoils.png
      :alt: image not found
      :align: center
