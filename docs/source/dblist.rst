########
 dblist
########

This program lists existing IMAS databases.

Possible commands are: list <shot number>- list existing databases
slices <shot number> <run number> - list existing databases, including
number of timeslices and time range for time-dependent IDSs times <shot
number> <run number> - list existing databases, including number of
timeslices their time points for time-dependent IDSs databases - list
existing databases (with data versions) dataversions - list existing
dataversions (with databases)

If the optional arguments shot number and run number are given, only
databases with these numbers will be shown.

If no command is given, the list command is performed.

To see databases stored in the public imas database, use 'public' as the
user name.

***************
 Syntax dblist
***************

    .. command-output:: dblist -h

****************
 Example dblist
****************

.. code-block:: bash

   # Show available databases
   $ dblist databases
   ITER      3
   ITER_MD      3
   TORBEAM      3
   test      3

.. code-block:: bash

   # Show available dataversions with databases from specific user database
   $ dblist -u $USER dataversions
   0 jet_reference
   3        DEBUG         GRAY          HCD         ITER      TORBEAM         

.. code-block:: bash

   # Show available dataversions with databases from specific user database
   $ dblist -u $USER databases
      DEBUG    3
      GRAY     3
      HCD      3
      ITER     3
      TORBEAM  3
      aug      3

.. code-block:: bash

   # Show available time slices with ids names from specific user database
   $ dblist -u $USER slices
   Database: DEBUG
      Data version: 3
         Backend: mdsplus
            Shot 130012
               Run:    26
                        core_profiles:    1 slices (149.98919999999998 - 149.98919999999998)
                        core_sources:    1 slices (149.98919999999998 - 149.98919999999998)
                  distribution_sources:    1 slices (149.98919999999998 - 149.98919999999998)
                        distributions:    1 slices (149.98919999999998 - 149.98919999999998)
                                 waves:    1 slices (149.98919999999998 - 149.98919999999998)
            Shot 134173
               Run:    26

.. code-block:: bash

   # Show available time slices with ids names from specific user database with specific shot/run
   $ dblist -u $USER slices 130012 26
   Database: DEBUG
      Data version: 3
         Backend: mdsplus
            Shot 130012
               Run:    26
                              core_profiles:    1 slices (149.98919999999998 - 149.98919999999998)
                              core_sources:    1 slices (149.98919999999998 - 149.98919999999998)
                        distribution_sources:    1 slices (149.98919999999998 - 149.98919999999998)
                              distributions:    1 slices (149.98919999999998 - 149.98919999999998)
                                       waves:    1 slices (149.98919999999998 - 149.98919999999998)

.. code-block:: bash

   # Show last modified databases with compact output from  specific user database
   dblist -u $USER  list -M -c 
   Database: DEBUG
      Data version: 3
         Backend: mdsplus
            Shot 130012:    1 runs
            Shot 134173:    1 runs
   Database: GRAY
      Data version: 3
         Backend: mdsplus
            Shot      0:    1 runs
            Shot 100000:    1 runs


.. code-block:: bash

   # Search data entries with just folder name
   dblist -f /work/imas/shared/imasdb/TEST/3/ --showuri list
   ┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ Sr. No. ┃ uri                                                             ┃
   ┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
   │ 0       │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/92436/850"   │
   │ 1       │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/134000/37"   │
   │ 2       │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/134173/2326" │
   │ 3       │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/134173/101"  │
   │ 4       │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/130012/125"  │
   │ 5       │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/130012/11"   │
   │ 6       │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/130012/14"   │
   │ 7       │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/130012/115"  │
   │ 8       │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/130012/13"   │
   │ 9       │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/130012/16"   │
   │ 10      │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/130012/105"  │
   │ 11      │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/130012/12"   │
   │ 12      │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/130012/15"   │
   │ 13      │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/130012/10"   │
   │ 14      │ "imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/100000/206"  │
   └─────────┴─────────────────────────────────────────────────────────────────┘


.. code-block:: bash

   # look for slices or time ranges and available idses using dblist with folder option
   $ dblist -f /work/imas/shared/imasdb/ITER/3/134174/ slices 134174
         Backend: hdf5
            Pulse /work/imas/shared/imasdb/ITER/3/134174/117/master.h5
   09:20:21 INFO     Parsing data dictionary version 3.42.0 @dd_zip.py:166
   09:20:21 INFO     Parsing data dictionary version 3.38.1 @dd_zip.py:166
                                                            core_profiles:  106 slices (10.599230769230868 - 75.00005602665553)
                                                            core_sources:  106 slices (10.599230769230868 - 75.00005602665553)
                                                            core_transport:  106 slices (10.599230769230868 - 75.00005602665553)
                                                            edge_profiles:  650 slices (10.1 - 75.0)
                                                            edge_sources:  650 slices (10.1 - 75.0)
                                                            edge_transport:  650 slices (10.1 - 75.0)
                                                            equilibrium:  106 slices (1.202 - 149.43759781205512)
                                                            summary:  106 slices (10.299692307692405 - 75.00005602665553)

