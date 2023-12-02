viewcoresources
===============

*viewsources* plot core_sources results. It uses `core_sources ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/core_sources.html>`


Syntax viewcoresources
~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    $ viewcoresources -h
    usage: viewcoresources [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-t TIME] [--save] [-i]

    ---- Display core_sources results

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
    -t TIME, --time TIME  time
    --save                Save figure at default location
    -i, --info            Adds all extra provenance info to the plot


Example viewcoresources
~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ viewcoresources -s 130012 -r 5 -u username -d ITER
        Time  = 190.82 s in range [31.20,328.18] s
        Index = 8
        Averaged resolution = 19.79856 s
        Core_sources contains 1 source
        

    .. image:: _static/images/viewcoresources1.png
        :alt: image not found
        :align: center

    .. image:: _static/images/viewcoresources2.png
        :alt: image not found
        :align: center
