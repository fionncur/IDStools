
viewhcddistributions
====================

*viewhcddistributions* shows waveforms

Syntax viewhcddistributions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ viewhcddistributions -h
    usage: viewhcddistributions [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-uri URI] [-s PULSE] [-r RUN] [-t TIME] [--save]

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
    -t TIME, --time TIME  Time
    --save                Save figure at default location


Example viewhcddistributions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ viewhcddistributions -s 100015 -r 108 -u schneim -d SPOT
        

    .. image:: _static/images/viewhcddistributions.png
        :alt: image not found
        :align: center


    .. code-block:: bash

        $ viewhcddistributions -s 130012 -r 115 -d TEST
        $ viewhcddistributions --uri "imas:mdsplus?user=public;shot=130012;run=115;database=TEST;version=3" 

    .. image:: _static/images/viewhcddistributions2.png
        :alt: image not found
        :align: center



