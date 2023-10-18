viewecstrayradiation
====================

*viewecstrayradiation* script shows electron cyclotron stray radiation information by showing different plots. It shows cut off layer, resonance layer, top view equilibrium.

.. note::
    This program is experimental and current in development.

Syntax viewecstrayradiation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    $ viewecstrayradiation -h
    Install tqdm to enable progress bar
    usage: ecstray.py [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN

    ---- Shows electron cyclotron stray radiation information by showing different plots

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

Example ecstray
~~~~~~~~~~~~~~~
    .. code-block:: bash

        $ viewecstrayradiation -s 134174 -r 117

    .. image:: _static/images/ecstray.png
        :alt: image not found
        :align: center


