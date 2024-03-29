##################
 viewedgeprofiles
##################

*viewedgeprofiles* script shows edge profiles plots by interpolating on
rectangular grid. It shows Electrons, Ions and Neutral density plots.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`

*************************
 Syntax viewedgeprofiles
*************************

.. code-block:: bash

   $ viewedgeprofiles -h
   usage: viewedgeprofiles [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-t TIME] [--separatix] [--save]

   ---- Edge Profile plot

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
   --separatix           Show separtix
   --save                Save figure at default location

**************************
 Example viewedgeprofiles
**************************

   .. code-block:: bash

      $ viewedgeprofiles -s 123314 -r 1

   .. image:: _static/images/viewedgeprofiles.png
      :alt: image not found
      :align: center
