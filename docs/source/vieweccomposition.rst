vieweccomposition
=================

*vieweccomposition* shows EC composition (ECRH and ECCD profiles)

Syntax vieweccomposition
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ vieweccomposition -h
    usage: vieweccomposition [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-uri URI] [-s PULSE] [-r RUN] [-t TIME] [-f FORCE_PSI]
                            [--verbose] [--save]

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
    -uri URI, --uri URI   uri (default=None)
    -s PULSE, --shot PULSE, --pulse PULSE
                            Pulse number
    -r RUN, --run RUN     Run number
    -t TIME, --time TIME  Time for which profiles are displayed
    -f FORCE_PSI, --force_psi FORCE_PSI
                            = 1 to force displaying the profiles versus poloidal flux
    --verbose             = 1 to display numerical analysis of gaussian profiles
    --save                Save figure at default location


Example vieweccomposition
~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ vieweccomposition -d TEST -s 134173 -r 2326 
        $ vieweccomposition --uri "imas:mdsplus?user=public;shot=134173;run=2326;database=TEST;version=3"

    .. image:: _static/images/vieweccomposition.png
        :alt: image not found
        :align: center






