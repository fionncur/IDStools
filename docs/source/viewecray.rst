###########
 viewecray
###########

*viewecray* shows plots for RF Waves and depositions. This script uses
output of TORBEAM code.
`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

******************
 Syntax viewecray
******************

.. code-block:: bash

    $ viewecray -h
    usage: viewecray [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-uri URI] [-s PULSE] [-r RUN] [-t TIME] [--wall] [--save]

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
    -uri URI, --uri URI   uri (default=None)
    -s PULSE, --shot PULSE, --pulse PULSE
                            Pulse number
    -r RUN, --run RUN     Run number
    -t TIME, --time TIME  Time
    --wall                Wall display flag
    --save                Save figure at default location

*******************
 Example viewecray
*******************

   .. code-block:: bash

        $ viewecray -d TEST -s 134173 -r 2326 
        $ viewecray --uri "imas:mdsplus?user=public;shot=134173;run=2326;database=TEST;version=3"

   .. image:: _static/images/viewecray.png
      :alt: image not found
      :align: center
