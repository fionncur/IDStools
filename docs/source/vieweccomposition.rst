###################
 vieweccomposition
###################

*vieweccomposition* shows ECRH and ECCD profiles and waveforms
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`

**************************
 Syntax vieweccomposition
**************************

.. code-block:: bash

   $ viieweccomposition -h
   usage: vieweccomposition [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-t TIME] [-f FORCE_PSI] [--verbose] [--save]

   ---- Display EC results

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
   -s SHOT, --shot SHOT  Shot number, either int 130012, or list [130012,130012]
   -r RUN, --run RUN     Run number, either int 23, or list [23,24]
   -t TIME, --time TIME  Time for which profiles are displayed
   -f FORCE_PSI, --force_psi FORCE_PSI
                           = 1 to force displaying the profiles versus poloidal flux
   --verbose             = 1 to display numerical analysis of gaussian profiles
   --save                Save figure at default location

***************************
 Example vieweccomposition
***************************

   .. code-block:: bash

      $ vieweccomposition -u schneim -d TORBEAM -s 134173 -r 2326

   .. image:: _static/images/vieweccomposition.png
      :alt: image not found
      :align: center
