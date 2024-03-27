###########
 viewecray
###########

*viewecray* shows plots for RF Waves and depositions. This script uses
output of TORBEAM code.

******************
 Syntax viewecray
******************

.. code-block:: bash

   $ viewwavespropndepo -h
   usage: viewwavespropndepo [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-t TIME] [--wall] [--save]

   ---- Display EC wave ray-tracing results

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
   -s SHOT, --shot SHOT  Shot number list, ex: [130012,130013]
   -r RUN, --run RUN     Run number list, ex: [23,24]
   -t TIME, --time TIME  Time
   --wall                Wall display flag
   --save                Save figure at default location

*******************
 Example viewecray
*******************

   .. code-block:: bash

      $ viewecray -d TEST -s 134173 -r 2326

   .. image:: _static/images/viewecray.png
      :alt: image not found
      :align: center
