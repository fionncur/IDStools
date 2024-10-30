#########
 idssize
#########

*idssize* retrieves the size of IDS objects from a database entry and
shows IDS size in bytes and the time taken to read each object. It also
shows total size of all IDS objects in the data entry. It shows total
time taken to read all objects from the data entry. It is helpful for
performance check of ids objects.

****************
 Syntax idssize
****************

   .. command-output:: idssize -h


Example idssize
~~~~~~~~~~~~~~~

    .. code-block:: bash

        $ idssize --uri "imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3"
        Reading 0.000 MB of data for dataset_description/0 took 0.00 seconds
        Reading 0.001 MB of data for divertors/0 took 0.00 seconds
        Reading 34.526 MB of data for edge_profiles/0 took 0.00 seconds
        Reading 26.076 MB of data for edge_sources/0 took 0.00 seconds
        Reading 12.907 MB of data for edge_transport/0 took 0.00 seconds
        Reading 3.057 MB of data for equilibrium/0 took 0.00 seconds
        Reading 4.164 MB of data for radiation/0 took 0.00 seconds
        Reading 0.006 MB of data for summary/0 took 0.00 seconds
        Reading 0.009 MB of data for wall/0 took 0.00 seconds
        Total reading time = 0.0000 s
        Total data size =  80.7 MB
        Fractions of the total size for imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3
        % bytes    IDS
        0.00 %    dataset_description/0
        0.00 %    divertors/0
        42.76 %    edge_profiles/0
        32.29 %    edge_sources/0
        15.98 %    edge_transport/0
        3.79 %    equilibrium/0
        5.16 %    radiation/0
        0.01 %    summary/0
        0.01 %    wall/0


