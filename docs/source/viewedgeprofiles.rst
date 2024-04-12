viewedgeprofiles
================

*viewedgeprofiles* script shows edge profiles plots by interpolating on rectangular grid. It shows Electrons, Ions and Neutral density plots.

Syntax viewedgeprofiles
~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    $ viewedgeprofiles -h
    usage: viewedgeprofiles [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-uri URI] [-s PULSE] [-r RUN] [-t TIME] [--separatix]
                            [--wall] [--save]

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
    -uri URI, --uri URI   uri (default=None)
    -s PULSE, --shot PULSE, --pulse PULSE
                            Pulse number
    -r RUN, --run RUN     Run number
    -t TIME, --time TIME  Time
    --separatix           Show separtix
    --wall                Show wall
    --save                Save figure at default location


Example viewedgeprofiles
~~~~~~~~~~~~~~~~~~~~~~~~
    .. code-block:: bash

        $ viewedgeprofiles -s 123314 -r 1 --separatix --wall
        $ viewedgeprofiles --uri "imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3" --separatix --wall --time 60

    .. image:: _static/images/viewedgeprofiles.png
        :alt: image not found
        :align: center


