idsprint
========

*idsprint* is a utility that, as the name implies, dumps or prints all data on the console.
It is handy if you need to rapidly verify if specific fields or attributes have been 
filled out or empty . The output can also be saved to a file using extraction.


Syntax idsprint
~~~~~~~~~~~~~~~

    .. code-block:: bash     

        $ idsprint -h
        usage: idsprint.py [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] -s SHOT -r RUN [-f] ids

        Prints content of an IDS onto the terminal

        positional arguments:
        ids                   Name of the IDS to dump

        optional arguments:
        -h, --help            show this help message and exit
        -u USER, --user_or_path USER
                                user            (default=public)
        --database DATABASE, -d DATABASE
                                database name   (default=ITER)
        --backend BACKEND, -b BACKEND
                                backend format  (default=MDSPLUS)
        --version VERSION, -v VERSION
                                data version    (default=3)
        -s SHOT, --shot SHOT  Shot number
        -r RUN, --run RUN     Run number
        -f, --full            Print all array elements (can be very slow for large data)


Example idsprint
~~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ idsprint -s 134174 -r 117 equilibrium

        class equilibrium
        Attribute ids_properties
            class ids_properties
            Attribute comment: 
            Attribute homogeneous_time: 1
            Attribute source: 
            Attribute provider: 
            Attribute creation_date: 
            Attribute version_put

