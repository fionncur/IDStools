idssize
=======

*idssize*  retrieves the size of IDS objects from a database entry and shows IDS size in bytes and the time taken to read each object. 
It also shows total size of all IDS objects in the data entry. It shows total time taken to read all objects from the data entry. 
It is helpful for performance check of ids objects.


Syntax idssize
~~~~~~~~~~~~~~

    .. code-block:: bash     

        $ idssize -h
        usage: idssize [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION] [-uri URI] [-s PULSE] [-r RUN] [ids [ids ...]]

        Show size and time of IDSs

        positional arguments:
        ids                   Name (or space separated list of names) of IDS to (leave empty to show size of all IDSs)

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
        -uri URI, --uri URI   uri             (default=None)
        -s PULSE, --shot PULSE, --pulse PULSE
                                Pulse number
        -r RUN, --run RUN     Run number


Example idssize
~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ idssize -s 122525 -r 1
        Examining data for public, ITER, 3, 122525, 1
        Reading 0.001 MB of data for dataset_description/0 took 0.00 seconds
        Reading 0.003 MB of data for divertors/0 took 0.02 seconds
        Reading 35.431 MB of data for edge_profiles/0 took 5.58 seconds
        Reading 27.630 MB of data for edge_sources/0 took 5.62 seconds
        Reading 14.335 MB of data for edge_transport/0 took 4.48 seconds
        Reading 3.057 MB of data for equilibrium/0 took 0.02 seconds
        Reading 5.578 MB of data for radiation/0 took 3.94 seconds
        Reading 0.016 MB of data for summary/0 took 0.12 seconds
        Reading 0.011 MB of data for wall/0 took 0.01 seconds
        Total reading time = 19.79 s
        Total data size =  86.1 MB
        Fractions of the total size for public/ITER/3/122525/1
        % bytes    IDS
         0.00 %    dataset_description/0
         0.00 %    divertors/0
        41.17 %    edge_profiles/0
        32.11 %    edge_sources/0
        16.66 %    edge_transport/0
         3.55 %    equilibrium/0
         6.48 %    radiation/0
         0.02 %    summary/0
         0.01 %    wall/0



