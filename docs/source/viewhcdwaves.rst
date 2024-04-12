viewhcdwaves
============

*viewhcdwaves* shows hcd waveforms

Syntax viewhcdwaves
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ viewhcdwaves -h
    usage: viewhcdwaves [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-uri URI] [-s PULSE] [-r RUN] [-t TIME] [-f] [-l] [--save]

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
    -f, --force_psi       force displaying the profiles versus poloidal flux
    -l, --hide_legend     remove the legend from graphs
    --save                Save figure at default location



Example viewhcdwaves
~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ viewhcdwaves -s 134173 -r 101  -d TEST 
        $ viewhcdwaves --uri "imas:mdsplus?user=public;shot=134173;run=101;database=TEST;version=3"

    .. image:: _static/images/viewhcdwaves.png
        :alt: image not found
        :align: center


    .. code-block:: bash

        $ viewhcdwaves -s 105039 -r 1 -u schneim -d SAVE -t 25

    .. image:: _static/images/viewhcdwaves2.png
        :alt: image not found
        :align: center



