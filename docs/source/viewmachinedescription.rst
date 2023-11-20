viewmachinedescription
======================

*viewmachinedescription*  plots machine description data stored in databases


Syntax viewmachinedescription
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code-block:: bash   

        $ viewmachinedescription -h
        usage: viewmachinedescription [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION]

        ---- View machine description

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

Example 
~~~~~~~

    .. code-block:: bash

        $ viewmachinedescription -d ITER_MD 
        23/11/20 23:20:26 INFO: Start of MDPLOT
        23/11/20 23:20:26 INFO: Reading meta data of MD
        23/11/20 23:20:26 INFO: Set target components
        23/11/20 23:20:26 INFO: Loading MD database
        23/11/20 23:20:26 INFO: Plotting MD
        23/11/20 23:20:26 WARNING: VS3U : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VS3L : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: TF coil busbars (equivalent coil) : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VC1 : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:20:26 WARNING: VC2 : pf_active.coil.element.geometry.rectangle is empty
        23/11/20 23:21:27 INFO: End of MDPLOT

    .. image:: _static/images/machine_description.png
        :alt: image not found
        :align: center
