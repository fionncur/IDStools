idssize
======

*idssize*  retrieves the size of IDS objects from a database entry and shows IDS size in bytes and the time taken to read each object. 
It also shows total size of all IDS objects in the data entry. It shows total time taken to read all objects from the data entry. 
It is helpful for performance check of ids objects.


Syntax
~~~~~~

    .. code-block:: bash     

        $ idssize --help
        Install tqdm to enable progress bar
        usage: idssize [-h] [-u USER] [--database DATABASE] [--backend BACKEND] [--version VERSION]
                    shot run [ids [ids ...]]

        Show size and time of IDSs

        positional arguments:
        shot                  Shot number
        run                   Run number
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



Example
~~~~~~~

    .. code-block:: bash

        $ idssize 134174 117
        Install tqdm to enable progress bar
        Examining data for public, ITER, 3, 134174, 117
        Reading 16.903 MB of data for core_profiles/0 took 1.05 seconds
        Reading 30.329 MB of data for core_sources/0 took 2.66 seconds
        Reading 24.918 MB of data for core_transport/0 took 1.68 seconds
        Reading 337.810 MB of data for edge_profiles/0 took 83.88 seconds
        Reading 153.541 MB of data for edge_sources/0 took 72.72 seconds
        Reading 85.343 MB of data for edge_transport/0 took 68.20 seconds
        Reading 48.121 MB of data for equilibrium/0 took 0.61 seconds
        Reading 0.056 MB of data for summary/0 took 0.10 seconds
        Total reading time = 230.91 s
        Total data size = 697.0 MB
        Fractions of the total size for public/ITER/3/134174/117
        % bytes    IDS
        2.4 %     core_profiles/0
        4.4 %     core_sources/0
        3.6 %     core_transport/0
        48.5 %     edge_profiles/0
        22.0 %     edge_sources/0
        12.2 %     edge_transport/0
        6.9 %     equilibrium/0
        0.0 %     summary/0


